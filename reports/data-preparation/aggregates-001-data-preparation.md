# aggregates-001：PostgreSQL → Doris 数据准备与核验

## 1. 结论与执行范围

结论：已分阶段准备可表达的数据并完成完整记录核验，但整个输入域尚未全部完成一致前提。43 个隔离阶段覆盖当前 Importer 接受的 313 条查询；已成功完成 540 次阶段表/视图全记录比较，均相同。另有 6 个阶段对象的复合类型或 BYTEA 映射仍受限，不能将相应缺表错误归为 SQLGlot 缺陷。

aggtype(a INT,b INT,c TEXT)[] 已用 ARRAY<STRUCT<a:INT,b:INT,c:STRING>> 明确映射并补齐 7 个阶段；保留数组顺序、[1:n] 维度、元素/字段 NULL，不将其改成普通字符串。

| 环境 | 实际值 |
| :--- | :--- |
| PostgreSQL | 18.1，postgres:18.1-bookworm；127.0.0.1:5432 |
| Doris | doris-4.1.3-rc02-7126cf65d96；127.0.0.1:9030（MySQL 协议 VERSION() 为兼容值，不作为真实产品版本） |
| SQLGlot | 30.25.1.dev6；feb0e08aba28a29590596bb3f5761fbaeb0e98b9；../sqlglot，未应用修复 |
| 源端配置 | UTC、LC_COLLATE/LC_CTYPE=C、DateStyle=ISO, MDY、extra_float_digits=0；各阶段相关配置见下表 |
| 目标配置 | UTC；enable_strict_cast=false；enable_decimal256=false |
| 本批起止 | 2026-11-18T09:53:26.238438+00:00 → 2026-11-18 15:01:21 UTC |
| 运行代码/依赖 | PYTHONPATH=src，借用 ../doris-sql-validator/.venv/bin/python；加载原项目 .env 到进程，不复制凭据，不修改框架代码 |

源 SQL 与 .out 使用用户提供的原路径、原文件名，不复制或修改。原输入位于 ../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql 和 aggregates.out；依赖 test_setup.sql、create_aggregate.sql 和官方 COPY 数据，见指纹表。只记录 SQL/准备脚本/数据指纹，不记录 .out 指纹。

专用数据库：53 个 PostgreSQL 库（阶段库、基础库及事务工作库）和 44 个 Doris 库（43 阶段库与共享物理数据存储库）。创建前已检查名称不存在；没有复用、删除或清空已有用户数据库。保留阶段库供后续只读复查，不自动清理。

## 2. 阶段与查询对应关系

原脚本有 COPY 装数、空表→非空表、反复替换视图、事务内函数定义及回滚。不能一次装成最终状态后运行全部查询。本次先在独立 PostgreSQL 工作库重建各状态，再冻结为阶段库；Doris 在对应阶段暴露同名逻辑视图，底层 DUPLICATE KEY 存储保留重复行，额外行号不暴露给查询。相同实际记录的物理存储可以共享，阶段逻辑视图不会随之后装数改变。

外部准备将临时表物化到专用库以供不同连接只读访问；事务使用独立工作库与父状态恢复，DDL/装数不在验证器内执行。该处理用于 SELECT 的逻辑数据状态，不证明临时对象生命周期、目录文字、锁、执行计划或事务可见性完全一致。PG 元数据/反解析查询另外列为受限。

