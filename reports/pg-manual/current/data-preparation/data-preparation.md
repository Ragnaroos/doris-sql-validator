# PostgreSQL → Doris 数据准备报告

## 1. 实际完成范围

参考评估库：`dsv_pg_manual_20261111`。该标识记录所用环境，不表示用户机器上已经存在此库。
已准备并完整核验 21 张逻辑表/视图，共 11097 行。当前实际数据一致，不代表两端类型域和约束完全相同。
核验范围为 20 个官方脚本中固定选择的 753 条查询，不是官方全量脚本回放。查询 SQL 与官方 .out 原件保持不变。

## 2. 数据阶段与输入

所有样本对应 setup/postgres-setup.sql 和三个官方 COPY 文件构成的固定初始阶段，旧脚本中其他临时表、后续 UPDATE/复用阶段不在本轮范围。当前 PG 的 753 条源结果已重新执行核对，结果不对应的记录另外列出。
原始输入、源脚本位置和官方 commit 见 cases/postgres/manual/current/scope.json。
postgres-setup.sql 为源 CREATE/INSERT，COPY 数据由 scripts/pg_manual_sample.py --prepare 使用 cursor.copy 从固定 data 文件加载；doris-setup.sql 保存本批首次真实执行的目标 CREATE/INSERT/view 语句。本轮若为复核，则保留这些脚本但不重复执行。

## 3. 逐表完整记录核验与类型映射

| 表 | 源/目标行数 | 重复记录数 | NULL 单元格数 | 完整记录 | 字段映射 |
| :--- | :--- | ---: | ---: | :--- | :--- |
| j1_tbl | 11/11 | 0 | 4 | 一致 | i: int4→INT, j: int4→INT, t: text→VARCHAR(512) |
| j2_tbl | 9/9 | 1 | 4 | 一致 | i: int4→INT, k: int4→INT |
| t1 | 1/1 | 0 | 0 | 一致 | name: text→VARCHAR(512), n: int4→INT |
| t2 | 3/3 | 0 | 0 | 一致 | name: text→VARCHAR(512), n: int4→INT |
| t3 | 3/3 | 0 | 0 | 一致 | name: text→VARCHAR(512), n: int4→INT |
| x | 5/5 | 0 | 2 | 一致 | x1: int4→INT, x2: int4→INT |
| y | 4/4 | 0 | 1 | 一致 | y1: int4→INT, y2: int4→INT |
| empsalary | 10/10 | 0 | 0 | 一致 | depname: varchar→VARCHAR(512), empno: int8→BIGINT, salary: int4→INT, enroll_date: date→DATE |
| subselect_tbl | 8/8 | 0 | 1 | 一致 | f1: int4→INT, f2: int4→INT, f3: float8→DOUBLE |
| foo | 1/1 | 0 | 0 | 一致 | id: int4→INT |
| bar | 3/3 | 0 | 0 | 一致 | id1: int4→INT, id2: int4→INT |
| department | 8/8 | 0 | 1 | 一致 | id: int4→INT, parent_department: int4→INT, name: text→VARCHAR(512) |
| int2_tbl | 5/5 | 0 | 0 | 一致 | f1: int2→SMALLINT |
| int4_tbl | 5/5 | 0 | 0 | 一致 | f1: int4→INT |
| int8_tbl | 5/5 | 0 | 0 | 一致 | q1: int8→BIGINT, q2: int8→BIGINT |
| text_tbl | 2/2 | 0 | 0 | 一致 | f1: text→VARCHAR(512) |
| onek | 1000/1000 | 0 | 0 | 一致 | unique1: int4→INT, unique2: int4→INT, two: int4→INT, four: int4→INT, ten: int4→INT, twenty: int4→INT, hundred: int4→INT, thousand: int4→INT, twothousand: int4→INT, fivethous: int4→INT, tenthous: int4→INT, odd: int4→INT, even: int4→INT, stringu1: name→VARCHAR(512), stringu2: name→VARCHAR(512), string4: name→VARCHAR(512) |
| tenk1 | 10000/10000 | 0 | 0 | 一致 | unique1: int4→INT, unique2: int4→INT, two: int4→INT, four: int4→INT, ten: int4→INT, twenty: int4→INT, hundred: int4→INT, thousand: int4→INT, twothousand: int4→INT, fivethous: int4→INT, tenthous: int4→INT, odd: int4→INT, even: int4→INT, stringu1: name→VARCHAR(512), stringu2: name→VARCHAR(512), string4: name→VARCHAR(512) |
| aggtest | 4/4 | 0 | 0 | 一致 | a: int2→SMALLINT, b: float4→FLOAT |
| gstest1 | 10/10 | 0 | 0 | 一致 | a: int4→INT, b: int4→INT, v: int4→INT |
| gstest_empty | 0/0 | 0 | 0 | 一致 | a: int4→INT, b: int4→INT, v: int4→INT |

