# aggregates-001 / fix-017：有限 NUMERIC 数组修复

## 1. 本轮结论

继续task-001，完成两项独立功能，分别保存本地commit，未push、创建Issue或PR。**task-001仍未完成，整份输入未完成。** 本轮不是修改验证器或比较规则；没有建表、装数、更改原SQL/.out或YAML。

| 本轮修复 | 完整本地commit | 验证范围 |
| :--- | :--- | :--- |
| 有限整数NUMERIC数组：大于INT64、最多76位、嵌套、显式整数CAST运行时有限域 | 3281a9848a342660b8b47a9145846d562db5fb35 | 32条构造/显式CAST控制；29条原生完整元素文本、2条显式TEXT/Decimal控制、1条DOUBLE追加原生等值 |
| 同Scale有限小数/科学计数法NUMERIC数组；精确Decimal与范围/Scale保护 | 4dc65a35a7efa92551cb9fb00c2315fcb8ff659f | 30条数组构造完整元素文本、Scale、类型与重复核验；另13条TEXT投影暴露独立下标问题，未通过 |

详细源SQL、实现、失败候选和限制见[task-001报告](tasks/aggregates-001/fix-017/task-001.md)。75条变体中前62条取得相应规则/控制证据，13条完整查询仍错误；不写成75条MATCH，也不把两个commit计为两个已完成task。

本轮实际实施任务1项，互斥状态为“已修改但未完成验收”1项，其余状态0。另将已有数组下标研究经实际执行补证登记为task-010，未实施、不计本轮实施任务。全批初轮9项加新登记1项，共10项：7项完成各自约定验收、task-001/003两项已修改未完成、task-010一项未实施；不改首轮313条/226份归因统计。

## 2. 代码、环境与权限

| 项目 | 实际情况 |
| :--- | :--- |
| 目标checkout / 分支 | ../sqlglot-functional-commits / codex/doris-functional-commits |
| 本轮起点 → 最终HEAD | 6922457c6d223eafb1e3e7c1aaab211f88487874 → 4dc65a35a7efa92551cb9fb00c2315fcb8ff659f |
| 两项依赖顺序 | 3281a9848a342660b8b47a9145846d562db5fb35的父commit为起点；4dc65a35a7efa92551cb9fb00c2315fcb8ff659f的父commit为3281a9848a342660b8b47a9145846d562db5fb35。每项有代码与测试，第一项提交后再开始第二项，未重写历史 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；本轮未刷新远端main、未push |
| 上游起始基线 | 089891f2521780e2c5b243005017af9db62f25a6；此前18个功能commit，本轮追加2个，当前共20个本地commit，均未推送 |
| 改动文件 | sqlglot/parsers/postgres.py、sqlglot/generators/doris.py、tests/dialects/test_postgres.py、tests/dialects/test_doris.py；相对本轮起点224行增加、5行删除 |
| 本轮binary diff SHA256 / 最终tree | aec4a1bcb83e3bc66979baa2221e54261d595cb962298e7b7f50f402d7c689d9 / 2d67bf2a19bfee80c26e812392473206e615e488 |
| 最终状态 | active checkout跟踪/未跟踪文件均干净；原sqlglot-experiment的dirty diff仍为32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73，未改；社区checkout跟踪文件未改 |
| 测试解释器 | ../sqlglot-experiment/.venv/bin/python；版本字符串30.25.1.dev355，显式PYTHONPATH/当前目录指向active checkout |
| 数据库解释器 | ../doris-sql-validator/.venv/bin/python；版本字符串30.25.1.dev6；实际导入../sqlglot-functional-commits/sqlglot/__init__.py，旧安装版本字符串不作为源码身份 |
| 数据库 | PostgreSQL18.1，127.0.0.1:5432；已有Doris单机环境127.0.0.1:9030，按对应源码提交7126cf65d96核对FLOAT实现。协议VERSION()返回5.7.99，不把它写成Doris产品版本 |
| 实际默认Session补查 | PG UTC、ISO MDY、extra_float_digits=0；Doris UTC、enable_strict_cast=false、enable_decimal256=false。本轮精确值批处理仅增加源只读及两端10秒超时，没有改这些类型策略 |
| 输入/数据阶段 | 原aggregates.sql/.out、原stage-01–43 YAML、dsv_wf_agg001_s01–s43；数值新边界用stage-01，真实表控制使用已有tenk1 |