| 阶段 | Case 数 | 源语句范围 | 双端库 | YAML / JSON 前缀 |
| :--- | :--- | :--- | :--- | :--- |
| aggregates-001-stage-01 | 97 | 5–101 | dsv_wf_agg001_s01 | aggregates-001-stage-01 |
| aggregates-001-stage-02 | 12 | 104–115 | dsv_wf_agg001_s02 | aggregates-001-stage-02 |
| aggregates-001-stage-03 | 20 | 117–138 | dsv_wf_agg001_s03 | aggregates-001-stage-03 |
| aggregates-001-stage-04 | 1 | 140–140 | dsv_wf_agg001_s04 | aggregates-001-stage-04 |
| aggregates-001-stage-05 | 2 | 143–144 | dsv_wf_agg001_s05 | aggregates-001-stage-05 |
| aggregates-001-stage-06 | 1 | 146–146 | dsv_wf_agg001_s06 | aggregates-001-stage-06 |
| aggregates-001-stage-07 | 6 | 149–158 | dsv_wf_agg001_s07 | aggregates-001-stage-07 |
| aggregates-001-stage-08 | 1 | 162–162 | dsv_wf_agg001_s08 | aggregates-001-stage-08 |
| aggregates-001-stage-09 | 10 | 165–183 | dsv_wf_agg001_s09 | aggregates-001-stage-09 |
| aggregates-001-stage-10 | 2 | 197–199 | dsv_wf_agg001_s10 | aggregates-001-stage-10 |
| aggregates-001-stage-11 | 1 | 204–204 | dsv_wf_agg001_s11 | aggregates-001-stage-11 |
| aggregates-001-stage-12 | 3 | 206–208 | dsv_wf_agg001_s12 | aggregates-001-stage-12 |
| aggregates-001-stage-13 | 1 | 246–246 | dsv_wf_agg001_s13 | aggregates-001-stage-13 |
| aggregates-001-stage-14 | 3 | 251–255 | dsv_wf_agg001_s14 | aggregates-001-stage-14 |
| aggregates-001-stage-15 | 6 | 260–265 | dsv_wf_agg001_s15 | aggregates-001-stage-15 |
| aggregates-001-stage-16 | 1 | 267–267 | dsv_wf_agg001_s16 | aggregates-001-stage-16 |
| aggregates-001-stage-17 | 23 | 276–306 | dsv_wf_agg001_s17 | aggregates-001-stage-17 |
| aggregates-001-stage-18 | 2 | 308–309 | dsv_wf_agg001_s18 | aggregates-001-stage-18 |
| aggregates-001-stage-19 | 2 | 311–312 | dsv_wf_agg001_s19 | aggregates-001-stage-19 |
| aggregates-001-stage-20 | 2 | 314–315 | dsv_wf_agg001_s20 | aggregates-001-stage-20 |
| aggregates-001-stage-21 | 2 | 317–318 | dsv_wf_agg001_s21 | aggregates-001-stage-21 |
| aggregates-001-stage-22 | 2 | 320–321 | dsv_wf_agg001_s22 | aggregates-001-stage-22 |
| aggregates-001-stage-23 | 2 | 323–324 | dsv_wf_agg001_s23 | aggregates-001-stage-23 |
| aggregates-001-stage-24 | 2 | 326–327 | dsv_wf_agg001_s24 | aggregates-001-stage-24 |
| aggregates-001-stage-25 | 12 | 329–340 | dsv_wf_agg001_s25 | aggregates-001-stage-25 |
| aggregates-001-stage-26 | 1 | 342–342 | dsv_wf_agg001_s26 | aggregates-001-stage-26 |
| aggregates-001-stage-27 | 1 | 344–344 | dsv_wf_agg001_s27 | aggregates-001-stage-27 |
| aggregates-001-stage-28 | 5 | 346–350 | dsv_wf_agg001_s28 | aggregates-001-stage-28 |
| aggregates-001-stage-29 | 2 | 353–354 | dsv_wf_agg001_s29 | aggregates-001-stage-29 |
| aggregates-001-stage-30 | 3 | 365–371 | dsv_wf_agg001_s30 | aggregates-001-stage-30 |
| aggregates-001-stage-31 | 49 | 380–428 | dsv_wf_agg001_s31 | aggregates-001-stage-31 |
| aggregates-001-stage-32 | 2 | 430–431 | dsv_wf_agg001_s32 | aggregates-001-stage-32 |
| aggregates-001-stage-33 | 6 | 433–438 | dsv_wf_agg001_s33 | aggregates-001-stage-33 |
| aggregates-001-stage-34 | 9 | 456–464 | dsv_wf_agg001_s34 | aggregates-001-stage-34 |
| aggregates-001-stage-35 | 2 | 468–469 | dsv_wf_agg001_s35 | aggregates-001-stage-35 |
| aggregates-001-stage-36 | 1 | 476–476 | dsv_wf_agg001_s36 | aggregates-001-stage-36 |
| aggregates-001-stage-37 | 1 | 481–481 | dsv_wf_agg001_s37 | aggregates-001-stage-37 |
| aggregates-001-stage-38 | 1 | 505–505 | dsv_wf_agg001_s38 | aggregates-001-stage-38 |
| aggregates-001-stage-39 | 1 | 527–527 | dsv_wf_agg001_s39 | aggregates-001-stage-39 |
| aggregates-001-stage-40 | 1 | 534–534 | dsv_wf_agg001_s40 | aggregates-001-stage-40 |
| aggregates-001-stage-41 | 2 | 544–546 | dsv_wf_agg001_s41 | aggregates-001-stage-41 |
| aggregates-001-stage-42 | 6 | 548–555 | dsv_wf_agg001_s42 | aggregates-001-stage-42 |
| aggregates-001-stage-43 | 4 | 582–585 | dsv_wf_agg001_s43 | aggregates-001-stage-43 |

所有阶段 YAML 平铺在 reports/data-preparation/，验证 JSON 平铺在 reports/validation/。每个阶段文件保留原 SQL、原 Case ID 和同文出现序号；不是按 SQL 文本去重，也不把跨阶段同文 SELECT 合并。

## 3. 类型映射与限制

下表合并重复字段布局；实际约束和 SQL 定义在两份准备脚本。源类型与目标物理类型不要求字面相同，但实际值需按明确规则核验。

