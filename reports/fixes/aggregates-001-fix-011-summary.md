# aggregates-001 / fix-011：task-001、task-003 类型核验

## 1. 本轮结论

**本轮已完成所列类型补查，但 task-001、task-003 仍为“已修改但未完成验收”；整份输入未完成。** 本轮是验收与归因补证，没有新增 SQLGlot 补丁。未把数组声明别名、驱动显示差异与真实类型缺口混为一类，也没有用“所有数组 CAST INT”伪造通过。

| 实际范围 | 数量与结论 |
| :--- | :--- |
| task-001 原关联查询 | 14 条，3 条原 .out 显示匹配、1 条显示/值差异、9 条 Doris 失败、1 条转译拒绝；4 条双端成功查询仍有原生类型差异 |
| task-003 原关联查询 | 10 条，6 条显示/值差异、4 条 Doris 失败；6 条双端成功查询仍为 int4[] / ARRAY<TINYINT> |
| 原始源证据补查 | 24 条当前 PG 均成功，文本化结果逐条与各自 .out 一致，未替换基线 |
| task-001 既有边界 | 18 条，全部成功、值与重复执行稳定；9 条取得的全部输出类型约束对齐，其余7条数组默认类型不同、1条独立id列位宽不同、1条Decimal结果约束不能判等 |
| task-003 既有边界 | 22 条，19 条已取类型可映射、2 条Decimal结果精度不能直接判等、1 条TIMESTAMP真实丢微秒；结合值/顺序，18条可完成本次固定输入维度核对，另外保留DISTINCT未保证元素顺序的实际差异 |
| 额外类型诊断 | 15 组只读对照，含同一源SQL的不同候选；4个人工CAST候选在当前样本对齐，1个统一INT反例把BIGINT变成NULL；不计为生成器修复 |
| 扩展原查询回归 | 142 条、19 阶段：82 匹配、36 Doris失败、19值/顺序不同、1转译失败、4源端负向；前轮81个匹配全部保持 |
| 当前代码测试 | PG/Doris/MySQL 156 方法、全部方言1079方法通过；156包含在1079内，不相加 |

142条比fix-010的132条多了10条，其中0306以前已在fix-001匹配，本次只是重新纳入回归范围。因此82对81**不是本轮新增修复提升**；本轮代码根本没有变化。不宣称执行了全部313条或完成最终43阶段验收。

本轮只纳入两个task，互斥状态为“已修改但未完成验收”2项，其余0项；全批仍为7项完成约定验收、2项已修改未验收。没有新增/重新打开task编号，没有把独立问题混成补丁。

## 2. 任务导航

| 任务 | 当前结论 | 本轮报告 | 下一实现重点 |
| :--- | :--- | :--- | :--- |
| task-001 数组构造 | 类型验收未关闭 | [task-001](tasks/aggregates-001/fix-011/task-001.md) | 裸整数/标量子查询、unknown/NULL与字符串的源共同元素类型保留；区分INT4/INT8/NUMERIC，不硬转INT |
| task-003 ARRAY_AGG NULL/空输入 | NULL规则保留，类型验收未关闭 | [task-003](tasks/aggregates-001/fix-011/task-003.md) | 从可信输入类型保留数组元素类型；VALUES推断、Decimal结果声明与已有显示/时间问题分开 |

