# PostgreSQL → Doris 验证与修复工作流

本指南面向提供 PostgreSQL 测试 SQL、DDL/数据和配对 .out 的用户。工作流只有四步：准备数据、确定性验证、人工调用归因 Skill、人工调用修复 Skill。所有 Shell 命令从仓库根目录执行；安装方式见 [README](../README.md#安装)。

本仓库不附带测试 SQL、参考输出、Case YAML 或已执行报告。下文路径是运行约定，只有实际执行后才产生文件，不要把模板当作已经完成的证据。

## 1. 职责与执行方式

| 步骤 | 工具 | 输入 | 输出 |
| :--- | :--- | :--- | :--- |
| 1. 准备数据 | 外部 SQL 客户端，或显式调用 pg-doris-prepare-data Skill | 原 SQL/.out、DDL/INSERT/COPY 及数据依赖、双端测试库 | 准备报告和双端准备 SQL |
| 2. 确定性验证 | import-cases、cases-lint、run | SQL/.out → Case YAML；多数据状态时按 stage 分组 | 每份 YAML 对应一份验证 JSON；一个批次可有多个 stage |
| 3. 差异归因 | 显式调用 pg-doris-attribute Skill；必要时用 probe-pg-batch / probe-pg-case | 验证 JSON、准备材料、代码库和两端只读连接 | 批次汇总（含任务索引）与每条待调查 SELECT 的 Markdown |
| 4. 修复与回归 | 显式调用 pg-doris-fix Skill | 选定任务或整份输入授权、归因证据和 SQLGlot checkout | 代码/测试、每轮汇总和任务 Markdown；获授权时独立 commit 到 fork |

import-cases、cases-lint、run、probe-pg-case 和 probe-pg-batch 是普通 Python 程序，不调用模型。三个项目 Skill 位于 .agents/skills/，仅由人显式调用；CLI 不自动触发 Skill，也不自动进入下一步。

验证器不执行 DDL/DML，不复制数据，不检查两端基表是否相同。数据准备、代码修改、commit 和 push 分别按明确授权执行；不向社区自动创建 Issue/PR。验证完成后可直接调用归因 Skill，不需要额外交接入口或索引。社区当前仅接受维护者 PR，外部报告走 Issue，详见 [SQLGlot 贡献指南](https://github.com/tobymao/sqlglot/blob/main/CONTRIBUTING.md)；本流程以 fork 内修复提交和实际验收为交付，不以社区 PR 为结束条件。

整份输入持续修复模式的目标：在固定原 SQL/.out、数据阶段和比较规则下，将所有已确认可由 SQLGlot 安全修复的问题修复并验收，持续调查新暴露差异。初始任务清单或 fix-001 执行完毕不等于整份输入完成；完整条件见第 7.5 节。

## 2. 输入与目录约定

~~~text
用户原始输入（路径任意，不要求搬入仓库）
  aggregates.sql / aggregates.out                   原文件名保持不变
  DDL、INSERT/COPY、data/                     原脚本所需的准备材料和数据依赖

reports/                                     统一按阶段分目录
├── data-preparation/                        步骤一和二的文件平铺，按批次前缀归组
│   ├── aggregates-001-data-preparation.md       数据准备、核验证据和类型映射
│   ├── aggregates-001-postgres-setup.sql        源端实际采用的准备脚本
│   ├── aggregates-001-doris-setup.sql           目标准备脚本
│   ├── aggregates-001-stage-01-cases.yaml    步骤二：第一数据状态对应的查询和数据库配置
│   ├── aggregates-001-stage-02-cases.yaml    步骤二：第二数据状态对应的查询和数据库配置
│   └── aggregates-001-stage-43-cases.yaml    中间阶段省略；43 是本次完整样本的实际阶段数
├── validation/                              步骤二报告平铺，每个 stage 一份 JSON
│   ├── aggregates-001-stage-01-validation.json 第一阶段的运行信息、总结和逐查询记录
│   ├── aggregates-001-stage-02-validation.json 第二阶段的结果，不重复第一阶段的查询
│   └── aggregates-001-stage-43-validation.json 与同名阶段 YAML 一一对应，中间阶段省略
├── attribution/                             步骤三由人工调用 Skill 后生成
│   ├── aggregates-001-attribution-summary.md    首轮归因及唯一当前任务清单，后续增量维护
│   └── cases/aggregates-001/<case-id>.md        每条待调查 SELECT 一份，后续证据追加，不按轮次复制
└── fixes/                                   步骤四只保存汇总与逐修复任务报告
    ├── aggregates-001-fix-001-summary.md        第一轮范围、状态、commit、回归及全批剩余项
    ├── aggregates-001-fix-002-summary.md        后续轮次实际运行才产生，不覆盖前轮
    └── tasks/aggregates-001/<fix-batch>/<task-id>.md 本轮每任务一份，跨轮沿用 task-id
~~~

batch-id 是输入批次标识，不是 Case ID。使用实际源文件去扩展名名称加三位编号：aggregates.sql 首次为 aggregates-001，同名下一次为 aggregates-002；多个文件作为一批时使用用户指定的组名。用户或显式调用的数据准备 Agent 从已有最大编号递增，检查所有同前缀产物未占用，不能按文件数量推算。

同一输入继续修复使用原 batch-id 和递增 fix-001、fix-002 等轮次，不重新上传输入或改成 aggregates-002。task-id 是跨轮稳定的问题编号；一个 task 可以关联多个 Case/commit，一轮可以处理多个 task。commit 是实际代码提交，不是修复轮次，也不按每条 SQL 分配。

stage 是同一批次内的数据库状态编号，不是工作流步骤，也不是 SQL 文件编号。上图采用完整 aggregates.sql 的多状态布局；只有一个数据状态的输入仍使用 aggregates-001-cases.yaml 和 aggregates-001-validation.json，不要求增加 stage。阶段数量取决于实际脚本及准备方案，不固定为 43，具体划分见步骤二。

这是命名约定，不是 CLI 自动编号功能。CLI 没有 --batch-id 参数，也不会扫描旧报告分配编号。原输入可留在任何用户指定位置；inputs/postgres/aggregates-001/ 只是下文命令采用的示例位置。

~~~text
固定命名规则
  准备文件：reports/data-preparation/<batch-id>-...
  单状态 YAML：reports/data-preparation/<batch-id>-cases.yaml
  单状态验证：reports/validation/<batch-id>-validation.json
  多状态 YAML：reports/data-preparation/<batch-id>-stage-<两位阶段号>-cases.yaml
  多状态验证：reports/validation/<batch-id>-stage-<两位阶段号>-validation.json
  归因汇总：reports/attribution/<batch-id>-attribution-summary.md
  逐条归因：reports/attribution/cases/<batch-id>/<case-id>.md
  修复汇总：reports/fixes/<batch-id>-<fix-batch>-summary.md
  逐项修复：reports/fixes/tasks/<batch-id>/<fix-batch>/<task-id>.md

import-cases --output    指定 YAML 完整路径，不自动添加批次前缀。
run --output             指定 JSON 完整路径，不创建同批次的外层目录。
run 未指定上述两参数     从 YAML 文件名去掉扩展名及末尾 -cases，
                         默认保存 reports/validation/<所得名称>-validation.json。
                         stage-01-cases.yaml 因此对应 stage-01-validation.json；
                         多个 stage 各运行一次，不自动合并成一个 JSON。
run --stdout             只向终端返回同结构 JSON，不写文件；不能与 --output 同用。
probe-pg-case            --candidate-sql 接受文本，返回事实到终端，不生成文件或目录。
probe-pg-batch           --candidates-json 接受同阶段多条请求，返回统计和逐条事实；不生成文件。
~~~

YAML 用相对于自身目录的路径引用原 SQL/.out，不复制原件。recorded_output 只保存格式、路径及可选 Driver，不保存 .out 内容指纹。每次 run 直接读取当前路径中的 .out，再按 SQL 内容和出现序号定位结果；不检查它是否被修改。源脚本和 YAML 的内容指纹仍可用于报告/对照对应关系检查，与 .out 是否改变无关。

同文 SELECT 的每次出现保留独立 Case ID 和 output_occurrence，不按 SQL 文本去重。若脚本是 INSERT → SELECT → UPDATE → SELECT，两次查询可能读取不同数据；必须在验证器外按阶段准备和运行，不能用最终数据一次运行全部查询。批次编号不会隔离、恢复或锁定数据库。

## 3. 环境配置

先按 README 安装 Python 3.12 和相邻 SQLGlot checkout，从 .env.example 创建自己的 .env。真实地址、端口与凭据来自 POSTGRES_*、DORIS_*，YAML 只保存方言、引擎、逻辑连接名和库名。

~~~bash
./scripts/postgres.sh up
./scripts/postgres.sh smoke
.venv/bin/doris-sql-validator doctor --source-engine postgres
~~~

Doris 由用户自行启动。doctor 会检查两端；首轮 Recorded Output 验证不要求源库在线，但步骤三的实时补证需要 PostgreSQL。不要公开 .env 或在 YAML、报告、提示词中填写密码。使用独立测试库与只读验证账号；建表装数账号限于已授权范围。

## 4. 步骤一：准备相同逻辑数据

### 4.1 执行已有准备脚本

用户已有双端准备脚本时，在验证器之外通过 psql 与 MySQL 兼容客户端执行。先审查写入范围，保留重复行和 NULL；遇到同名且来源不明的库表先停止确认，不自动 DROP、TRUNCATE 或覆盖。

Recorded Output 只运行 Doris 时可仅准备目标端；实时 PostgreSQL 补证需要源端。准备脚本执行成功不等于数据相同，仍需核验查询所对应阶段、完整记录和类型映射。

### 4.2 显式调用数据准备 Skill

~~~text
使用 $pg-doris-prepare-data。
批次：aggregates-001；项目为当前工作流仓库。
输入：inputs/postgres/aggregates-001/aggregates.sql、aggregates.out 及全部 DDL/数据依赖。
允许仅在指定的 PostgreSQL/Doris 专用测试库中建表装数；未知已有对象停止询问。
逐阶段核对完整记录、重复次数、NULL、类型映射与 Session 限制。
原脚本含装数、对象替换或事务状态变化时，在准备报告中列出 stage 编号、
对应源查询位置、双端阶段库和 Session，供步骤二按原 Case 列表划分 YAML。
输出到 reports/data-preparation/，三个文件共用 aggregates-001- 前缀。
核验命令、实际输出和差异写入同一 Markdown，不另生成核验 JSON。
不修改源 SQL/.out 或 SQLGlot，不自动进入下一步。
~~~

按 [数据准备 Skill](../.agents/skills/pg-doris-prepare-data/SKILL.md) 及其 [模板](../.agents/skills/pg-doris-prepare-data/assets/data-preparation-template.md) 保存实际证据。命名由人或 Agent 确定，不是 CLI 自动分配。

### 4.3 本步骤产物

~~~text
reports/data-preparation/
├── aggregates-001-data-preparation.md     数据准备与核验的唯一报告
│   内容：原材料路径、数据库版本/Session、数据阶段与查询对应关系、逐列类型映射、
│         实际装数情况、完整数据核验方法/命令/输出、差异及未覆盖范围。
│   用途：让归因 Agent 判断数据前提，不能只写“通过”或只比较 COUNT/样本。
├── aggregates-001-postgres-setup.sql      实际采用的源端准备脚本
│   内容：经审查的建表、装数、阶段与必要 Session 操作，注明 COPY 依赖。
│   用途：复现对应源数据状态，由外部客户端执行，不替换用户原件。
└── aggregates-001-doris-setup.sql         实际采用的目标准备脚本
    内容：目标类型、表模型、装数和必要 Session 操作，保留重复记录和 NULL。
    用途：复现目标逻辑数据；不能因当前值可表示就宣称类型域完全相同。
~~~

数据/类型无法无损表示、只抽样或缺少执行证据时，明确受限查询和未核验范围。后续直接把这三份实际文件路径交给归因 Skill，不另生成引用索引。

## 5. 步骤二：生成 YAML 并运行确定性验证

### 5.1 数据阶段与文件命名

一个 SQL 文件可以只对应一个数据状态，也可以在执行过程中依次改变状态。以 aggregates.sql 为例，它包含空表查询、COPY 装数、CREATE OR REPLACE VIEW、事务内定义和 ROLLBACK；原 .out 中的每个结果对应查询当时的状态，而不是整个文件执行完后的最终状态。

~~~sql
-- 以下为说明数据状态的简化示意，不替换原测试 SQL。
CREATE TABLE sample (value INT);
SELECT COUNT(*) FROM sample;       -- 空表状态，源参考结果是 0
INSERT INTO sample VALUES (1);
SELECT COUNT(*) FROM sample;       -- 装数后状态，源参考结果是 1
~~~

如果统一装成最后的非空状态再跑这两条 SELECT，第一条会得到 1，即使 SQLGlot 转译正确也会误报。因此步骤一在验证器外准备并保留对应数据状态；步骤二只把各状态适用的 SELECT 交给对应数据库执行。验证器不执行上面示意中的建表或装数语句。

~~~text
输入：aggregates.sql + aggregates.out
批次：aggregates-001

单一状态时
  aggregates-001-cases.yaml                 全部查询共享文件顶层的双端数据库配置
  aggregates-001-validation.json            一次 run 的唯一报告

多个状态时
  aggregates-001-stage-01-cases.yaml        第一状态的查询子集，指定第一组阶段库
  aggregates-001-stage-01-validation.json   对应第一份 YAML 的一次 run
  aggregates-001-stage-02-cases.yaml        第二状态的查询子集，指定第二组阶段库
  aggregates-001-stage-02-validation.json   对应第二份 YAML 的一次 run
  ……                                       后续阶段依次编号，不按 SELECT 文本去重

完整 aggregates 样本的一次实际执行划分为 43 个 stage：
  YAML：aggregates-001-stage-01-cases.yaml 至 aggregates-001-stage-43-cases.yaml
  JSON：aggregates-001-stage-01-validation.json 至 aggregates-001-stage-43-validation.json
  313 条被 Importer 接受的查询分布在这些 YAML 中，每条出现只属于一个阶段。
  43 不是程序硬编码，也不是保证原脚本全部 SELECT 都已正确提取；导入遗漏须另报。
~~~

不是每条 DDL/DML 都机械新增一个 stage。按查询所需的表数据、对象定义和会话条件决定分组，在准备报告中写明依据。多个查询共享同一状态时可以放入一份 YAML；状态不同则不能仅因 SQL 文本相同而合并。

### 5.2 导入与分阶段 YAML 的产生方式

import-cases 只负责提取 Case，当前没有自动识别/重放数据阶段的调度能力，也没有 --stage 参数。它每次按 --output 写一份 YAML。下面命令适用于单一状态；多状态时，其输出只能作为待划分的导入结果，不能直接拿最终状态运行整份文件：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input inputs/postgres/aggregates-001/aggregates.sql \
  --recorded-output inputs/postgres/aggregates-001/aggregates.out \
  --source-database dsv_demo --target-database dsv_demo \
  --output reports/data-preparation/aggregates-001-cases.yaml
~~~

完整 aggregates.sql 应由人或显式调用的数据准备 Agent，基于这次导入的 Case 列表和步骤一的阶段对应表生成各 stage YAML；也可以在内存取得导入结果后直接保存各阶段，不落盘整份中间 YAML。划分时必须：

~~~text
每份 stage YAML
  source.database / target.database       改为准备报告中的对应阶段库
  input / recorded_output                 继续引用同一份原 aggregates.sql / aggregates.out
  cases                                   只保留本阶段的查询
    id / statement_index / line_start / line_end / output_occurrence / sql
                                          保留原导入值，不因分组重新编号或修改源 SQL
  import_summary / import_diagnostics      与该阶段的实际范围对应；导入遗漏和未分配诊断
                                          在同批准备报告/归因汇总明确说明，不无声丢弃

划分检查
  各阶段 Case ID 不重叠，合计与本次接受范围相符。
  同文 SELECT 在不同源位置仍保留不同 ID 和原 .out 出现序号。
  不能只重复 import-cases 并更换数据库名；那会反复包含整份查询，不是阶段划分。
  阶段映射属于外部准备，不给验证器增加 DDL/DML 或快照导入职责。
~~~

只有阶段 YAML 是后续的实际验证输入。若曾落盘整份中间 YAML，核对划分完整后不把它作为另一套正式输入或再运行一遍。

### 5.3 检查并执行每个阶段

以下命令在第一阶段双端测试库已由步骤一准备好之后执行：

~~~bash
.venv/bin/doris-sql-validator cases-lint \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml

.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --output reports/validation/aggregates-001-stage-01-validation.json
~~~

其余阶段同时替换 YAML 和 JSON 中的 stage-01，例如第二阶段用 stage-02，直到准备报告列出的最后一阶段。每次 run 只读这一份 YAML、只连接它指定的阶段库，不自动切换状态，也不执行准备脚本。单一状态则使用不带 stage 的文件名。

主工作流必须提供配对 .out。CLI 仍保留 Live Source 诊断能力，但读取 .out 失败不会自动改用源数据库。生成的 Doris SQL 只在有差异时保存到报告，不回写 YAML。cases-lint 只输出检查信息。

run 返回 1 通常表示发现失败或差异，报告仍已生成；输入/配置错误可能返回 2。全部无法导入时会直接报错，没有进入 run 便不能声称生成了验证报告。重复使用同一 --output 会覆盖该文件；需要保留重跑结果时显式选择新文件名。

### 5.4 本步骤产物与报告范围

~~~text
reports/data-preparation/aggregates-001-stage-01-cases.yaml
  内容：源/目标方言与逻辑配置、原 SQL 路径及来源指纹、.out 格式/路径、
        导入计数/诊断，每条只读查询的 ID、SQL 原文、源位置和出现序号。
  用途：run 的机器可读输入，不是 SQL 行号到 .out 行号的固定映射。
        不包含 .out 指纹、DDL/DML 执行步骤或人工标签/预期结论。
        与步骤一三份文件共用 aggregates-001 前缀，stage-01 额外区分数据状态。
        第二阶段对应 stage-02，依次类推；单一状态可省略整个 stage-XX 段。

reports/validation/aggregates-001-stage-01-validation.json   第一阶段唯一首轮报告
├── run        输入/YAML 路径与来源指纹、.out 路径/格式、运行时间、实际 SQLGlot
│              版本/提交、验证模式、双端逻辑配置及比较规则；不含密码或 .out 指纹。
├── summary    查询数、明确分母的匹配率、失败分类、负向用例数、待归因/前提排查数、
│              导入计数及证据限制。
└── queries    每条查询一条记录
    匹配：仅 id、source_sql、result，不重复目标 SQL、字段、样本或 Digest。
    差异：补充源状态、action、具体错误、生成 SQL及有限字段/行值反例。
    负向：保留源错误与已有目标表现，标注默认不归因，不生成独立文件。
    读取异常：已保留源 SQL 的导入 .out 读取失败也作为记录，防止漏计。
~~~

多个 stage 会产生多份 JSON，但每次 run 仍只保存一个 JSON，不额外生成验证 Markdown。步骤三直接读取同批全部阶段 JSON，并在一份 aggregates-001-attribution-summary.md 中汇总；不增加交接入口、阶段索引或另一份合并验证报告。跨阶段匹配率使用各阶段成功匹配数之和 / 已取得成功源结果数之和，不能直接平均各阶段百分比。

匹配率为成功匹配 / 已取得成功源结果的查询数，包括已经读到成功 .out 的转译失败，不含源端报错或源结果未知。action 为“归因”只表示需要调查，不等于已确认 SQLGlot 缺陷；“前提排查/补查源证据”先查环境和输出；源端负向默认不进入主修复清单。详细字段与示例见 [用户指南第 8 节](USER_GUIDE.md#8-验证报告结构与结果判读)。

比较仍基于取得的完整结果，报告只保存最多三个字段差异或每侧三种行反例及省略数。不保存完整大结果或重复的前五行；.out 缺失原生类型等维度不算已经验证。

### 5.5 参考输出定位

~~~text
import-cases
  拆分脚本 → 只保留只读查询及查询形状的 Parser 失败
  → 分配 ID、源位置和同文出现序号
  → 尝试按 SQL 回显/出现序号读取 .out，记录导入诊断
  → 写入 YAML，不复制完整结果，不保存 .out 指纹。

cases-lint
  检查 YAML 结构、ID 和统计，不连接数据库、不匹配 .out。

run
  直接读取当前 .out，不比较文件新旧指纹
  → 从 YAML 取源 SQL，调用 SQLGlot 生成 Doris SQL
  → 定位对应源输出并执行 Doris，按共用规则比较
  → 写入 --output 指定的单一 JSON。
  转译失败不执行双端 SQL，但仍尝试只读 .out 确认源状态；
  成功源结果进入主归因范围，源端负向默认排除，读取失败保留具体原因。
~~~

具体实现：importing/importer.py、source_provider.py 和 recorded_output/parsers.py。原 SQL 行号用于追踪，SQL 内容与 output_occurrence 才用于定位 .out。输入内容变动后要使用配套的 YAML/输出重新验证，不能让不同阶段的材料混用；框架不再用 .out 指纹强制执行这项约定。

## 6. 步骤三：逐 SELECT 归因并汇总修复任务

目标是找到社区 SQLGlot 转换到 Doris 的缺口，形成可实施的代码修改和测试要求，而不是只判断候选 SQL 当前值是否一致。归因阶段只保存两类 Markdown：批次汇总和每条待调查 SELECT 的报告，执行事实与原因直接写进同一文档，不另建执行文件。

~~~text
使用 $pg-doris-attribute。
批次：aggregates-001。
首轮报告：reports/validation/aggregates-001-stage-01-validation.json
          至 aggregates-001-stage-43-validation.json，读取准备报告列出的全部阶段，
          不只读取第一个 stage；具体阶段数以本次实际准备为准。
准备报告：reports/data-preparation/aggregates-001-data-preparation.md。
准备 SQL：reports/data-preparation/aggregates-001-postgres-setup.sql、
          reports/data-preparation/aggregates-001-doris-setup.sql。
从报告 run 定位 YAML、原 SQL/.out；SQLGlot checkout 为 ../sqlglot。
每条非匹配、非源端负向的查询生成 reports/attribution/cases/aggregates-001/<case-id>.md；
包含首轮事实、完整候选、真实执行摘要、具体原因、代码依据、修复方案和测试要求。
按可独立实施、验证和审查的行为修复形成 task；同根因的多条 Case 共享任务，
不同实现机制或过宽的问题组拆分，不按每条 Case、函数、文件或执行轮次分配 commit。
在汇总的任务条目集中写目标、纳入/排除范围、最小复现、实施建议、依赖和验收，
Case 文档链接 task，只补本查询的证据与例外；研究和待补证事项另列于同一汇总。
匹配与默认排除的源端负向不另建 Case 文档；前提问题也逐条写明阻断，不编造候选。
对全部源成功差异进行调查或逐条说明具体阻断，不擅自挑选一部分代表全批。
生成 reports/attribution/aggregates-001-attribution-summary.md，
汇总数量、进度、每条报告链接与唯一当前 SQLGlot 任务清单；
已有清单时先判重：复用未完成 task、重新打开范围内遗漏，独立能力才新增编号。
任务与完整 Case 匹配分别说明，不为让单条查询通过而混入多个无关修复。
共同材料/环境与代码依据在本轮读取分析一次，按共同规则组织调查，再逐条核对例外。
同阶段候选优先通过 probe-pg-batch 批量只读对照，不跨阶段混用；
脚本事实/统计整合入对应 Case Markdown 和汇总，AI 负责代码归因、方案与限制。
不另建候选 SQL、执行 JSON、整批明细、独立任务清单或 evidence/ 目录。
不修代码、不改数据库数据、不自动进入步骤四。
~~~

Skill 直接读取各阶段验证 JSON 和显式提供的准备材料，不仅凭文件前缀猜数据已一致。单一状态批次只提供 aggregates-001-validation.json。多状态批次仍只生成一份批次汇总，并在逐条 Case 文档中注明实际 stage、YAML 和验证 JSON 路径。应有 Case 文档数等于各阶段非匹配且非源端负向的查询数之和，包含环境/输出读取阻断；每次出现保留原 Case ID。同一根因可合并为一个修复任务，但不丢不同数据阶段、类型或 Session 的例外。

### 6.1 只读对照命令与返回信息

归因是“Agent 分析 + 普通脚本真实执行”的组合，不是让 AI 凭文字猜结果。Skill 告诉 Agent 如何分析和取证；Agent 负责阅读代码、提出 Doris 候选及解释原因，probe-pg-batch / probe-pg-case 负责连接数据库并返回实际比较事实。它们不是 AI 调用接口，不生成候选，也不修改 SQLGlot；人可以手动执行，Agent 也可以在授权范围内调用同一命令或其 Python 函数。

~~~text
步骤二的 run
  社区 SQLGlot 生成的 Doris SQL vs 原 .out
  → 发现差异，保存首轮验证 JSON

步骤三的归因
  Agent 读取首轮事实、准备材料及代码，提出独立 Doris 候选
  → 同阶段候选通过 probe-pg-batch（单条也可 probe-pg-case）实际执行并返回比较结果
  → Agent 据实际结果继续分析/调整候选，将原因和证据写入 Case Markdown
  → 同根因归并到批次汇总的修复任务索引

独立候选匹配：说明当前样本存在可行改写线索，仍需核对类型、顺序及边界。
独立候选不匹配：继续调查，不能仅凭一次失败断言 Doris 不支持。
没有执行证据：写未执行或证据不足，不能由 AI 编造“已匹配”。
~~~

下面是取证工具的调用方法，不是用户在步骤二之后必须额外运行的固定阶段，也不表示已经执行了示例 SQL。多条候选优先在同一实际阶段批量传入，不要求候选文件：

~~~bash
.venv/bin/doris-sql-validator probe-pg-batch \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --report reports/validation/aggregates-001-stage-01-validation.json \
  --candidates-json - --output-format markdown <<'JSON'
[
  {"case_id": "<该阶段第一个待调查 Case ID>", "candidate_sql": "<完整只读 Doris 候选 SQL>"},
  {"case_id": "<该阶段另一个待调查 Case ID>", "candidate_sql": "<完整只读 Doris 候选 SQL>"}
]
JSON
~~~

将占位符替换为真实编号/SQL，使用标准 JSON 字符串转义。每条请求只支持 case_id、candidate_sql 和可选 source_variant_sql；后者表示新的 PostgreSQL 边界变体，不使用原 .out。同一 Case 可以多次请求，工具按输入顺序返回请求序号，不将它们当不同原查询。两份路径必须是同一阶段；不同阶段分别调用，不能在请求中覆盖数据库或 Session。

批量入口一次加载并核对 YAML/首轮报告，按需读取一次 .out，逐条安全检查、执行、比较并重复执行；不缓存数据库结果、不合并 SQL、不引入连接池。输入/只读检查/输出读取失败的请求不连接数据库；执行或比较中的工具异常保留已采集事实并继续下一条，数据库错误保留实际原文。一条请求失败不阻断整批。

默认 --output-format json 返回共同输入、批次统计和逐条结构化事实；markdown 返回相同事实整理出的中文表格、SQL、类型、错误和有限反例，便于整合进既有归因/修复 Markdown，不额外落盘。脚本只整理事实，不生成原因或修复任务。共同规则集中分析一次，仍逐条检查类型/参数/NULL/排序及阶段例外；不同 Case 不共用执行结论。

统计按“请求”计，包括重试与边界；完成、未执行、工具失败互斥。源/候选执行失败、行值差异、类型不同或证据不足、顺序差异等观察可能重叠，不能相加作 Case 数或根因数。跨阶段汇总不同 Case 时核对原 Case ID，不能直接相加每次调用的不同编号数。

退出 0 表示所有请求完成工具处理，不保证数据库成功、结果一致或归因完成；存在未执行/工具处理失败时返回 1，仍输出整批事实；共同材料不对应、JSON 数组格式错误或参数错误返回 2，不执行整批。具体差异仍须读逐条结果。批量入口和单条入口的比较标准、超时与结果上限一致。

单条调查仍可直接传 SQL 文本：

~~~bash
review_case_id='<从本次报告复制待归因 Case ID>'

.venv/bin/doris-sql-validator probe-pg-case \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --report reports/validation/aggregates-001-stage-01-validation.json \
  --case-id "$review_case_id" \
  --candidate-sql 'SELECT 5 DIV 2 AS value'
~~~

这里的 stage-01 只是路径示例，必须将 --path 和 --report 一起替换为待调查 Case 所属阶段，不跨阶段引用。候选较长或含特殊字符时可使用 --candidate-sql - 从标准输入读取；不写临时 SQL 文件。上面的 SQL 只是参数用法示例，必须替换为当前 Case 的真实候选，不能拿它验证任意查询。边界源变体直接使用 --source-variant-sql '<完整 PostgreSQL SQL>'，不借用原 .out。

~~~text
两种对照入口的普通脚本职责
  检查 YAML/验证报告/源 SQL 对应关系，不核验 .out 指纹
  → 在任何查询前检查源 SQL、社区 SQL 和候选均为单条只读查询，拒绝写入/加锁
  → 原查询时读取 .out 参考；明确源变体时不用原参考输出
  → 实际执行 PG、已保存的社区 Doris SQL（存在时）、独立候选及重复执行
  → 在内存比较实际取得的完整有限结果，不因类型不同而跳过行值
  → 只向终端返回结构化执行事实，不创建目录或写任何文件。

返回内容
  查询 ID、执行时间、实际 SQL、版本与会话、具体错误、字段类型、真实行数，
  分维度比较、每次结果最多三行样本，以及实际行值/重复次数/顺序的有限反例。
  它不是生成的 JSON 文档，不自动作根因判断；Agent 将必要事实整理到本 Case Markdown。
~~~

比较范围和展示范围不同：工具在每次成功取得的完整有限结果上比较，再限制终端样本；默认单次最多采集 10,000 行，超过上限明确报证据不足，不拿截断结果冒充完整结果。需要更多细节时可以在已授权只读范围内补查，将具体 SQL/命令与事实仍写入该 Case 文档，不强制保存完整大结果。

单条工具返回 0 也只表示此次对照调用完成，不表示候选全部等价或 SQLGlot 缺口已确认；看返回中的具体执行/类型/值/顺序维度。匹配与负向的精简首轮记录没有历史 target_sql，不重建冒充旧输出；源 SQL 不能被工具安全解析时明确阻断，不把它推定成非法源 SQL。

原 .out 与实时 PG 的状态/结果关系需要在报告中核对；工具未自动证明两者完整一致。二者不同应先检查数据阶段、Session 和版本，不无声更换源基线。缺表、权限、输出读取异常等前提未满足时不强行改写；源端负向默认不为复制 PG 报错进入主修复范围。

### 6.2 两类 Markdown 的内容与用途

~~~text
reports/attribution/
├── aggregates-001-attribution-summary.md      由人显式调用归因 Skill 后的 Agent 编写
│   内容：输入/版本/共同环境、首轮统计、应有/已生成逐条报告数、实际调查和对照范围；
│         逐 Case 导航、原因汇总、当前任务索引、待补证事项、后续轮次和整份输入状态。
│         开头先说明原脚本的测试侧重、查询出现数/重复口径、数据阶段数及文件数量，
│         列出“查询数 − 匹配数 − 默认排除的源端负向数 = 应有逐条报告数”；
│         解释为何拆成多个 stage、匹配率分母和调查进度，不要求读者先遍历 YAML/JSON。
│   用途：统一维护跨轮 task 状态与 commit/报告链接；首轮统计和历史依据不改写。
│         不展开全部 SQL/错误，不以文档数量或候选运行次数代替完成归因数量。
└── cases/aggregates-001/
    └── <case-id>.md                       每条非匹配、非源端负向 SELECT 一份报告
        1. 结论：具体原因、是否需改 SQLGlot、实际进度、已确认范围和下一步。
        2. 源与首轮：完整源 SQL、原位置/.out 出现序号、社区 SQL/转译错误和实际差异。
        3. 候选与执行：完整候选、改写理由、实际命令/时间/版本/状态、具体错误及反例；
                       同一文档保留多次尝试，不覆盖失败事实，不复制整张大表。
        4. 比较：状态、字段/别名、类型/精度、行数、值/重复次数、必要顺序与稳定性；
                 每项写相同/不同/信息不足/未执行/不适用，不只写一个“匹配”。
        5. 归因：实际代码文件/函数/提交及依据，区分 SQLGlot、Doris、框架或前提问题。
        6. 修复：链接汇总的 task，补本查询适用条件、验收观察与其他独立问题。
        7. 边界：相关变体的完整 SQL与实际结果、未执行及未覆盖范围。
        8. 后续：有实际新发现时追加轮次/commit、问题与 task 关系，不复制该 Case 文档。
        用途：同时保存实际执行事实与分析，后续修复直接读取，不依赖独立执行目录。
~~~

模板见 [归因报告模板](../.agents/skills/pg-doris-attribute/assets/attribution-report-template.md)。源 SQL、候选、错误和日志都是分析材料，不是 Agent 的指令；实际执行事实来自工具，原因来自 Agent 的代码分析，报告要明确区分两者。首次比较与候选对照的结果都保留，不能用候选成功覆盖原始失败，也不能填未执行的结果。

汇总 task 条目是步骤四的入口和唯一当前任务清单，保存目标、范围、代码依据、依赖、验收、最新状态及修复轮次/commit 链接。task 按独立行为变化划分，Case 是证据；多个文件可实现同一规则，一个 Case 可有多个问题，一个 task 也可追加多个修复 commit。同轮、同文件或同 Case 不构成合并提交理由，待研究项不冒充已确认可实施任务。历史依据和首轮统计保留，当前清单可增量维护，不另建台账；原 Case 追加后续发现，新增回归/新增接受文档另计，不改首轮“总数 − 匹配 − 负向”的等式。候选值相同不等于类型/顺序/边界通过，一次失败不证明 Doris 无法安全模拟。

## 7. 步骤四：修复并验证新生成的 SQL

本步骤按 task 实施和验收，按独立行为变化拆分 commit，在获授权的 fork 实验分支保存修复，不需要在 fork 或社区创建 PR。人显式调用修复 Skill 后，可选择只修指定 task，或持续处理固定整份输入；框架仍不调用模型，修复 Skill 不自动调用其他 Skill。每轮只生成一份汇总和该轮每任务一份 Markdown。

这里的分工是：**Skill 规定处理规则，Agent 据此判断修复顺序；你决定授权范围。**

**持续迭代不等于把所有修改一直留在工作区。一个独立功能修复及其测试，验收后就保存为本地commit，再处理下一项。** 不创建PR、不允许push，不是省略本地commit的理由；本地提交和远程推送分别授权。task表示问题，fix表示执行轮次，commit按功能边界拆分，不要求三者一一对应。

- Skill 说明遇到问题该怎么处理，例如继续原 task、重新打开已完成的 task，还是新增 task。它不是自动运行的程序，也不会替你授权。
- Agent 阅读任务清单、代码和实际执行结果，判断下一项应该修什么，并说明理由；不是机械地按 task 编号依次修复。
- 你决定这次只修哪些 task，还是持续修完整份输入，以及是否允许 commit、push。Agent 只能在你允许的范围内继续。

### 7.1 执行模式与授权

指定任务模式适合单项试修：只修你选定的 task。发现其他问题时，Agent 把它关联到已有任务或新增到清单，并告诉你，但不会直接开始修。即使你允许处理全部已有 task，也不代表允许继续修后来发现的新任务。没有说清范围时，Agent 先向你确认。

~~~text
使用 $pg-doris-fix。
批次：aggregates-001；修复批次：fix-001。
任务入口：reports/attribution/aggregates-001-attribution-summary.md。
模式：指定任务；task-id：<明确的 task 列表>。
目标 checkout：<本地 fork checkout 路径>；本地分支：<实验分支>。
允许修改对应 SQLGlot 代码和测试，并执行必要的只读数据库回归。
允许将每项独立行为修复及相关测试保存为本地commit，测试并核对实际提交内容后再继续下一项。
本次不授权push，不创建社区Issue/PR，不修未选的新任务。
按任务报告实际验收与整批剩余范围，不能把所选任务完成写成整份输入完成。
~~~

整份输入持续修复模式允许在固定范围内反复归因、维护任务清单和修复，不必每次暴露问题都重新人工调用步骤三；仍需先取得可安全实施的证据。以下示例允许按功能本地commit、暂不push，需替换实际fork和实验分支后再使用：

~~~text
使用 $pg-doris-fix。
批次：aggregates-001；起始修复轮次：fix-001，已有后续轮次时从最新状态继续。
模式：整份输入持续修复，范围为原 aggregates.sql 和配对 .out 的全部源成功只读查询，
包含所有准备阶段、Parser 拒绝和重新导入后新增接受的查询；源端负向默认排除。
任务入口：reports/attribution/aggregates-001-attribution-summary.md。
目标 checkout：<本地 fork checkout 路径>。
授权 fork：https://github.com/<fork-owner>/sqlglot.git；实验分支：codex/pg-doris-aggregates。
允许在该 checkout 修改 SQLGlot 及测试；每个独立行为修复及相关测试单独 commit，
本次不授权push，不更新main，不向社区提交Issue/PR；远程推送以后单独授权。
先读取既有 task、全部相关 Case/阶段材料和历轮修复；共同依据复用但逐条例外保留。
开始每项修复前在原task条目补齐具体反例、拟改规则、范围、验收和提交依赖。
每项独立修复验收后实际本地commit、记录修复SHA；未提交原因未解决前不叠加下一独立功能。
用修改后的 SQLGlot 从原源 SQL 重新生成 Doris SQL、执行并验收；
保持原 SQL/.out、数据条件和比较规则不变，不用手写候选代替修复验证。
每轮检查剩余差异和新增回归：同根因复用 task，已验收范围内遗漏重新打开，
独立能力新增 task；增量补证在本 Skill 内完成，不自动调用另一个 Skill。
继续至全部可由 SQLGlot 安全修复的问题完成验收，并在最终代码版本完成全阶段回归；
仍不确定可修复性、前提阻断或有未调查项时不得宣布整份输入完成。
回归默认 run --stdout，同阶段批量执行，保留逐条实际生成 SQL、类型、错误与反例。
每轮仅生成 reports/fixes/aggregates-001-<fix-batch>-summary.md 和
reports/fixes/tasks/aggregates-001/<fix-batch>/<task-id>.md；
更新归因汇总当前 task 清单，在原 Case 文档追加后续发现，不改写首轮/前轮事实。
不增加交接、台账、候选、执行 JSON、日志、patch 或额外报告。
不修改验证框架、不建表装数或更改 Session 政策；需扩大权限时停止相关任务请求确认。
无法安全推进或反复尝试不再增加有效证据时报告未完成范围和恢复条件，不无限重试。
~~~

commit 与 push 可以分别授权；仅允许 commit 时不得自动推送。上述授权仅在实际调用时生效，阅读/修改文档不代表现在执行。一次持续调用可以处理多轮，也可由人后续显式从 fix-002 等恢复；目标仓库/分支或输入范围改变需要新授权，不默认接管其他数据库或文件。

如果只想试代码而不commit，应明确指定“未提交试验”及范围；Agent尊重该选择，但不能默认为后续所有功能都不提交。开始修复前缺少提交权限说明时先确认，而不是连续多轮只在报告中写“未commit”。

### 7.2 跨轮任务维护与提交边界

每次修复并测试后，Agent 都要检查还剩什么问题，再决定下一步：本次修改把原来正确的查询改坏了，优先修这个回归；当前任务承诺解决的问题还没修完整，就继续原任务；另一个任务是后续修复的前提，就先处理前置任务。其他独立问题根据实际证据和阻断程度安排，不要求按编号顺序执行。若下一项超出你的授权范围，Agent 只说明建议，不直接实施。

fix-001、fix-002 是执行轮次，由人或 Agent 检查未占用后递增，不是 CLI 自动编号，也不是新一份源输入。恢复时读取最新 Summary 和当前分支，不从起始版本覆盖已有修复；同 task 跨轮保持编号，每轮处理时在该轮路径保存报告。

每次进入下一项修复前，先在归因汇总的原task条目写清楚“具体错在哪里、准备怎么改、哪些不改、如何验收、依赖哪个commit”。已经解决的范围、未验收部分和下一步计划分开写；不另建任务清单，也不只留“继续task-001”这样的标题。

修复的是源SQL的语义规则，不是让某份测试文件不报错。先说明源语义依据、适用的类型和上下文、目标能力限制，再决定改代码；源Parser只描述源方言，Doris如何转换由目标生成侧处理。针对某个Doris版本的文本中转、lambda等补偿，要单独说明必要性、适用条件和未验证范围，不能只凭样本值相同就称通用支持。测试既检查具体结果，也检查转换顺序、NULL、类型及必要组合上下文；不要求一次支持全部语法，但不能悄悄给源类型增加约束。

继续已有task时，优先审查此前补丁的语义错误和职责耦合，再扩展能力。汇总分别写已实现规则、补偿待审查和研究阻断；旧反例只复测而未解决，就明确写“无新增实现”，不反复作为下一轮已确定可修复的目标。

~~~text
读取统一 task 清单和当前代码
  → 补齐具体方案、功能提交边界和前置commit，确认本地commit权限
  → 实施一项独立修复，补测试和受影响回归
  → 核对准确提交内容，实际本地commit，记录修复SHA
  → 检查剩余差异、原匹配查询和新增接受范围
  → 同根因继续原 task；范围内遗漏重新打开；独立能力新增 task
  → 更新本轮报告与清单；push仅另按授权
  → 继续下一轮，直到满足第 7.5 节，或明确阻断并交付未完成范围
~~~

判重依据是规则、代码路径及语义契约，不是同文 SQL、函数名或错误文本。同一 Case 可先因数组构造失败，修复后暴露已有聚合 task 的问题：复用聚合 task，数组 task 不因其他问题自动失败；若数组规则承诺范围本身仍有反例，则重新打开数组 task。新引入回归优先定位引入 commit，不能伪称原有 Doris 限制。

归因汇总的 task 索引是唯一当前清单，更新当前状态、关联 Case、最新轮次/commit/任务报告链接，在原条目追加变更依据；首轮统计、原归因、首轮 JSON 和前轮执行事实不改写。原 Case 追加后续章节，不按轮次复制；原匹配查询出现回归或新增接受查询需要调查时才增加此前没有的 Case 文档，另列覆盖变化，不修改首轮分母。

一组清楚的行为修复连同相关测试默认作为一个 commit；多文件可共同实现该规则，同 task 补遗漏可以再提交，多个 task 真正不可分割才共用提交并说明理由。同一轮、同文件或同 Case 都不能作为混合提交理由。每次提交前测试并检查 diff，排除用户和未验收的无关改动；不重写已发布历史，不自动 amend/squash/rebase/强推。实验未验收代码需要相应授权并明确标记，不算已修复。推送前核对目标 fork/实验分支及相对远程的全部待推送提交，不夹带无关本地历史；不推 upstream 或擅自更新 fork main。

#### 本地提交的检查要求

- 一项task可以有多个功能commit，例如数组构造输出、源元素类型保留、整数/布尔文本输入、浮点文本输入；一次fix也可以包含多个独立commit。同一行为的调试尝试不要求次次提交。
- 有本地commit授权且该行为通过约定验收，就在进入下一独立行为前实际提交。没有权限先确认；测试失败或无法可靠拆分则说明阻断，不能继续把其他功能堆入工作区。
- 检查暂存diff，确保“父commit + 本次提交”本身代码和测试可运行。只在包含其他未提交修复的工作区测试通过，不证明这次独立提交正确。同文件交叉改动难以验证时，获授权后在独立checkout测试准确的拟提交状态，不直接整文件git add。
- 每项实际提交在已有任务报告/归因清单记录完整修复SHA、父commit、行为与配套测试、验收或实验状态、是否push。起始社区SHA与修复SHA分开；报告写好不是commit已经生成。
- 提交后检查剩余diff及其归属，再开展下一项。未验收代码需按明确授权保存为实验commit，不能因此将整个task标完成；不得自动丢弃失败尝试。

#### 已有混合未提交改动的补救

暂停新功能，先只读梳理基线、最终改动、任务归属和依赖；保留原checkout不动。获得重建授权后，从同一基线建立单独分支/checkout，按功能依赖顺序逐项重建实现和配套测试，每个准确提交状态独立验证后commit。不是整包提交，也不是按文件拆分；同一文件内的多个功能仍需分开。

没有逐轮源码快照时，旧报告只能辅助恢复修复目标，不能声称重现每一轮精确补丁。补救产生的是现在新建的功能提交，不伪造旧日期/SHA。最后将重建分支HEAD的跟踪文件与原最终内容逐一比较、执行最终相关回归；有差异先解释，不覆盖原文件。提交对应关系追加到已有归因/修复报告，不改历史“未提交”事实、不新增台账或混合总commit。原checkout切换、清理和push另按授权。

### 7.3 修复后实际执行

先确认运行时导入的就是修改后的 checkout：

~~~bash
.venv/bin/python -c 'import sys, sqlglot; print(sys.executable); print(sqlglot.__file__); print(sqlglot.__version__)'

.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --stdout
~~~

run --stdout 仍执行这份阶段 YAML 内的转译、Doris 查询和 .out 比较，只是不写文件。每个阶段在一个进程中运行选定查询，需要筛选时重复传 --id，而不是每条另起进程。其他受影响阶段分别运行各自 YAML，在同一份修复批次汇总中记录实际范围，不将第一阶段通过视为整批通过。终端返回的 JSON 与步骤二文件版使用相同的 run / summary / queries 结构；没有额外“JSON: 路径”输出。不能同时传 --output。全部比较匹配返回 0；差异、失败或源端负向等仍可能返回 1，JSON 仍可读，不把退出码当作某个修复任务的验收结论。输入/配置错误返回的诊断不保证是报告 JSON。

已有 Case 使用原 YAML，可用 --id 指定 Case 并记录范围；还要重跑相关既有成功查询。Importer 的 Parser 修复需从同一份原 SQL/.out 重新生成 reports/data-preparation/aggregates-001-fix-001-cases.yaml，再按原语句位置/SQL 对应新旧 Case，单列新增接受范围；不改旧 YAML、不混算匹配率。原本全部导入失败时引用真实错误，不伪造修复前报告。

多状态的重新导入同样必须按原准备依据划分为 aggregates-001-fix-001-stage-01-cases.yaml 等阶段输入，再执行对应阶段；整份新导入结果只是中间材料，不能直接在单库执行，也不能仅按旧 Case ID 丢弃新接受的查询。阶段状态无法覆盖新增查询时先补准备条件并记录限制。

精简匹配记录没有新生成 SQL或完整原生类型，不能据此声称这些维度通过。需要时由修复 Agent 在同一修改后环境调用 ValidationService.run_suite，读取内存 CaseRunReport 的 target_sql、source_evidence 和 target_result；或用 SqlglotTranspiler.transpile_case 真正转译，再通过 pg_probe.execute_query / compare_probe 补充双端类型、完整有限记录和必要重复执行。Python 调用须加载项目 .env 并使用 YAML 中同一数据库；实际命令/API、生成 SQL和观察值直接整理进任务 Markdown，不要求落盘 JSON或新建脚本。

首轮 .out 是主参考；实时 PG 与它不同先查数据阶段/Session/版本，不能无声换基线。旧首轮报告内的 target_sql 是旧生成结果，probe-pg-case --report 指向旧报告不会验证修复后的生成器。边界也必须从对应 PG 变体经修改后 SQLGlot 生成再执行，不能只跑步骤三手写候选。

实时补证可在一个 Python 进程内批量转译并调用 probe_postgres_cases，或把实际生成 SQL交给同阶段 probe-pg-batch。先证明新进程导入的是修改后 checkout，再保留实际生成调用；批量工具的旧社区重放字段不能代替本轮生成结果。使用终端返回的事实片段填入同一任务报告，AI 补实现依据和验收判断，不重复抄写统计或新建执行文件。共用边界/测试记录一次并注明适用范围，每条关联原查询仍保留自己的结果及例外，不减少必要复测。

### 7.4 本步骤产物及内容

~~~text
<本地 fork checkout>/                        获授权修改的独立 checkout，与运行时 import 对应
  sqlglot/... / tests/...                    实际转换代码和回归测试，不复制为报告中的 patch 文件

reports/fixes/
├── aggregates-001-fix-001-summary.md            批次汇总，由显式调用修复 Skill 的 Agent 编写
│   内容：模式/授权、起止代码版本、当前任务状态、commit/依赖/推送状态、实际回归；
│         新增/复用/重新打开项、全批剩余差异、最终完成检查或下一轮入口。
│   用途：区分本轮任务完成与整份输入完成，不重复全部 SQL与执行结果。
└── tasks/aggregates-001/fix-001/
    └── <task-id>.md                         每个选定修复任务一份，合并实施与回归
        1. 结论：task 状态、原条目/Case/前轮报告链接、验收范围、未满足项。
        2. 修改：独立行为、最小复现、实际文件/函数、关键 diff、真实 commit/依赖。
        3. 执行：修复前后实际生成 SQL/错误、命令/API/时间、数据库与数据阶段；
                 执行状态、字段/别名、类型/精度、行数、值/重复次数、必要顺序。
        4. 测试：新增测试、相关边界、真实命令/通过失败数量、具体错误和未覆盖项。
        5. 验收：任务与整条 Case 结果分别说明，后续问题的归并、新回归及下一轮要求。
        用途：直接审查本任务改了什么、是否真的修好，不依赖独立执行文件。
~~~

模板见 [修复报告模板](../.agents/skills/pg-doris-fix/assets/fix-report-template.md)。真实事实、SQL和必要错误/反例写入任务文档，共同环境放汇总。每轮实际纳入任务一份报告，同轮后续尝试追加，下一轮写到 fix-002 等路径并链接前轮；不创建空白下一轮文件。归因当前任务清单增量维护、Case 追加后续发现，历史事实不可被最终结果覆盖。

当前状态统一为“已修复并完成约定验收 / 已修改但未完成验收 / 重新打开 / 当前阻断 / 未处理 / 不需修改”。最后一种须写明当前版本已覆盖或归因更正的依据；不能借此排除未知问题。每个 task 在轮次结束只计一种，本轮合计等于实际纳入数，全批按唯一 task-id 去重。新增/复用/重新打开/完成事件可重叠，不相加当任务总数；打开后再完成仍保留打开事件。类型、顺序或约定边界仍有反例则不能验收，当前样本通过也不表示全部输入同义。

默认不生成 implementation-report.md、regression-report.md、before/after/、evidence/、候选 SQL、测试日志或 patch 文件。测试命令、结果数量和具体错误写进任务 Markdown，实际代码/测试留在 SQLGlot checkout。只有明确需要 CI/统计导出时才额外用 run --output 指定新 JSON路径；它不是后续审查的必需输入，不覆盖首轮报告。

源端负向默认不承担全部错误复刻，仅对直接相关或明确授权专项补边界。未执行、缺依赖、超时或失败不写成通过；记录真实 fork commit 链接与 push 状态，保存代码不等于验收。社区 Issue/PR 不属于本流程默认产物，需要另外授权并遵守社区贡献政策。

### 7.5 整份输入完成条件

每轮 Summary 必须写“整份输入已完成”或“整份输入未完成”及依据，不能仅写 fix-001 已完成。指定任务模式可写“所选任务完成，整份输入未验收”。整份完成需同时满足：

1. 固定原脚本中纳入的源成功只读查询全部有去向，含全部 stage、导入诊断/Parser 拒绝和重新导入新增接受项，无遗漏或未调查记录。
2. 所有确认能由 SQLGlot 安全修复的任务均已验收或实测由当前版本覆盖，无未处理、未验收、重新打开或仍不确定是否可修复的遗留项。
3. 最终同一 checkout/commit 下，对原输入/阶段/比较规则完成全阶段回归，含原匹配与新增接受查询，无引入的未解决回归；必要原生类型、顺序和有限边界具备实测证据。
4. 剩余不匹配逐条有不能仅靠安全 SQLGlot 修改解决的具体依据和外部去向；一次候选失败不等于 Doris 无法模拟。缺连接、源证据或关键元数据导致无法判断时，不得宣布整份完成。
5. 源端负向默认单列排除，不改源 SQL/.out、数据或比较规则制造通过；完成针对固定范围与约定证据，不要求 100% MATCH，也不证明所有可能 PostgreSQL 输入同义。

未完成时在已有 Summary 列下一轮 task/补证范围、当前起始 commit、最近修复报告和实际阶段材料入口，不增加台账。需扩大权限、存在用户修改冲突、关键前提阻断或反复尝试不再增加有效证据而无法安全推进时，停止相关任务并说明恢复条件；这属于未完成，不是为了达到结束条件而删去问题，也不无限重试。

## 8. 复用官方回归样本

从 PostgreSQL 官方仓库取得同一提交的 src/test/regress/sql/ 与 src/test/regress/expected/ 配对文件，保留版本、许可、COPY 依赖和数据阶段信息。它们不保证可在空库直接执行，也不保证整个脚本读取同一个数据状态。

所有报告均受所记录版本、数据、Session 和类型域限制；成功匹配不代表全部 SELECT 语法覆盖或对所有输入完全等价。