| 逻辑对象 | 源字段/类型 | Doris 类型 | 限制 |
| :--- | :--- | :--- | :--- |
| aggtest | a smallint；b real | SMALLINT；FLOAT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| emp | name text；age integer；location point；salary integer；manager name | STRING；INT；STRING；INT；VARCHAR(512) | POINT 以其原始文本表示保存；不验证几何操作或继承 ONLY 的等价。 |
| int4_tbl | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| int8_tbl | q1 bigint；q2 bigint | BIGINT；BIGINT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| onek | unique1 integer；unique2 integer；two integer；four integer；ten integer；twenty integer；hundred integer；thousand integer；twothousand integer；fivethous integer；tenthous integer；odd integer；even integer；stringu1 name；stringu2 name；string4 name | INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；VARCHAR(512)；VARCHAR(512)；VARCHAR(512) | NAME→VARCHAR(512) 仅本批实际字符串可表示，类型域/排序另验。 |
| person | name text；age integer；location point | STRING；INT；STRING | POINT 以其原始文本表示保存；不验证几何操作或继承 ONLY 的等价。 |
| stud_emp | name text；age integer；location point；salary integer；manager name；gpa double precision；percent integer | STRING；INT；STRING；INT；VARCHAR(512)；DOUBLE；INT | POINT 以其原始文本表示保存；不验证几何操作或继承 ONLY 的等价。 |
| student | name text；age integer；location point；gpa double precision | STRING；INT；STRING；DOUBLE | POINT 以其原始文本表示保存；不验证几何操作或继承 ONLY 的等价。 |
| tenk1 | unique1 integer；unique2 integer；two integer；four integer；ten integer；twenty integer；hundred integer；thousand integer；twothousand integer；fivethous integer；tenthous integer；odd integer；even integer；stringu1 name；stringu2 name；string4 name | INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；INT；VARCHAR(512)；VARCHAR(512)；VARCHAR(512) | NAME→VARCHAR(512) 仅本批实际字符串可表示，类型域/排序另验。 |
| varchar_tbl | f1 character varying(4) | STRING | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| regr_test | x double precision；y double precision | DOUBLE；DOUBLE | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| bitwise_test | i2 smallint；i4 integer；i8 bigint；i integer；x smallint；y bit(4) | SMALLINT；INT；BIGINT；INT；SMALLINT；STRING | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| bool_test | b1 boolean；b2 boolean；b3 boolean；b4 boolean | BOOLEAN；BOOLEAN；BOOLEAN；BOOLEAN | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| minmaxtest | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| minmaxtest1 | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| minmaxtest2 | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| minmaxtest3 | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| t1 | f1 integer；f2 integer | INT；INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| t2 | f1 bigint；f2 oid | BIGINT；BIGINT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| v1 | f1 integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| pagg_test | x integer；y integer | INT；INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| v_pagg_test | y integer；tmin integer；tmax integer；tndistinct bigint；bmin text；bmax text；bndistinct bigint；amin integer；amax integer；andistinct bigint；aamin integer；aamax integer；aandistinct bigint | INT；INT；INT；BIGINT；STRING；STRING；BIGINT；INT；INT；BIGINT；INT；INT；BIGINT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| aggordview1 | ten integer；p50 integer；px integer；rank bigint | INT；INT；INT；BIGINT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| btg | x integer；y integer；z text；w integer | INT；INT；STRING；INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| group_agg_pk | x integer；y integer；z integer；w integer；f integer | INT；INT；INT；INT；INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| agg_data_20k | g integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| agg_data_2k | g integer | INT | 类型别名、可空性、主键/视图与输出类型契约仍独立验证。 |
| agg_group_1 | c1 integer；c2 numeric；c3 bigint | INT；DECIMAL(38,0)；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_group_2 | a integer；c1 numeric；c2 numeric[]；c3 bigint | INT；DECIMAL(38,0)；ARRAY<DECIMAL(38,0)>；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_group_3 | c1 numeric；c2 bigint；c3 bigint | DECIMAL(38,0)；BIGINT；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_group_4 | c1 numeric；c2 numeric[]；c3 bigint | DECIMAL(38,0)；ARRAY<DECIMAL(38,0)>；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_hash_1 | c1 integer；c2 numeric；c3 bigint | INT；DECIMAL(38,0)；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_hash_2 | a integer；c1 numeric；c2 numeric[]；c3 bigint | INT；DECIMAL(38,0)；ARRAY<DECIMAL(38,0)>；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_hash_3 | c1 numeric；c2 bigint；c3 bigint | DECIMAL(38,0)；BIGINT；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_hash_4 | c1 numeric；c2 numeric[]；c3 bigint | DECIMAL(38,0)；ARRAY<DECIMAL(38,0)>；BIGINT | 无约束 NUMERIC→固定 DECIMAL 仅限已核验数据；不证明完整类型域。 |
| agg_view1 | aggfns aggtype[] | ARRAY<STRUCT<a:INT,b:INT,c:STRING>> | 按真实 aggtype(a INT,b INT,c TEXT) 字段构造 STRUCT；核验原数组 [1:n] 维度、元素与字段 NULL，不把复合数组转成普通字符串 |

