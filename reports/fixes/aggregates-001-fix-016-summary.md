# aggregates-001 / fix-016：数组输入转换的连续修复

## 1. 本轮结论

继续原 task-001，在同一次授权中完成四项独立规则的实现、双端核验和本地提交，没有在第一项通过后停止。**四项限定规则通过本轮验收，但 task-001 仍有未解决范围，整份输入未完成。** 未修改框架、比较器、SQL/.out、YAML 或数据库数据；未 push、创建 Issue 或 PR。

| 本轮独立修复 | 本地 commit | 验证范围 |
| :--- | :--- | :--- |
| 无 FROM 的有限标量投影中，保留 REAL 转换后再提升的顺序 | `6e92c3f330ea17d6458baf656c7731012dfec95b` | 13 条成功源查询，含别名、NULL、嵌套、舍入边界及外层数组 CAST |
| 十六进制浮点输入先精确转换为源 FLOAT/DOUBLE 值 | `be74c6b42e63d129d6aa116bab90bac46abc6394` | 24 条，含中点、最大值、次正规数、符号和已有 CAST |
| 接受 PG 合法的 NaN/Inf/Infinity 数组输入 | `9c3b30efc6aedaf54c3327d44f4ca231d39e3d97` | 16 条，核验非有限类别、Infinity 符号、NULL 和重复位置 |
| 显式 DOUBLE→REAL 运行时 CAST 不被数组共同类型提升吞掉 | `ce841540a49228d9114a0346abc84283abcbe4c2` | 36 条单行变体，另补 1 条四行、重复值及稳定 ORDER BY 查询 |
| 非有限拼写保护补漏（不是第五项新功能） | `6922457c6d223eafb1e3e7c1aaab211f88487874` | 增加 ASCII 限制，避免把 PG 拒绝的 `İnf`/`ınf` 当作 Infinity；两条均实测 SQLSTATE 22P02，默认排除归因 |

详细实现、实际 SQL、逐项结果和余项见 [task-001 报告](tasks/aggregates-001/fix-016/task-001.md)。任务数为 1、规则为 4、保存 commit 数为 5（含非有限输入保护的补漏），不能计作完成了 4 个 task。

| 本轮互斥任务状态 | 数量 |
| :--- | ---: |
| 已修复并完成约定验收 | 0 |
| 已修改但未完成验收 | 1 |
| 重新打开 / 当前阻断 / 未处理 / 不需修改 | 各 0 |

复用 task-001，未新增或重新打开其他 task。全批仍为 9 项：7 项已完成各自约定验收，task-001/003 两项未完成。

## 2. 代码与环境

| 项目 | 实际情况 |
| :--- | :--- |
| checkout / 分支 | `../sqlglot-functional-commits` / `codex/doris-functional-commits` |
| 起点 → 最终 HEAD | `365986d92f426fa6c837d3fc60ba6a41acd0770c` → `6922457c6d223eafb1e3e7c1aaab211f88487874` |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；未刷新远端 main，未推送 |
| 改动 | `sqlglot/generators/doris.py`、`tests/dialects/test_doris.py`，262 行增加、19 行删除 |
| 本轮二进制 diff SHA256 | `a4db7ecef627f1b6ce6a205fae74ec56be5b80ff4a1c5715e0f4d84a24f6ce06` |
| 最终 Git tree | `311d79fe42df7939dd79e958c081d4538cd91fd7` |
| 实际 SQLGlot 导入 | `../sqlglot-functional-commits/sqlglot/__init__.py` |
| 解释器 | 单测用 `../sqlglot-experiment/.venv/bin/python`；数据库用 `../doris-sql-validator/.venv/bin/python`；均显式设置 PYTHONPATH 指向本轮 checkout |
| 版本字符串 | 单测环境 `30.25.1.dev355`，数据库环境 `30.25.1.dev6`，沿用旧安装元数据；以实际导入路径与完整 SHA 识别源码，不靠安装版本字符串猜测 |
| 数据库 | PostgreSQL 18.1：127.0.0.1:5432；Doris `doris-4.1.3-rc02-7126cf65d96`：127.0.0.1:9030；FE Alive=true |
| Session | UTC；PG `DateStyle=ISO, MDY`、`extra_float_digits=0`；Doris `enable_strict_cast=false`、`enable_decimal256=false`，本轮未改变这些策略 |
| 输入与阶段 | 原 `aggregates.sql/.out`，原 stage-01–43 YAML 及 `dsv_wf_agg001_s01`–`s43`；无新快照或数据装载 |