具体验收子项已写进这两份报告，并更新[原归因任务清单](../attribution/aggregates-001-attribution-summary.md#tasks)；仍沿用原 task-id。原24份Case文档追加本轮事实，不复制成新一套归因文件。

## 3. 代码、输入与环境

指定任务模式：用户授权继续 task-001、task-003 类型验收及有证据支持的相关安全修复。未扩大到验证器、全局类型推断、数据库写入、Session政策或新独立任务实施。没有安全通用补丁前不强行修改代码，不将未完成写成不可修复。

| 项目 | 本轮实际身份 |
| :--- | :--- |
| SQLGlot checkout / 分支 | ../sqlglot-experiment / codex/doris-array-literal |
| 起止 HEAD | 089891f2521780e2c5b243005017af9db62f25a6 |
| 起止累积 diff SHA256 | 均为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18；与fix-010相同，包含前轮已有修改 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 框架解释器 | ../doris-sql-validator/.venv/bin/python；PYTHONDONTWRITEBYTECODE=1，PYTHONPATH=../sqlglot-experiment:src |
| 实际 import | ../sqlglot-experiment/sqlglot/__init__.py；30.25.1.dev355 |
| PostgreSQL | 本轮18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | 本轮SHOW FRONTENDS为doris-4.1.3-rc02-7126cf65d96、Alive=true，127.0.0.1:9030；UTC、enable_strict_cast=false |
| 时间 | 2026-11-24，40条边界结束11:12:07，原查询回归结束11:12:44，补充控制结束11:14:54；以上均Asia/Shanghai |
| 提交 / 推送 | 无commit/push，无Issue/PR；此前代码与用户修改保留 |

原SQL/.out仍位于 `../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql` 和同名.out；YAML在 `reports/data-preparation/aggregates-001-stage-XX-cases.yaml`，首轮JSON在 `reports/validation/aggregates-001-stage-XX-validation.json`。原 SQL/.out、YAML、首轮及前轮报告不修改，不保存/校验.out指纹。

读取并沿用[数据准备报告](../data-preparation/aggregates-001-data-preparation.md)及同前缀postgres-setup.sql、doris-setup.sql，没有重建或重装数据。准备脚本中本轮涉及的 least/cleast 和 rwagg/eatarray 函数体已核对，为纯计算/数组处理；只在源只读连接补查，不执行其他未知副作用函数。

## 4. 实际执行方式与证据

同阶段原查询通过一个Python进程里的 `CliRunner().invoke(app, ['run','--path',<原YAML>,'--stdout','--id',<ID>,...])` 批量运行。142条各阶段查询数为：01:50、03:8、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:15、25:6、30:3、31:25、32:1、33:3、40:1、41:1、42:3、43:4。未把多个阶段SQL混到同一数据库。

关联原查询和边界实际使用当前 `SqlglotTranspiler.transpile_case` 或 `parse_one(..., read='postgres').sql('doris', unsupported_level=RAISE)`，然后 `pg_probe.execute_query` / `compare_probe`；10秒、10000行限制，边界两端各重复一次。没有用人工CAST候选代替当前生成器的验收。

新增源元数据补查为只读的 `cursor.pgresult.fmod(i)`、字段描述和 `SELECT oid,typname,typelem FROM pg_type`。源文本基线核对使用 `SELECT CAST(c0 AS TEXT),... FROM (<原查询>) checked(c0,...)`，按原记录值/重复次数核对 .out，不凭包装证明原排序或用包装替换原SQL。

### 明确的类型归因

| 观察 | 本轮证据 | 去向 |
| :--- | :--- | :--- |
| _int4 / ARRAY<INT> | 源element OID23、目标INT，32位元素别名可映射 | 补足递归类型证据，不需要为名称不同改SQLGlot |
| _int4 / ARRAY<TINYINT> | 0287及多个边界是真位宽差异；去掉聚合后的VALUES也复现 | SQLGlot缺少可信源共同类型保留，原task的类型子项仍未完成 |
| _text / ARRAY<NULL_TYPE>或VARCHAR(5) | 全unknown/NULL、裸字符串的类型解析不同 | 不是“值一样就可忽略”，保留源默认类型转换缺口 |
| Decimal元数据 | 直接同型CAST数组可读到655366/(10,2)；聚合或外层Neg结果为-1 | 不再笼统说驱动全都读不到；区分结果是否声明约束，不能直接判精度相等 |
| Boolean数组 | BOOL/BOOLEAN类型一致，原生标量投影true/NULL/false对齐1/NULL/0 | 当前样本是嵌套显示问题；原比较不同保留，不改框架 |
| TIMESTAMP数组丢微秒 | 无ARRAY_AGG的标量CAST也丢 .123456 | 已有通用时间精度研究，不混入NULL聚合补丁 |
| 手工全转INT | 成功源ARRAY[2147483648]被候选转换成[NULL] | 明确排除不安全补丁，不能以样本小整数成功泛化 |

共同类型规则参考[PostgreSQL官方说明](https://www.postgresql.org/docs/18/typeconv-union-case.html)，协议字段修饰信息参考[PQfmod](https://www.postgresql.org/docs/18/libpq-exec.html)。实际取证与Agent对原因的解释分开；文档规则不替代本轮执行。

## 5. 测试与验收限制

工作目录 `../sqlglot-experiment`，PATH含其.venv/bin，解释器为 `.venv/bin/python`：

| 实际命令 | 结果 |
| :--- | :--- |
| python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.dialects.test_mysql | 156方法通过 |
| python -m unittest discover -s tests/dialects | 1079方法通过 |
| .venv/bin/ruff check、format --check 六个既有累积修改文件；git diff --check | 通过 |

本轮无新代码/新单测。这些测试说明当前checkpoint未坏，不证明数据库类型验收通过。核心233方法只在前轮运行，本轮未重跑；完整make check、C/mypy、DuckDB相关全套也未运行。

## 6. 下一轮与整份输入状态

原task列表增加了明确类型子项与本轮事实，**没有通过改任务名称或删除反例来关闭任务**。下一实现顺序建议：先在task-001内处理可证明源元素类型的保真转换；再在task-003内处理其输入类型传播/结果类型保留。共享的VALUES/CASE/全局字面量求型、时间精度与框架表示若需要独立代码机制，先明确新的拆分/授权，不把它们随手塞入数组补丁。

目前“直接加annotate_types”还不安全：它将ARRAY[1.25,2]标为DOUBLE、ARRAY[NULL]标为NULL，和源NUMERIC/TEXT不同；而VALUES的INT例子在qualify后虽能推断，当前Generator尚不会自动保真CAST。这是需要继续实现/测试的具体缺口，不是已证明不可解决，也不是必须让用户提供Schema。

整份输入未完成：两个既有task仍有类型反例/约束未对齐，尚有其他待研究与前提阻断，本轮未进行所有43阶段的最终回归，既知导入遗漏也未处理。不以本轮报告或单元测试通过代替最终验收；没有自动扩大范围或实施下一轮。