尚未完成的映射：

| 阶段 | 对象 | 源字段 | 实际限制 |
| :--- | :--- | :--- | :--- |
| aggregates-001-stage-13 | t_opf | a avg_rec；b text | No lossless reviewed fixture mapping for avg_rec (avg_rec) |
| aggregates-001-stage-14 | t_having | id integer；a avg_rec | No lossless reviewed fixture mapping for avg_rec (avg_rec) |
| aggregates-001-stage-26 | bytea_test_table | v bytea | (1105, 'errCode = 2, detailMessage = doris do not support varbinary create table, could use it by catalog') |
| aggregates-001-stage-27 | bytea_test_table | v bytea | (1105, 'errCode = 2, detailMessage = doris do not support varbinary create table, could use it by catalog') |
| aggregates-001-stage-28 | bytea_test_table | v bytea | (1105, 'errCode = 2, detailMessage = doris do not support varbinary create table, could use it by catalog') |
| aggregates-001-stage-29 | bytea_test_table | v bytea | (1105, 'errCode = 2, detailMessage = doris do not support varbinary create table, could use it by catalog') |

avg_rec 的 (1.0) 与 (1.00) 被专门用来测试记录字节比较，不能通过统一 Decimal Scale 抹掉区别。BYTEA 的字节包含非 UTF-8 内容；当前 Doris 版本内表 VARBINARY 建表被拒绝，错误明确提示外部 Catalog 是另一范围，不能据此宣称整个 Doris 不支持任何二进制，也不能擅自当普通文本。

## 4. 完整记录核验

每个成功映射的阶段对象均读取全量记录，不用 COUNT 或抽样代替。下表仅合并相同表/字段布局和相同记录内容的重复展示；540 次实际比较均相同，共 44 个表记录状态。每行列出涉及阶段（stage- 前缀沿用本批）。