原输入位置和准备材料见 [归因汇总输入节](../attribution/aggregates-001-attribution-summary.md#inputs)；首轮 JSON 保持不变。本轮只用 `run --stdout` 取得回归结果，不另存验证 JSON。

原 `sqlglot-experiment` 未清理或修改：其 dirty diff 指纹仍为 `32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73`。社区 checkout 的跟踪文件未修改。每项提交前在不含后一项的准确代码状态下测试，提交后核对工作区干净；五个提交均只包含对应行为及测试。该分支相对起始社区基线现共 18 个本地功能提交，均未 push。

## 3. 实际回归

### 3.1 本轮新边界与既有边界

| 范围 | 实际结果 | 不能据此声称的结论 |
| :--- | :--- | :--- |
| 新增 89 条成功源变体 | 89 条二进制源值与目标原生元素核验通过，FLOAT32/64 及嵌套维度可核对，重复执行稳定 | 主比较器仅 37 条行值一致；51 条显示差异、1 条源文本驱动解码失败仍保留，不能写 89 MATCH |
| 新增四行 ORDER BY 查询 | 每行元素原生等值、NULL、重复次数和 id 顺序通过，重复稳定 | 不证明任意非唯一排序或全部 CAST 输入域等价 |
| 既有 185 条：37+60+41+47 | 两端查询成功且重复稳定；178 条单行数组原生核验通过，其余 7 条多行/SQL NULL 查询另补原生计数和必要 id 顺序核验通过 | 原比较器仍为 125 一致、59 不同、1 无行值结论；独立 id 位宽和 Decimal 声明等既有类型余项不因此消失 |

原生核验是补证，不替换原比较规则。NaN 用 `ISNAN` 判断类别，Infinity 用 `ISINF` 与符号判断；不以 NaN=NaN 或显示字符串相同作证明，也未验证 NaN payload、符号位或有符号零的位级一致性。

### 3.2 原输入扩展回归

实际在最终 HEAD、原 .out 与各自数据阶段运行 **310 条 / 43 阶段**。排除已记录有后端风险的 Case 0301、0303、0304，故不是全部 313 条最终验收。

| 框架直接记录的结果 | 数量 | 解读 |
| :--- | ---: | :--- |
| 匹配 | 82 | 可用 Recorded Output 比较通过，不等于原生类型契约全部验证 |
| 源端负向用例 | 25 | .out 记录源端报错，默认不进入归因/修复主清单 |
| 行值或顺序不匹配 | 64 | 观察到差异，尚不能只凭该标签确定 SQLGlot 根因 |
| Doris 执行失败 | 119 | 保留实际错误；本轮没有实施这些独立函数、聚合等能力 |
| Doris 环境问题 | 12 | 框架粗分类，不是 12 条都已经归因为装数问题，见下文 |
| SQLGlot 转译失败 | 8 | 包括 Parser/Generator 拒绝；源成功不能因此标负向 |
| 合计 | 310 | 其中源成功 285 条，82/285 的可用证据匹配率约 28.77% |

对可解析原查询，使用 `git show` 只读加载本轮起点的 Doris Generator，与最终生成结果逐条比较，**生成 SQL/生成错误没有变化**；Parser 本轮未修改。此核对不等于在起点重新执行了 310 条 SQL，也不冒称旧 142 条逐 ID 运行结果已重新对比。82 匹配数与历史相同不是新增修复提升。

task-001 原关联 14 条仍为：3 匹配、1 行值/显示差异、9 Doris 执行失败、1 排除范围内的 ARRAY 子查询构造转译拒绝。具体错误见任务报告。

12 条环境标签中，0012/0016 实际生成保留 `FROM ONLY student`，Doris 报 `Table [ONLY] does not exist`；PG AST 正确认出了 `only=True`。这是独立源修饰与目标生成行为问题，不能断言 student 缺数据。其余 10 条涉及 `t_opf`、`bytea_test_table` 缺表，需要独立前提核查。本轮未建表、删改 ONLY 或安排其他 task 的修复。

### 3.3 单元测试

| 准确代码状态 / 命令范围 | 结果 |
| :--- | :--- |
| 第一项提交前：Doris/PG/MySQL + expressions/generator/parser | 333 项通过；提交后 162 项定向通过 |
| 第二项提交前：同组 | 334 项通过；提交后 163 项定向通过 |
| 第三项提交前：同组 | 335 项通过 |
| 第四项提交前：同组 | 336 项通过 |
| 最终 HEAD：三方言 + expressions/generator/parser/transpile/tokens/build/schema/lineage | 443 项通过 |
| 最终 HEAD：全部方言 discovery | 1088 项通过 |
| Ruff check / format --check / git diff --check | 两个变动文件全部通过；最终工作区干净 |

443/1088 是 unittest 方法数且有重叠，不是新增 SQL 数量，不能相加。完整 optimizer、mypy、C 扩展及 `make check` 未运行，没有为此安装或升级依赖。

共同命令示例（在 SQLGlot checkout 下）：

```bash
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  ../sqlglot-experiment/.venv/bin/python -m unittest discover -s tests/dialects -p 'test_*.py'
```

首次全部方言测试的 lazy-load 子进程找不到 `python`；补齐 PATH 后原代码重跑通过。临时数据库核验初版还曾错误地固定输出别名为 xs，已按实际别名修正并完整重跑；这些是测试调用问题，不是 SQLGlot 修复。原输入回归的辅助基线比对曾被既有 Parser 错误中断，补齐异常处理后全部 43 阶段重跑完成，不能把中断那次当完整回归。

## 4. 未完成范围与继续条件

当前不能把整个 task-001 关闭：未知文本列直接→REAL 仍有真实舍入差异；一般列/参数缺少可信源类型时不能猜型；NUMERIC 的无约束域、非有限值和 Decimal 声明不能用任意 DOUBLE/固定 Decimal 冒充。有限十六进制的长度/指数保护也仍有明确限制。详见 [剩余问题与下一步](tasks/aggregates-001/fix-016/task-001.md#6-剩余问题与下一步)。

本轮没有因一次候选失败把这些问题判作“不可能修复”。直接 CAST 与 ARRAY_MAP 两条运行时文本路径都已有反例，且中点区分了直接 REAL 舍入与先 DOUBLE 后 REAL；因此停止套用同一候选。下一步需要先确定安全的运行时 FLOAT32 输入实现或明确可移植的类型/输入范围；若涉及改变 Doris、Schema 前提或结果表示契约，须另获授权，不能靠改变比较器继续制造通过。

整份输入完成检查仍不满足：所选任务有余项；另外 3 条风险查询未最终执行；其他 task 和前提/类型问题未全量关闭。已有四项本地修复可独立审查，**不以本轮结束或 commit 成功代替完成判断**。