完整记录按多重集合比较，不仅是 COUNT/抽样。FLOAT 两端显式转 DOUBLE，PG 使用二进制读取，逐值按 float.hex 检查真实存储值；不采用浮点容差。NULL、空字符串和重复次数保留。

类型限制：TEXT、无长度 VARCHAR、NAME 映射为 VARCHAR(512)，本批 UTF-8 字节长度全部检查，不截断。INTEGER 位宽和 DATE 保持对应；Doris DUPLICATE KEY 保留重复记录。源 PK/FK 约束及全类型域不是本轮核验目标。源大小写名称在 Doris 创建同记录 view，源 SQL 不因此改写。

## 4. 当前 PG 与历史预期输出的重新核对

| 检查结果 | 查询数 |
| :--- | ---: |
| 显示文本与行重复次数一致 | 620 |
| 两端都报错，具体同因尚未确认 | 133 |

成功结果按原生 PG 文本与官方 aligned .out 的行值/重复次数核对，不能恢复 .out 丢失的类型或 NULL 表示细节；负向用例仅确认两边都失败，不宣称同因。输出不可解析或当前源结果不同的记录保留在 data-verification.json，不静默视为通过，也不修改官方答案。

## 5. 版本、Session、证据与下一步

PostgreSQL 环境（版本/数据库/时区/日期格式/浮点额外显示位）：`['PostgreSQL 18.1 (Debian 18.1-1.pgdg12+2) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14+deb12u1) 12.2.0, 64-bit', 'dsv_pg_manual_20261111', 'UTC', 'ISO, MDY', '0']`。
Doris 的实际版本及 PG 错误 SQLSTATE 在 data-verification.json。沿用本批首次创建时的 PG 库配置；源查询核验时仅设置当前 PG Session 的 UTC、ISO/MDY、extra_float_digits=0、5s statement_timeout，不修改旧库、表数据或全局配置；Doris 使用原有 Session 政策。
准备和验证命令见 [PostgreSQL 工作流](../../../../docs/POSTGRES_MANUAL_WORKFLOW.md)。数据准备报告是外部前提证据，不是验证器内部 Gate；运行器不执行这里的准备 SQL。

## 6. 实际 Session 补查

```json
{
  "PostgreSQL": {
    "version": "PostgreSQL 18.1 (Debian 18.1-1.pgdg12+2) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14+deb12u1) 12.2.0, 64-bit",
    "lc_collate": "C",
    "lc_ctype": "C",
    "TimeZone": "UTC",
    "DateStyle": "ISO, MDY",
    "extra_float_digits": "0",
    "statement_timeout": "5s"
  },
  "Doris": {
    "time_zone": "UTC",
    "sql_mode": "ONLY_FULL_GROUP_BY",
    "enable_strict_cast": "false",
    "enable_decimal256": "false",
    "enable_nereids_planner": "当前版本未提供该变量"
  }
}
```

Session 是当前连接实际值，没有修改 Doris 全局或 Session。时区、严格转换等不一致是后续归因需要单独检查的环境前提，不应直接算 SQLGlot 缺陷。