| 对象/数据状态 | 阶段编号 | PG/Doris 行数 | NULL 单元格 | 重复行数 | 完整多重集合 | 源摘要 / 目标摘要 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| aggtest / _fixture_93f1aa72111364f2 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 4/4 | 0 | 0 | 相同 | bd45b794e214ef33f06fe33cdb7f964a78c838745f6f861945034c08685b5a90 / bd45b794e214ef33f06fe33cdb7f964a78c838745f6f861945034c08685b5a90 |
| emp / _fixture_fab604a7372b8853 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 6/6 | 2 | 0 | 相同 | 2c4b19683251c7e736d8b49b8b6bb5e5d4fb02a35ae68ab16c9ad0256d90a6b0 / 2c4b19683251c7e736d8b49b8b6bb5e5d4fb02a35ae68ab16c9ad0256d90a6b0 |
| int4_tbl / _fixture_8d458f62f02d1354 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 5/5 | 0 | 0 | 相同 | 7552618b33624f6488d5fc26f0eade646e3d2bc993e651a98ba3cf99bf4678be / 7552618b33624f6488d5fc26f0eade646e3d2bc993e651a98ba3cf99bf4678be |
| int8_tbl / _fixture_7f0c3d9fd374a475 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 5/5 | 0 | 0 | 相同 | df3d52f3d8bb47b46b262d435ad38215a19984faea87147c6e4107718ff6494c / df3d52f3d8bb47b46b262d435ad38215a19984faea87147c6e4107718ff6494c |
| onek / _fixture_125a2ca01d51ae16 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 1000/1000 | 0 | 0 | 相同 | de8d6750437369ef94efb842c5fb174dbca3942b6e65ec432d9c7fecb19a8d21 / de8d6750437369ef94efb842c5fb174dbca3942b6e65ec432d9c7fecb19a8d21 |
| person / _fixture_6c4a611c2fe3372d | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 58/58 | 0 | 0 | 相同 | c84f4e07e2a16f452a67d6c7adf02c5604e7db82fe194d9150693c0a06eb638a / c84f4e07e2a16f452a67d6c7adf02c5604e7db82fe194d9150693c0a06eb638a |
| stud_emp / _fixture_a577f088b602cc2e | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 3/3 | 5 | 0 | 相同 | c2b81b49348187b5a416feb7bb1e3904bce9164d21661946b698c1e9c23c8b53 / c2b81b49348187b5a416feb7bb1e3904bce9164d21661946b698c1e9c23c8b53 |
| student / _fixture_ebfce6b9011b527d | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 5/5 | 0 | 0 | 相同 | 49f26ecdd444119605c595f7d69d9553f8efbed6ca0b868559480cc8771eea7f / 49f26ecdd444119605c595f7d69d9553f8efbed6ca0b868559480cc8771eea7f |
| tenk1 / _fixture_867927786d32b391 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 10000/10000 | 0 | 0 | 相同 | 3b095d1dd7597afb8610ec1b5a44adecd0110c96e8fffe781067a72422c065c6 / 3b095d1dd7597afb8610ec1b5a44adecd0110c96e8fffe781067a72422c065c6 |
| varchar_tbl / _fixture_37d2c17f2a6d3540 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 4/4 | 0 | 1 | 相同 | 176b2ca3d07f72d869aeedd5e0673151484576e191516339865ef431dc484fa7 / 176b2ca3d07f72d869aeedd5e0673151484576e191516339865ef431dc484fa7 |
| regr_test / _fixture_2e6ed556427d83ee | 02 | 5/5 | 0 | 0 | 相同 | ebefbf031ced4c7937d45b352b0496e25f65287633fe6f720cde2e7de2678bfb / ebefbf031ced4c7937d45b352b0496e25f65287633fe6f720cde2e7de2678bfb |
| bitwise_test / _fixture_29952586615e5533 | 04 | 0/0 | 0 | 0 | 相同 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 / 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| bitwise_test / _fixture_ddab016adfd5da0d | 05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 3/3 | 1 | 0 | 相同 | a8e97ead8422a190751e822b821a76e1321a983f9cca712cebf41f050bb6e767 / a8e97ead8422a190751e822b821a76e1321a983f9cca712cebf41f050bb6e767 |
| bool_test / _fixture_fec0f2bae14ad42e | 06 | 0/0 | 0 | 0 | 相同 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 / 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| bool_test / _fixture_b9967ac2a8b96f21 | 07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 | 3/3 | 6 | 0 | 相同 | 22fc1e956c79d5a85dfcffe1c69a3198893b5cd4ac41fa40a6e90e8f8da416e3 / 22fc1e956c79d5a85dfcffe1c69a3198893b5cd4ac41fa40a6e90e8f8da416e3 |
| minmaxtest / _fixture_9dcf9951c17c3f96 | 10 | 8/8 | 0 | 0 | 相同 | 70f7c8c0d2d3a7534f1f1cd527b2b0c2b9beb8c828b3aae73dcccef74839dccf / 70f7c8c0d2d3a7534f1f1cd527b2b0c2b9beb8c828b3aae73dcccef74839dccf |
| minmaxtest1 / _fixture_39d45f6b71928833 | 10 | 2/2 | 0 | 0 | 相同 | cd8ca571f6b901fb2d21d81ec4a6f31e24235f18b78d9dcb3d500914fec7fa38 / cd8ca571f6b901fb2d21d81ec4a6f31e24235f18b78d9dcb3d500914fec7fa38 |
| minmaxtest2 / _fixture_9906dec05b0c96fe | 10 | 2/2 | 0 | 0 | 相同 | abc331f8677b671ae2d6b3225990b5f734dd35f99b1eee6e406784979ab7e562 / abc331f8677b671ae2d6b3225990b5f734dd35f99b1eee6e406784979ab7e562 |
| minmaxtest3 / _fixture_335badb16176708f | 10 | 2/2 | 0 | 0 | 相同 | c7bc592fa0e5899a2cc451510d4fb03bfc50bed5c1c7ee60b62c0c5d44e34d69 / c7bc592fa0e5899a2cc451510d4fb03bfc50bed5c1c7ee60b62c0c5d44e34d69 |
| t1 / _fixture_586a452554447b0a | 15,16 | 0/0 | 0 | 0 | 相同 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 / 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| t2 / _fixture_882511340a419b3e | 15,16 | 0/0 | 0 | 0 | 相同 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 / 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| v1 / _fixture_2f59aeff21b0f9af | 16 | 0/0 | 0 | 0 | 相同 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 / 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| pagg_test / _fixture_3bc7b0a0b7bcdf12 | 30 | 5000/5000 | 1250 | 1245 | 相同 | 679af2a2168596c0a8524c4d6d80efb65c52e2145f2f01f4b789a296001e36a3 / 679af2a2168596c0a8524c4d6d80efb65c52e2145f2f01f4b789a296001e36a3 |
| v_pagg_test / _fixture_d93731d2d78858f3 | 30 | 10/10 | 0 | 0 | 相同 | 41b290ebda04c2763c3263792f4317b88e2e14da5c1a8e343328337919181f95 / 41b290ebda04c2763c3263792f4317b88e2e14da5c1a8e343328337919181f95 |
| aggordview1 / _fixture_9a73a0bf7c9ee853 | 32 | 10/10 | 9 | 0 | 相同 | b2da2b74f2ee812f1b4513341c8a2f4dcb67fb30721015bb709fee8e22715800 / b2da2b74f2ee812f1b4513341c8a2f4dcb67fb30721015bb709fee8e22715800 |
| btg / _fixture_2c37dfbe39576ca1 | 38 | 100/100 | 0 | 0 | 相同 | b4910a78e13db8366f2a8ea5bf3f0c5c42b8a9e7198bc8cb2926528107f686ec / b4910a78e13db8366f2a8ea5bf3f0c5c42b8a9e7198bc8cb2926528107f686ec |
| group_agg_pk / _fixture_b8ea6e647e1173ba | 38 | 100/100 | 0 | 90 | 相同 | 2def415aedff630e9928c8960269726c13eddf1fa5af274ef0d8ff0c81983845 / 2def415aedff630e9928c8960269726c13eddf1fa5af274ef0d8ff0c81983845 |
| agg_data_20k / _fixture_b28f7bdafc3ef7dd | 43 | 20000/20000 | 0 | 0 | 相同 | a2f0a68f5038677263b32e6cc5c981119db581028e25d189f564707be2ae1de9 / a2f0a68f5038677263b32e6cc5c981119db581028e25d189f564707be2ae1de9 |
| agg_data_2k / _fixture_a49bd92d400ac2c9 | 43 | 2000/2000 | 0 | 0 | 相同 | 221876d2aaa7e3f6d72e8d63beca5491bc48060571a013df69afee62067a34ee / 221876d2aaa7e3f6d72e8d63beca5491bc48060571a013df69afee62067a34ee |
| agg_group_1 / _fixture_0b0a1e4f6941b91f | 43 | 10000/10000 | 0 | 0 | 相同 | 651426d94fb2c48287c02b0d7091385c39e6d0c5931e907a0c944a6455cda210 / 651426d94fb2c48287c02b0d7091385c39e6d0c5931e907a0c944a6455cda210 |
| agg_group_2 / _fixture_14df7bc03c4a7c15 | 43 | 450/450 | 0 | 0 | 相同 | 5fb7ac96dac935bb1920511859f63a0da8c2cef43522df1d093b562a8db94d5b / 5fb7ac96dac935bb1920511859f63a0da8c2cef43522df1d093b562a8db94d5b |
| agg_group_3 / _fixture_fbcae98f24da3e2b | 43 | 1000/1000 | 0 | 0 | 相同 | a0c01df3f9a7f247ba77902d7f6896c6e5dcc2cbaae4d76bc344d0ca12540e76 / a0c01df3f9a7f247ba77902d7f6896c6e5dcc2cbaae4d76bc344d0ca12540e76 |
| agg_group_4 / _fixture_5eba18d2c85def15 | 43 | 1000/1000 | 0 | 0 | 相同 | 4e6eb6fbd37e1aa9d51149c3aa4bfb829a23b27fe915a429282ce984f1cb7311 / 4e6eb6fbd37e1aa9d51149c3aa4bfb829a23b27fe915a429282ce984f1cb7311 |
| agg_hash_1 / _fixture_0b0a1e4f6941b91f | 43 | 10000/10000 | 0 | 0 | 相同 | 651426d94fb2c48287c02b0d7091385c39e6d0c5931e907a0c944a6455cda210 / 651426d94fb2c48287c02b0d7091385c39e6d0c5931e907a0c944a6455cda210 |
| agg_hash_2 / _fixture_14df7bc03c4a7c15 | 43 | 450/450 | 0 | 0 | 相同 | 5fb7ac96dac935bb1920511859f63a0da8c2cef43522df1d093b562a8db94d5b / 5fb7ac96dac935bb1920511859f63a0da8c2cef43522df1d093b562a8db94d5b |
| agg_hash_3 / _fixture_fbcae98f24da3e2b | 43 | 1000/1000 | 0 | 0 | 相同 | a0c01df3f9a7f247ba77902d7f6896c6e5dcc2cbaae4d76bc344d0ca12540e76 / a0c01df3f9a7f247ba77902d7f6896c6e5dcc2cbaae4d76bc344d0ca12540e76 |
| agg_hash_4 / _fixture_5eba18d2c85def15 | 43 | 1000/1000 | 0 | 0 | 相同 | 4e6eb6fbd37e1aa9d51149c3aa4bfb829a23b27fe915a429282ce984f1cb7311 / 4e6eb6fbd37e1aa9d51149c3aa4bfb829a23b27fe915a429282ce984f1cb7311 |
| agg_view1 / _fixture_composite_18 | 18 | 1/1 | 0 | 0 | 相同 | 2890a746839bdb812f1e5dfcf7ba71a7ac9b304b4f7b939f145e40ed8460e7cf / 2890a746839bdb812f1e5dfcf7ba71a7ac9b304b4f7b939f145e40ed8460e7cf |
| agg_view1 / _fixture_composite_19 | 19 | 1/1 | 0 | 0 | 相同 | 09a0c8c945d4346ebed5c35158e22a836484b4732c51f4a0dd06e660e9efdbb8 / 09a0c8c945d4346ebed5c35158e22a836484b4732c51f4a0dd06e660e9efdbb8 |
| agg_view1 / _fixture_composite_20 | 20 | 1/1 | 0 | 0 | 相同 | 35af659ce255015e7c5a0882e134003dfd9ad5401619080419f8488b854403a1 / 35af659ce255015e7c5a0882e134003dfd9ad5401619080419f8488b854403a1 |
| agg_view1 / _fixture_composite_21 | 21 | 1/1 | 0 | 0 | 相同 | 35af659ce255015e7c5a0882e134003dfd9ad5401619080419f8488b854403a1 / 35af659ce255015e7c5a0882e134003dfd9ad5401619080419f8488b854403a1 |
| agg_view1 / _fixture_composite_22 | 22 | 1/1 | 0 | 0 | 相同 | fe4f14e92908f0adcc8bda3b176711d10ce62e9ac477942ca5027f79ca614821 / fe4f14e92908f0adcc8bda3b176711d10ce62e9ac477942ca5027f79ca614821 |
| agg_view1 / _fixture_composite_23 | 23 | 1/1 | 0 | 0 | 相同 | 2877ba469ed66801632a4cfc10b4c8fc0e8910879ca824301bf82e3f76f62fb0 / 2877ba469ed66801632a4cfc10b4c8fc0e8910879ca824301bf82e3f76f62fb0 |
| agg_view1 / _fixture_composite_24 | 24 | 1/1 | 0 | 0 | 相同 | 09a0c8c945d4346ebed5c35158e22a836484b4732c51f4a0dd06e660e9efdbb8 / 09a0c8c945d4346ebed5c35158e22a836484b4732c51f4a0dd06e660e9efdbb8 |