准备材料、首轮JSON及原始输入见[统一归因汇总](../attribution/aggregates-001-attribution-summary.md#inputs)。.out原件不改、不新增指纹字段；没有产生输入副本、执行JSON、候选SQL、日志、patch或额外交接文档。

## 3. 测试与数据库回归

### 3.1 代码测试

从SQLGlot目标checkout运行，所有检查对应实际提交内容：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" \
../sqlglot-experiment/.venv/bin/python -m unittest discover -s tests/dialects

PYTHONDONTWRITEBYTECODE=1 \
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" \
../sqlglot-experiment/.venv/bin/python -m unittest \
  tests.dialects.test_doris tests.dialects.test_postgres \
  tests.test_expressions tests.test_parser tests.test_generator \
  tests.test_serde tests.test_transpile

../sqlglot-experiment/.venv/bin/ruff check \
  sqlglot/parsers/postgres.py sqlglot/generators/doris.py \
  tests/dialects/test_postgres.py tests/dialects/test_doris.py

../sqlglot-experiment/.venv/bin/ruff format --check \
  sqlglot/parsers/postgres.py sqlglot/generators/doris.py \
  tests/dialects/test_postgres.py tests/dialects/test_doris.py

git diff --check
~~~

第一项独立代码通过1089项方言、300项定向/核心；第二项最终代码通过1090项方言、301项定向/核心。两组有重叠，不相加当独立测试数。lint/format四文件通过，diff无空白错误。

曾有一次最后全方言命令漏加PATH，只有test_lazy_load子进程因找不到python报错；补上上面的PATH后，在最终commit重跑1090项通过。保留这次环境问题，不伪装成代码失败或省略失败事实。未运行全部优化器/mypy/C扩展/make check，不安装额外依赖。

### 3.2 新边界与既有边界

- 新增75条完整源查询实际运行，详见任务报告逐条表。62条构造/控制有各自验收证据，13条独立下标失败；原生补证不制造主框架MATCH。
- 最终代码重跑旧37+60+41+47+89=274条边界：273条双端成功并重复稳定；1条ARRAY[1.25,2]现在严格unsupported，避免NUMERIC混合Scale生成错误的固定Scale数组。原目标DOUBLE类型不等于源NUMERIC；仍须明确这是一条旧接受查询变为拒绝，不能写“274条无回退”。
- NaN重复核验按类别判断，不能使用NaN=NaN；初次原始Python比较给出14条“不稳定”，纠正这一核验方式后273条稳定。这是诊断脚本比较方式，不改正式框架。
- 上述旧边界读取采用PG二进制及完整结构补查；不把这些数值补证冒称与历轮文本驱动/主框架使用完全相同的比较方法。完整类型/顺序并未对所有可能输入域证明。
- 另有40次REAL手写路径可行性测试及3条真实表四行查询，证明直接文本REAL仍有未解决反例；不计NUMERIC修复通过数，具体输入、结果和源码依据见任务报告第5节。

### 3.3 原输入43阶段回归

从workflow项目根目录执行，先在进程中加载已有连接环境变量（凭据不写报告），显式指向active SQLGlot；每一阶段使用自己的YAML，安全范围内每条ID均纳入。加载连接环境后的等价CLI命令示例如下：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../sqlglot-functional-commits:src \
../doris-sql-validator/.venv/bin/python -m doris_sql_validator.cli run \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --stdout
~~~

上面展示stage-01；实际以CliRunner调用同一run入口，遍历stage-01–43并传入每阶段安全Case ID。没有生成新的验证文件。排除已记录有源后端风险的0301/0303/0304，共310条，而非全部313条最终验收。

| 主框架结果 | 第一项commit回归 | 最终commit回归 | 含义 |
| :--- | ---: | ---: | :--- |
| 匹配 | 82 | 82 | Recorded Output可用证据匹配；不是全部原生类型契约已证明 |
| 源端负向用例 | 25 | 25 | 默认不进入归因/修复主清单 |
| 行值或顺序不匹配 | 64 | 64 | 仍需按具体语义/表示及其他任务处理 |
| Doris执行失败 | 119 | 114 | 少5条是提前拒绝，不是执行修好了 |
| Doris环境问题 | 12 | 12 | 框架粗标签；原ONLY等已知语义解释沿用前轮，不全归为装数缺失 |
| SQLGlot转译失败 | 8 | 13 | 多5条为NUMERIC混合Scale保护 |
| 合计 | 310 | 310 | 源成功285，匹配率82/285=28.77%，未提升 |

有变化的5条是stage-31：0410、0411、0412、0413、0415，源都是PERCENTILE的数组参数与WITHIN GROUP查询。之前目标在WITHIN GROUP处失败，现在ARRAY混合Scale先触发unsupported；函数参数的源上下文coercion及目标有序集合语法都没有修复，不把保护拒绝计成完成。

另用git show只读加载本轮起点PG Parser/Doris Generator、在相同RAISE策略下对原313条逐一比较生成结果：308条文本/错误完全相同，上述5条由生成成功改为unsupported。排除的3条仅做解析比较，没有在数据库执行。此检查不是起点数据库执行，也不改变源证据。

原task-001关联14条最终为3匹配、1值/显示差异、4目标失败、6转译拒绝；其5条失败阶段变化如上，原WITHIN GROUP问题仍在。其他VARIADIC、RWAGG、ARRAY子查询等独立限制保留。

## 4. 新发现与修复任务去向

| 发现 | 证据与归属 | 后续 |
| :--- | :--- | :--- |
| 默认PG数组[1]生成Doris[0]；源[0]生成目标[-1]错误取末元素 | 13条TEXT投影+3条普通INT控制实际执行；不是NUMERIC新回归。复用原数组下标研究登记task-010 | 独立功能commit，不混入本轮；需授权后验证正负/动态索引、越界NULL、嵌套、Map/JSON及其他方言 |
| 文本直接REAL存在double rounding及直接常量路径问题 | 40次路径及3条表查询；Doris对应源码和PG strtof依据见任务报告 | 原task-001保留，不用普通值通过掩盖中点错误 |
| 变Scale/一般NUMERIC、非有限、超过76位、未知源类型 | 本轮只证明有限可表达范围；固定Decimal不能等同PG无约束域 | 原task-001和既有类型研究；不统一转DOUBLE、不强制Schema、不改比较规则 |
| 5条WITHIN GROUP查询被NUMERIC保护先拒绝 | 上述stage-31及生成对比 | 仍是未修复源成功查询，不列负向，不把失败阶段变化计匹配提升 |

统一任务列表已更新，只有这一个列表，不另建新台账。task-003及其他原任务没有实施或重新验收。

## 5. 完成检查与下一轮

- 原源成功查询的全部数据阶段覆盖：**未满足**，310安全范围已跑；3条后端风险未执行，另有原导入器未提取范围沿用既有说明。
- SQLGlot可安全修复问题全部完成：**未满足**，task-001/003有余项，task-010已登记但未实施，其他研究项不冒称完成。
- 最终代码固定后的回归：**已执行约定范围**，43阶段310条、75条新变体、274条旧边界；明确保留提前拒绝、下标失败和未验证范围。
- 剩余差异都已证明不能只靠SQLGlot修复：**未满足**，只对已取得实现/数据库依据的范围下结论。

整份输入未完成，task-001也未关闭。下一独立任务建议task-010，下标的具体范围已写入[统一条目](../attribution/aggregates-001-attribution-summary.md#task-010)，等待用户选择；当前起点是4dc65a35a7efa92551cb9fb00c2315fcb8ff659f。本轮没有自动实施该任务。task-001的REAL/一般NUMERIC研究和task-003类型余项继续保留。

Skill规定处理规则，Agent据此判断修复顺序；用户决定授权范围。两个本地commit只表示对应代码已保存，不等于push、PR或全工作流完成。