实际查询和归一化方法：

```text
PostgreSQL：SELECT <原列顺序> FROM <阶段逻辑表>，cursor(binary=True) 读取；POINT/BIT 列仅在声明的映射中显式转文本。
Doris：SELECT <原列顺序> FROM <同名阶段视图>；FLOAT/DOUBLE 列额外 CAST AS DOUBLE，以免 FLOAT 协议显示缩短值。
复合数组：SELECT to_jsonb(aggfns), array_dims(aggfns) FROM agg_view1，按已知真实结构核验；目标 ARRAY<STRUCT> 按相同字段读取。
两侧所有行转为保留类型标记的规范记录，逐行计数后比较 Counter；忽略外层表顺序、保留重复次数。
数字用 Decimal 元组去除无意义尾零，不靠浮点容差；二进制用完整字节；布尔独立；NULL 独立；数组顺序保留；真实结构字段按已知名称组织。
摘要：对规范记录及出现次数排序后以 JSON 编码，再计算 SHA-256。摘要相同仅证明此规则下的本批实际记录，不代替类型域/约束验证。
实际输出：540 次完整 Counter 相同，0 次不相同；未映射对象不计作通过。
```

复杂值在报告中只展示必要反例/样本；完整结构比较发生在内存，未生成核验 JSON。对应 SQL 全部记录在 postgres-setup.sql / doris-setup.sql，名称带本批前缀。

## 5. 当前 PostgreSQL 与历史输出

| 源端核对情况 | 查询数 | 解释 |
| :--- | :--- | :--- |
| 显示文本、行及重复次数相同 | 258 | 只证明 .out 能表达的这些维度，类型信息仍需补查 |
| 当前显示文本或记录不同 | 21 | 包括统计实现/显示及视图反解析；逐 Case 不用当前值覆盖历史基线 |
| 历史成功、当前源执行异常 | 7 | 6 条版本/实现行为不兼容，1 条触发后端段错误 |
| 同类高风险语句未执行 | 2 | 保留历史成功证据，不重试 |
| 历史及当前均报错 | 25 | 源端负向用例，默认不进入归因/修复 |

PostgreSQL 18.1 对部分 float8_regr_* 状态函数要求 6 元素数组，而输入/历史成功输出使用 8 元素；也拒绝两条历史可执行的分组相关语法。未修改输入来迎合当前版本。另有 5 次 enable_groupagg 配置尝试在此版本不识别；未据计划配置失败修改查询或答案。

源端崩溃证据（已恢复，不重复执行）：

```text
2026-11-18 10:07:13.306 UTC: client backend was terminated by signal 11: Segmentation fault
Failed process: select array_agg(distinct r order by r using <, r using *<) ...
2026-11-18 10:07:16.313 UTC: database system is ready to accept connections
触发 Case：pg-aggregates-0301-8e89d955；同类 0303 / 0304 未重试。
```

数值补证：归因阶段另用 PostgreSQL binary cursor 复查 88 条数值查询，避免 extra_float_digits=0 的显示精度被误当作真实算术差异；Doris FLOAT32 的协议显示仍需单独说明。该补证不改变原 .out 或首轮比较规则。

## 6. 导入覆盖缺口

当前 Importer 接受 313 条查询；另有 2 条明确 SELECT 未被导入。原因位于 importing/importer.py:_sanitize_harness：COPY 检测仅匹配 FROM STDIN;，没有匹配 FROM STDIN NULL 'null';，数据正文与后面的 SELECT 混成一条后被跳过。这不是 .out 定位失败，也不是 SQLGlot 转译失败。本轮没有修改框架或用手工 YAML 隐藏缺口。

源行 302–328（前部可能含被注释的数据行）；实际 SELECT：

```sql
SELECT
  BIT_AND(i2) AS "1",
  BIT_AND(i4) AS "1",
  BIT_AND(i8) AS "1",
  BIT_AND(i)  AS "?",
  BIT_AND(x)  AS "0",
  BIT_AND(y)  AS "0100",

  BIT_OR(i2)  AS "7",
  BIT_OR(i4)  AS "7",
  BIT_OR(i8)  AS "7",
  BIT_OR(i)   AS "?",
  BIT_OR(x)   AS "7",
  BIT_OR(y)   AS "1101",

  BIT_XOR(i2) AS "5",
  BIT_XOR(i4) AS "5",
  BIT_XOR(i8) AS "5",
  BIT_XOR(i)  AS "?",
  BIT_XOR(x)  AS "7",
  BIT_XOR(y)  AS "1101"
FROM bitwise_test;
```

源行 376–388（前部可能含被注释的数据行）；实际 SELECT：

```sql
SELECT
  BOOL_AND(b1)     AS "f",
  BOOL_AND(b2)     AS "t",
  BOOL_AND(b3)     AS "f",
  BOOL_AND(b4)     AS "n",
  BOOL_AND(NOT b2) AS "f",
  BOOL_AND(NOT b3) AS "t"
FROM bool_test;
```

## 7. 文件身份与复查命令

| 输入或产物路径（相对项目根） | SHA-256 |
| :--- | :--- |
| ../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql | 9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62 |
| ../doris-sql-validator/cases/postgres/manual/current/assets/test_setup.sql | 1c5e005b488f306c41a349a55c768fe22a2882f0955ae8ae46d26d5baadcf7c3 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/sql/create_aggregate.sql | 825118ca3c338e0d95dab7358b2f78a67d2b451130c7c0be25fb840cd0db5dde |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/onek.data | 1f59332622392237c33d997e605177db5d77dc09b370599005223b0adf901b5c |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/tenk.data | d62f34bdc0a25a5ba36f2dbe62a35479d9e51a7326d482e418091ea2ed40e484 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/agg.data | ef281324e147482d6426b920a23bafd3fee151b57d59a913d611551a6a1935e6 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/person.data | 972c72e1b7a2753042c08b6350191c2153a939ae18a5efeb460266049e244fb0 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/emp.data | 7dbe59ca2db2c4b614c7a9911c5da8702d551a26cfbcd81b01ccdcfb2529b256 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/student.data | 20215bf2ed33198292cec7bcd121ff035a73e76ecbda567ee5ebeba6b477a832 |
| ../doris-sql-validator/upstream/postgres/src/test/regress/data/stud_emp.data | 8d2a5972c8751ad18138164b99f561140923d09c2b872804c24dbad74c1a6cdb |
| reports/data-preparation/aggregates-001-postgres-setup.sql | 9ab6156106b2468b286c2dce8c8c0552ffa08ce55ec3c45fb836220527069f2a |
| reports/data-preparation/aggregates-001-doris-setup.sql | a068c36ba56b8304276b4fab2b4ef8888731b6be520797d7a1083b4df8498748 |

.out 只引用原路径，不存或检查内容指纹。数据库凭据不进入任何报告。两份准备 SQL 对应实际执行的准备操作；源脚本使用 psql 的 \\connect / \\copy，从工作流项目根目录解释相对数据路径。建库名称必须全新，不能在现有本批库上盲目重放；再次运行应分配新批次。

当前环境实际通过 CLI 的同一入口在进程内逐阶段执行 cases-lint / run，未绕过 Comparator。安装本项目 .venv 并配置连接后，可直接复查任一已准备阶段：

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml

.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --output reports/validation/aggregates-001-stage-01-validation.json
```

其余阶段将 stage-01 替换为上表阶段前缀。验证器只执行 YAML 中查询，不执行准备 SQL、复制数据或设置 Fixture Gate。后续入口：[归因汇总](../attribution/aggregates-001-attribution-summary.md)。
