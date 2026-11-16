#!/usr/bin/env python3
"""Explicit sample reproduction outside the validator: no LLM or legacy runner."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
import logging
from pathlib import Path
import re
import shutil
import subprocess

from dotenv import load_dotenv
import sqlglot
from sqlglot import exp

from doris_sql_validator.case_loader import load_case_file, write_case_file
from doris_sql_validator.execution.doris import DorisAdapter
from doris_sql_validator.execution.postgres import PostgresAdapter
from doris_sql_validator.importing import ImportOptions, import_case_file
from doris_sql_validator.importing.importer import split_sql_script, _strip_leading_comments, _sanitize_harness
from doris_sql_validator.models import CaseDefinition, ImportDiagnostic, ImportSummary
from doris_sql_validator.recorded_output import parse_recorded_case
from doris_sql_validator.recorded_output.pg_echo import pg_echo_identity
from doris_sql_validator.sql_utils import file_sha256

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "cases/postgres/manual/current"
OUTPUT = ROOT / "reports/pg-manual/current"
TYPE_MAP = {"int2": "SMALLINT", "int4": "INT", "int8": "BIGINT", "float4": "FLOAT", "float8": "DOUBLE", "text": "VARCHAR(512)", "varchar": "VARCHAR(512)", "name": "VARCHAR(512)", "date": "DATE"}


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def fingerprint(path):
    return file_sha256(path.read_bytes())


def collect_inputs(corpus):
    """Copy inputs only; intentionally discard every historical observed result."""
    if INPUT.exists():
        raise RuntimeError("current 输入目录已存在，拒绝覆盖；先归档上一轮 current")
    old = json.loads((corpus / "provenance.json").read_text())
    INPUT.mkdir(parents=True)
    shutil.copytree(corpus / "assets", INPUT / "assets")
    (INPUT / "setup").mkdir()
    shutil.copyfile(corpus / "setup/postgres.sql", INPUT / "setup/postgres-setup.sql")
    shutil.copytree(corpus / "setup/data", INPUT / "setup/data")
    copyright_path = ROOT / "upstream/postgres/COPYRIGHT"
    if copyright_path.exists(): shutil.copyfile(copyright_path, INPUT / "UPSTREAM_COPYRIGHT")
    fields = ["id", "category", "file", "line_start", "line_end", "source_sql", "official_occurrence"]
    cases = [{k: c[k] for k in fields} for c in old["cases"]]
    inventory = {str(p.relative_to(INPUT)): fingerprint(p) for p in INPUT.rglob("*") if p.is_file()}
    dump(INPUT / "scope.json", {
        "upstream_commit": old["upstream_commit"],
        "selection_explanation": "复用历史固定的语句选择范围，不复制旧结果、是否通过、源行值或旧核验证据；本次重新执行。并非官方完整脚本回放。",
        "phase": "21 张持久表/视图的固定初始数据阶段；每条所选查询的当前源结果另外重新核对官方输出",
        "cases": cases, "input_sha256": inventory,
    })
    print(f"已复制 {len(cases)} 条样本的输入位置与原 SQL，不含历史执行结果", flush=True)


def load_scope():
    data = json.loads((INPUT / "scope.json").read_text())
    for relative, sha in data["input_sha256"].items():
        if fingerprint(INPUT / relative) != sha:
            raise RuntimeError(f"输入已改变：{relative}")
    return data


def sql_value(value):
    if value is None: return "NULL"
    if isinstance(value, bool): return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float, Decimal)): return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def record_key(row):
    values = []
    for v in row:
        if v is None: values.append(["NULL"])
        elif isinstance(v, float): values.append(["IEEE-754 binary64", v.hex()])
        elif isinstance(v, date): values.append(["date", v.isoformat()])
        elif isinstance(v, int): values.append(["integer", str(v)])
        else: values.append(["text", str(v)])
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def bag_evidence(rows):
    keys = [record_key(r) for r in rows]
    digest = hashlib.sha256()
    for key in sorted(keys):
        encoded = key.encode()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return Counter(keys), digest.hexdigest()


def source_baselines(connection, scope):
    checks = []
    occurrences = {}
    for filename in dict.fromkeys(c["file"] for c in scope["cases"]):
        counts = Counter()
        source_text = _sanitize_harness((INPUT / "assets" / filename).read_text(), "pg-regress")
        for statement in split_sql_script(source_text):
            raw = _strip_leading_comments(statement.text.strip())
            if raw:
                key = pg_echo_identity(raw)
                counts[key] += 1
                occurrences[(filename, statement.index)] = counts[key]
    with connection.cursor() as c:
        c.execute("SET default_transaction_read_only = on")
        c.execute("SET statement_timeout = '5s'")
        c.execute("SET timezone = 'UTC'")
        c.execute("SET datestyle = 'ISO, MDY'")
        c.execute("SET extra_float_digits = 0")
        for item in scope["cases"]:
            result = {"sample_id": item["id"], "file": item["file"], "statement": int(item["id"].rsplit("-", 1)[1]), "source_sql": item["source_sql"]}
            expected = None
            try:
                result["output_occurrence"] = occurrences[(item["file"], result["statement"])]
                expected = parse_recorded_case(output_format="pg-regress", output_text=(INPUT / "assets" / item["file"].replace(".sql", ".out")).read_text(), case=CaseDefinition(id=item["id"], statement_index=result["statement"], sql=item["source_sql"], output_occurrence=result["output_occurrence"]), dialect="postgres", artifact=item["file"].replace(".sql", ".out"))
            except ValueError as exc:
                result["reference_parse_error"] = str(exc)
            try:
                c.execute(item["source_sql"])
                # Raw PG text is the closest available source to aligned psql .out;
                # these are not native type/NULL/error-cause equivalence claims.
                wire = [[(c.pgresult.get_value(r, col) or b"").decode().strip() for col in range(c.pgresult.nfields)] for r in range(c.pgresult.ntuples)]
                result.update(source_success=True, row_count=len(wire))
                if expected is not None:
                    equal = expected.result.success and Counter(map(tuple, wire)) == Counter(map(tuple, expected.result.rows))
                    result["reference_check"] = "显示文本与行重复次数一致" if equal else "当前 PG 与历史输出不同，需单独核对"
                    if not equal: result.update(source_sample=wire[:5], reference_sample=expected.result.rows[:5])
            except Exception as exc:
                result.update(source_success=False, source_error=str(exc), sqlstate=getattr(exc, "sqlstate", None))
                if expected is not None:
                    result["reference_check"] = "两端都报错，具体同因尚未确认" if not expected.result.success else "历史输出成功但当前 PG 报错"
            checks.append(result)
    return checks


def prepare(database):
    scope = load_scope()
    if not re.fullmatch(r"dsv_pg_manual_[a-z0-9_]+", database):
        raise ValueError("只允许新建 dsv_pg_manual_ 前缀的独立测试库")
    folder = OUTPUT / "data-preparation"
    if folder.exists():
        raise RuntimeError("current 数据准备目录已存在，拒绝覆盖；请先归档")
    pg, target = PostgresAdapter(), DorisAdapter()
    # Check both before creating either; no DROP/TRUNCATE or reuse of old DBs.
    with pg.connect(database="postgres") as control:
        with control.cursor() as c:
            c.execute("SELECT 1 FROM pg_database WHERE datname=%s", (database,))
            if c.fetchone(): raise RuntimeError("PostgreSQL 同名库已存在，拒绝复用")
    dc = target.connect()
    try:
        with dc.cursor() as c:
            c.execute("SHOW DATABASES")
            if database in {r[0] for r in c.fetchall()}: raise RuntimeError("Doris 同名库已存在，拒绝复用")
    finally: dc.close()
    folder.mkdir(parents=True)
    dump(folder / "execution-start.json", {"database": database, "started_at": datetime.now(timezone.utc).isoformat(), "scope_sha256": fingerprint(INPUT / "scope.json"), "script_sha256": fingerprint(Path(__file__))})
    with pg.connect(database="postgres") as control:
        with control.cursor() as c:
            c.execute(f'CREATE DATABASE "{database}" LC_COLLATE \'C\' LC_CTYPE \'C\' TEMPLATE template0')
            for name, value in [("timezone", "UTC"), ("datestyle", "ISO, MDY"), ("extra_float_digits", "0"), ("statement_timeout", "5s")]:
                c.execute(f'ALTER DATABASE "{database}" SET {name} = \'{value}\'')
    dc = target.connect()
    try:
        with dc.cursor() as c: c.execute(f"CREATE DATABASE `{database}`")
    finally: dc.close()
    tables = {}
    pg_setup = (INPUT / "setup/postgres-setup.sql").read_text()
    statements = [_strip_leading_comments(s.text).strip() for s in split_sql_script(pg_setup)]
    # The reviewed input contains only these 21-table initial-state statements.
    with pg.connect(database=database) as connection:
        with connection.cursor() as c:
            for raw in statements:
                if not raw: continue
                node = sqlglot.parse_one(raw, read="postgres")
                if not isinstance(node, (exp.Create, exp.Insert)):
                    raise ValueError("准备输入不是经审查的 CREATE/INSERT")
                c.execute(raw)
                if isinstance(node, exp.Create):
                    table = node.this.this if isinstance(node.this, exp.Schema) else node.this
                    tables[table.name.lower()] = {"source_ddl": raw, "source_spelling": table.name}
            for table, filename in [("onek", "onek.data"), ("tenk1", "tenk.data"), ("aggtest", "agg.data")]:
                with c.copy(f"COPY {table} FROM STDIN") as copy:
                    copy.write((INPUT / "setup/data" / filename).read_bytes())
        target_sql = []
        for name, item in tables.items():
            with connection.cursor() as c:
                c.execute("SELECT column_name,data_type,udt_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position", (name,))
                columns = c.fetchall()
                c.execute(f'SELECT * FROM "{name}"')
                rows = c.fetchall()
            if not columns: raise RuntimeError(f"无法取得源表字段：{name}")
            for row in rows:
                if any(isinstance(v, str) and len(v.encode("utf-8")) > 512 for v in row):
                    raise RuntimeError("当前实际字符串超出目标 VARCHAR(512)，拒绝截断")
            definitions = ", ".join(f"`{col}` {TYPE_MAP[udt]} NULL" for col, _, udt in columns)
            ddl = f"CREATE TABLE `{name}` ({definitions}) DUPLICATE KEY(`{columns[0][0]}`) DISTRIBUTED BY HASH(`{columns[0][0]}`) BUCKETS 1 PROPERTIES ('replication_num'='1')"
            dc = target.connect(database=database)
            try:
                with dc.cursor() as c:
                    c.execute(ddl)
                    target_sql.append(ddl + ";")
                    for offset in range(0, len(rows), 100):
                        values = ",".join("(" + ",".join(sql_value(v) for v in row) + ")" for row in rows[offset:offset+100])
                        insert = f"INSERT INTO `{name}` VALUES {values}"
                        c.execute(insert)
                        target_sql.append(insert + ";")
                    if item["source_spelling"] != name:
                        alias = f"CREATE VIEW `{item['source_spelling']}` AS SELECT * FROM `{name}`"
                        c.execute(alias)
                        target_sql.append(alias + ";")
                    c.execute(f"DESCRIBE `{name}`")
                    item["target_columns"] = c.fetchall()
            finally: dc.close()
            item["source_columns"] = columns
            print(f"已新建并装数 {name}: {len(rows)} 行", flush=True)
        (folder / "doris-setup.sql").write_text("\n\n".join(target_sql) + "\n")
        source_script = pg_setup + "\n-- 下列 COPY 依赖由本目录 prepare 命令使用 cursor.copy 读取指定文件执行，不由验证器执行。\n"
        for name, fn in [("onek", "onek.data"), ("tenk1", "tenk.data"), ("aggtest", "agg.data")]:
            source_script += f"-- COPY {name} FROM STDIN，完整数据见 cases/postgres/manual/current/setup/data/{fn}\n"
        (folder / "postgres-setup.sql").write_text(source_script)
        # Compare full stored float values via DOUBLE, not a shortened float display.
        with connection.cursor() as c: c.execute("SET extra_float_digits = 3")
        for name, item in tables.items():
            columns = item["source_columns"]
            source_projection = ",".join(f'CAST("{col}" AS DOUBLE PRECISION)' if udt in {"float4", "float8"} else f'"{col}"' for col, _, udt in columns)
            target_projection = ",".join(f"CAST(`{col}` AS DOUBLE)" if udt in {"float4", "float8"} else f"`{col}`" for col, _, udt in columns)
            with connection.cursor(binary=True) as c:
                c.execute(f'SELECT {source_projection} FROM "{name}"')
                source_rows = c.fetchall()
            dc = target.connect(database=database)
            try:
                with dc.cursor() as c:
                    c.execute(f"SELECT {target_projection} FROM `{name}`")
                    actual = c.fetchall()
            finally: dc.close()
            sb, sh = bag_evidence(source_rows)
            tb, th = bag_evidence(actual)
            item.update(row_count=len(source_rows), target_row_count=len(actual), source_digest=sh, target_digest=th, complete_record_multiset_equal=sb == tb, null_cells=sum(v is None for row in source_rows for v in row), duplicate_rows=sum(n-1 for n in sb.values()))
            if sb != tb: raise RuntimeError(f"完整记录不一致：{name}；不会开始首轮验证")
        print("21 张逻辑表/视图的完整记录核验完成；开始重新核对当前 PG 与官方输出", flush=True)
        baselines = source_baselines(connection, scope)
        with connection.cursor() as c:
            c.execute("SELECT version(),current_database(),current_setting('TimeZone'),current_setting('DateStyle'),current_setting('extra_float_digits')")
            pg_environment = c.fetchone()
    dc = target.connect(database=database)
    try:
        with dc.cursor() as c:
            c.execute("SHOW FRONTENDS")
            fields = [d[0] for d in c.description]
            frontends = [dict(zip(fields, r)) for r in c.fetchall()]
    finally: dc.close()
    verification = {"database": database, "finished_at": datetime.now(timezone.utc).isoformat(), "scope_sha256": fingerprint(INPUT / "scope.json"), "tables": tables,
        "postgres_environment": pg_environment, "doris_frontends": frontends,
        "record_rule": "全记录多重集合，保留 NULL/重复；float4/float8 双端转 DOUBLE 并按 binary64 精确比较，普通字符串不做 JSON/空格归一化",
        "source_baselines": baselines,
        "type_limits": "TEXT/VARCHAR/NAME→VARCHAR(512)只证明本批实际记录可无损表示；约束、无限类型域和查询返回类型未证明相同；PG 视图 gstest1 在目标用相同记录表表示。"}
    dump(folder / "data-verification.json", verification)
    report_preparation(verification)
    print(f"数据准备报告：{folder/'data-preparation.md'}", flush=True)


def reverify():
    """Recheck only the previously created, traceable sample DB; no DB writes."""
    scope = load_scope()
    folder = OUTPUT / "data-preparation"
    path = folder / "data-verification.json"
    evidence = json.loads(path.read_text())
    marker = json.loads((folder / "execution-start.json").read_text())
    database = evidence["database"]
    if not re.fullmatch(r"dsv_pg_manual_[a-z0-9_]+", database) or marker["database"] != database or marker["scope_sha256"] != fingerprint(INPUT / "scope.json"):
        raise RuntimeError("不能确认本批原有专用库与相同输入，拒绝复用")
    evidence["preparation_action"] = "只读核验专用库的结构与完整记录；不重复建表或装数"
    evidence["reverification_started_at"] = datetime.now(timezone.utc).isoformat()
    pg, target = PostgresAdapter(), DorisAdapter()
    try:
        with pg.connect(database=database) as connection:
            with connection.cursor() as c:
                c.execute("SET default_transaction_read_only = on")
                c.execute("SET statement_timeout = '5s'")
                c.execute("SET extra_float_digits = 3")
            for name, item in evidence["tables"].items():
                if not re.fullmatch(r"[a-z0-9_]+", name):
                    raise ValueError("不安全的准备记录表名")
                with connection.cursor() as c:
                    c.execute("SELECT column_name,data_type,udt_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position", (name,))
                    columns = [list(row) for row in c.fetchall()]
                if columns != item["source_columns"]:
                    raise RuntimeError(f"源表结构已改变：{name}")
                source_projection = ",".join(f'CAST("{col}" AS DOUBLE PRECISION)' if udt in {"float4", "float8"} else f'"{col}"' for col, _, udt in columns)
                target_projection = ",".join(f"CAST(`{col}` AS DOUBLE)" if udt in {"float4", "float8"} else f"`{col}`" for col, _, udt in columns)
                with connection.cursor(binary=True) as c:
                    c.execute(f'SELECT {source_projection} FROM "{name}"')
                    source_rows = c.fetchall()
                dc = target.connect(database=database)
                try:
                    with dc.cursor() as c:
                        c.execute(f"DESCRIBE `{name}`")
                        if [list(row) for row in c.fetchall()] != item["target_columns"]:
                            raise RuntimeError(f"目标表结构已改变：{name}")
                        c.execute(f"SELECT {target_projection} FROM `{name}`")
                        actual = c.fetchall()
                        if item["source_spelling"] != name:
                            spelling = item["source_spelling"]
                            if not re.fullmatch(r"[A-Za-z0-9_]+", spelling): raise ValueError("不安全的别名")
                            c.execute(f"SELECT {target_projection} FROM `{spelling}`")
                            if bag_evidence(c.fetchall())[0] != bag_evidence(actual)[0]:
                                raise RuntimeError(f"大小写别名数据不一致：{spelling}")
                finally: dc.close()
                sb, sh = bag_evidence(source_rows)
                tb, th = bag_evidence(actual)
                # Keep the original expected data identity even after a failed
                # recheck; a retry must not bless newly changed records.
                item.setdefault("initial_source_digest", item["source_digest"])
                item.setdefault("initial_target_digest", item["target_digest"])
                original = (item["initial_source_digest"], item["initial_target_digest"])
                item.update(row_count=len(source_rows), target_row_count=len(actual), source_digest=sh, target_digest=th, complete_record_multiset_equal=sb == tb, null_cells=sum(v is None for row in source_rows for v in row), duplicate_rows=sum(n-1 for n in sb.values()), unchanged_since_initial_preparation=original == (sh, th))
                if sb != tb or original != (sh, th):
                    raise RuntimeError(f"双端数据不同或已偏离本批初始数据：{name}")
                print(f"重新完整核验 {name}: {len(source_rows)} 行，双端一致且未偏离初始数据", flush=True)
            evidence["source_baselines"] = source_baselines(connection, scope)
        evidence.pop("reverification_error", None)
    except Exception as exc:
        evidence["reverification_error"] = str(exc)
        for item in evidence["tables"].values(): item["complete_record_multiset_equal"] = False
        dump(path, evidence)
        (folder / "data-preparation.md").write_text("# 数据准备复核失败\n\n未完成一致数据复核，不进入本批首轮重跑。\n\n```text\n" + str(exc) + "\n```\n")
        raise
    evidence["finished_at"] = datetime.now(timezone.utc).isoformat()
    evidence["verification_script_sha256"] = fingerprint(Path(__file__))
    dump(path, evidence)
    record_environment()


def report_preparation(evidence):
    checks = Counter(c.get("reference_check", "参考输出无法解析") for c in evidence["source_baselines"])
    lines = ["# PostgreSQL → Doris 数据准备报告", "", "## 1. 实际完成范围", "",
        f"评估库：`{evidence['database']}`。以下记录对应数据阶段的结构、完整记录核验和类型映射限制。",
        f"已准备并完整核验 {len(evidence['tables'])} 张逻辑表/视图，共 {sum(t['row_count'] for t in evidence['tables'].values())} 行。当前实际数据一致，不代表两端类型域和约束完全相同。",
        "核验范围为 20 个官方脚本固定选择的 753 条查询，不是官方全量脚本回放。查询 SQL 与官方 .out 原件保持不变。", "",
        "## 2. 数据阶段与输入", "", "所有样本对应 setup/postgres-setup.sql 和三个官方 COPY 文件构成的固定初始阶段，旧脚本中其他临时表、后续 UPDATE/复用阶段不在本轮范围。当前 PG 的 753 条源结果已重新执行核对，结果不对应的记录另外列出。",
        "原始输入、源脚本位置和官方 commit 见 cases/postgres/manual/current/scope.json。",
        "postgres-setup.sql 为源 CREATE/INSERT，COPY 数据由 scripts/pg_manual_sample.py --prepare 使用 cursor.copy 从固定 data 文件加载；doris-setup.sql 保存本批首次真实执行的目标 CREATE/INSERT/view 语句。本轮若为复核，则保留这些脚本但不重复执行。", "",
        "## 3. 逐表完整记录核验与类型映射", "", "| 表 | 源/目标行数 | 重复记录数 | NULL 单元格数 | 完整记录 | 字段映射 |", "| :--- | :--- | ---: | ---: | :--- | :--- |"]
    for name, t in evidence["tables"].items():
        types = ", ".join(f"{c}: {u}→{TYPE_MAP[u]}" for c, _, u in t["source_columns"])
        lines.append(f"| {name} | {t['row_count']}/{t['target_row_count']} | {t['duplicate_rows']} | {t['null_cells']} | 一致 | {types} |")
    lines += ["", "完整记录按多重集合比较，不仅是 COUNT/抽样。FLOAT 两端显式转 DOUBLE，PG 使用二进制读取，逐值按 float.hex 检查真实存储值；不采用浮点容差。NULL、空字符串和重复次数保留。", "",
        "类型限制：TEXT、无长度 VARCHAR、NAME 映射为 VARCHAR(512)，本批 UTF-8 字节长度全部检查，不截断。INTEGER 位宽和 DATE 保持对应；Doris DUPLICATE KEY 保留重复记录。源 PK/FK 约束及全类型域不是本轮核验目标。源大小写名称在 Doris 创建同记录 view，源 SQL 不因此改写。", "",
        "## 4. 当前 PG 与历史预期输出的重新核对", "", "| 检查结果 | 查询数 |", "| :--- | ---: |"]
    for result, count in checks.items(): lines.append(f"| {result} | {count} |")
    lines += ["", "成功结果按原生 PG 文本与官方 aligned .out 的行值/重复次数核对，不能恢复 .out 丢失的类型或 NULL 表示细节；负向用例仅确认两边都失败，不宣称同因。输出不可解析或当前源结果不同的记录保留在 data-verification.json，不静默视为通过，也不修改官方答案。", "",
        "## 5. 版本、Session、证据与下一步", "", f"PostgreSQL 环境（版本/数据库/时区/日期格式/浮点额外显示位）：`{evidence['postgres_environment']}`。",
        "Doris 的实际版本及 PG 错误 SQLSTATE 在 data-verification.json。沿用本批首次创建时的 PG 库配置；源查询核验时仅设置当前 PG Session 的 UTC、ISO/MDY、extra_float_digits=0、5s statement_timeout，不修改旧库、表数据或全局配置；Doris 使用原有 Session 政策。",
        "步骤二调用 scripts/pg_manual_sample.py --validate：当前 Importer 生成只读 Query YAML，再通过当前 CLI 的 Recorded Output 路径仅执行 Doris。默认拒绝覆盖已有产物；替换报告需另行确认输出范围。数据准备报告不是验证器内部 Gate，不会连接到 AI 归因/修复。", ""]
    (OUTPUT / "data-preparation/data-preparation.md").write_text("\n".join(lines))


def record_environment():
    """Supplement this run's preparation evidence using read-only metadata."""
    path = OUTPUT / "data-preparation/data-verification.json"
    evidence = json.loads(path.read_text())
    database = evidence["database"]
    pg, target = PostgresAdapter(), DorisAdapter()
    with pg.connect(database=database) as connection:
        with connection.cursor() as c:
            c.execute("SELECT version(),datcollate,datctype,current_setting('TimeZone'),current_setting('DateStyle'),current_setting('extra_float_digits'),current_setting('statement_timeout') FROM pg_database WHERE datname=current_database()")
            fields = ["version", "lc_collate", "lc_ctype", "TimeZone", "DateStyle", "extra_float_digits", "statement_timeout"]
            evidence["postgres_session"] = dict(zip(fields, c.fetchone()))
    dc = target.connect(database=database)
    try:
        with dc.cursor() as c:
            values = {}
            for name in ["time_zone", "sql_mode", "enable_strict_cast", "enable_decimal256", "enable_nereids_planner"]:
                c.execute(f"SHOW VARIABLES LIKE '{name}'")
                rows = c.fetchall()
                values[name] = rows[0][1] if rows else "当前版本未提供该变量"
            evidence["doris_session"] = values
    finally: dc.close()
    evidence["environment_captured_at"] = datetime.now(timezone.utc).isoformat()
    dump(path, evidence)
    report_preparation(evidence)
    with (OUTPUT / "data-preparation/data-preparation.md").open("a") as f:
        f.write("\n## 6. 实际 Session 补查\n\n```json\n" + json.dumps({"PostgreSQL": evidence["postgres_session"], "Doris": evidence["doris_session"]}, ensure_ascii=False, indent=2) + "\n```\n\nSession 是当前连接实际值，没有修改 Doris 全局或 Session。时区、严格转换等不一致是后续归因需要单独检查的环境前提，不应直接算 SQLGlot 缺陷。\n")


def validate(*, resume=False, overwrite=False):
    if resume and overwrite: raise ValueError("续跑与覆盖重跑不能同时指定")
    scope = load_scope()
    verification = json.loads((OUTPUT / "data-preparation/data-verification.json").read_text())
    database = verification["database"]
    if not all(t["complete_record_multiset_equal"] for t in verification["tables"].values()):
        raise RuntimeError("外部准备尚未完成；请先处理，不修改验证器的执行逻辑")
    grouped = defaultdict(list)
    for item in scope["cases"]: grouped[item["file"]].append(item)
    runs = []
    for filename, selection in grouped.items():
        stem = Path(filename).stem
        output = INPUT / f"{stem}.yaml"
        output.parent.mkdir(parents=True, exist_ok=True)
        cf = import_case_file(INPUT / "assets" / filename, output, ImportOptions(input_format="pg-regress", dialect="postgres", source_engine="postgres", source_connection_profile="postgres-local", source_database=database, target_database=database, recorded_output=INPUT / "assets" / filename.replace(".sql", ".out")))
        allowed = {(int(c["id"].rsplit("-", 1)[1]), c["source_sql"].strip()) for c in selection}
        wanted_indices = {int(c["id"].rsplit("-", 1)[1]) for c in selection}
        selected = [c for c in cf.cases if (c.statement_index, c.sql.strip()) in allowed]
        retained = {(c.statement_index, c.sql.strip()) for c in selected}
        # Failed parsing/output lookup must not require a different report type.
        # Retry the exact selected SQL through run, whose guards and provider
        # record the first failing stage without bypassing read-only checks.
        for item in selection:
            index = int(item["id"].rsplit("-", 1)[1])
            if (index, item["source_sql"].strip()) not in retained:
                selected.append(CaseDefinition(
                    id=item["id"], statement_index=index,
                    line_start=item.get("line_start"), line_end=item.get("line_end"),
                    sql=item["source_sql"], output_occurrence=item["official_occurrence"],
                ))
        selected.sort(key=lambda c: c.statement_index)
        diagnostics = [d for d in cf.import_diagnostics if d.disposition == "skipped" or d.statement_index in wanted_indices]
        for c in cf.cases:
            if (c.statement_index, c.sql.strip()) not in allowed:
                diagnostics.append(ImportDiagnostic(statement_index=c.statement_index, line_start=c.line_start or 1, line_end=c.line_end or 1, disposition="skipped", statement_type="out_of_scope_query", reason="本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败"))
        counts = Counter(d.disposition for d in diagnostics)
        cf = cf.model_copy(update={"cases": selected, "import_diagnostics": diagnostics, "import_summary": ImportSummary(accepted=len(selected), skipped=counts["skipped"], ambiguous=counts["ambiguous"], errors=counts["error"])})
        destination = OUTPUT / "validation" / stem
        if overwrite and destination.exists():
            previous = destination / "validation.json"
            if previous.exists():
                saved = json.loads(previous.read_text())
                if saved["target"]["database"] != database or saved["input"]["sha256"] != cf.input.sha256 or saved["recorded_output"]["sha256"] != cf.recorded_output.sha256:
                    raise RuntimeError("已有报告不是本批相同输入/目标库，拒绝覆盖")
        if destination.exists() and not overwrite:
            if not resume: raise RuntimeError(f"报告目录已存在，拒绝覆盖：{destination}")
            payload = json.loads((destination / "validation.json").read_text())
            if load_case_file(output).definition != cf or payload["case_file"]["sha256"] != fingerprint(output):
                raise RuntimeError("本轮已完成报告与当前输入不对应，拒绝续跑")
            print(f"保留本轮已完成且 YAML 指纹不变的 {filename} 报告", flush=True)
        else:
            if output.exists() and not overwrite: raise RuntimeError(f"YAML 已存在但无本轮报告，拒绝覆盖：{output}")
            write_case_file(cf, output)
            destination.mkdir(parents=True, exist_ok=overwrite)
            # Actual latest CLI: .out route creates no PG adapter, does no setup/AI.
            command = [str(ROOT / ".venv/bin/doris-sql-validator"), "run", "--path", str(output), "--output-dir", str(destination)]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            if result.returncode not in (0, 1): raise RuntimeError(f"验证命令无法运行：{filename}\n{result.stdout}\n{result.stderr}")
            payload = json.loads((destination / "validation.json").read_text())
        runs.append({"file": filename, "selected_scope": len(selection), "accepted": len(selected), "in_scope_import_errors": counts["error"], "path": str(destination.relative_to(ROOT)), "summary": payload["summary"], "cases": payload["cases"]})
        print(f"{filename}: {len(selected)} 条，成功匹配 {payload['summary']['successful_matches']}，导入失败 {counts['error']}", flush=True)
    write_summary(scope, verification, runs)


def write_summary(scope, verification, runs):
    database = verification["database"]
    dump(OUTPUT / "validation-summary.json", {"database": database, "scope_count": len(scope["cases"]), "runs": [{k:v for k,v in r.items() if k != "cases"} for r in runs]})
    outcomes = Counter()
    for r in runs: outcomes.update(r["summary"]["outcomes"])
    n = sum(r["accepted"] for r in runs)
    matches = sum(r["summary"]["successful_matches"] for r in runs)
    negative = sum(r["summary"]["negative_source_cases"] for r in runs)
    import_errors = sum(r["in_scope_import_errors"] for r in runs)
    successful_rate = f"{matches/n:.2%}" if n else "未运行，不计算"
    lines = ["# PostgreSQL → Doris：最新流程首轮验证汇总", "", "## 1. 本轮范围和实际结果", "",
        f"独立评估库：`{database}`；输入来自 {len(runs)} 份官方脚本的固定 {len(scope['cases'])} 条样本范围，不是官方全量 SELECT。",
        f"当前 Importer 接受并交给运行器 {n} 条，导入失败 {import_errors} 条。运行器内 SQLGlot 转译失败 {outcomes['TRANSLATION_FAILED']} 条，未执行 Doris；其余继续取源证据并执行 Doris，具体状态见逐组报告。",
        f"两端成功且已有证据匹配 {matches} 条；占交给运行器查询 {matches}/{n} = {successful_rate}。其余含负向报错、转换失败、执行/结果差异，不等同于 SQLGlot 缺陷。",
        f"内部 MATCH 共 {outcomes['MATCH']} 条，其中成功结果匹配 {matches} 条、两端均报错且粗粒度类别相同 {outcomes['MATCH']-matches} 条。后者不能算成功结果匹配，也尚未证明错误同因。运行器实际读到的源端负向报错共 {negative} 条。",
        f"按原样本范围计算 {matches}/{len(scope['cases'])} = {matches/len(scope['cases']):.2%}；未被当前 Importer 接受的查询未计入执行分母，见各组导入诊断。",
        "先按数据准备 Skill 重新完整核验本批专用库，再使用当前框架 .out 模式验证；run 不连接 PG。固定验证只记录实际执行结果，不调用 AI 改写、归因或 SQLGlot 修复。", "",
        "## 2. 每组结果", "", "“进入运行器”包括随后转译失败的查询，不等于全部已发往 Doris。负向报错数仅统计运行器实际取得的参考输出；准备阶段另外执行了全部 753 条源 SQL。", "", "| 原始脚本 | 样本范围 | 进入运行器 | 成功结果匹配 | 源端负向报错 | 范围内导入失败 | 详细报告 |", "| :--- | ---: | ---: | ---: | ---: | ---: | :--- |"]
    for r in runs:
        lines.append(f"| {r['file']} | {r['selected_scope']} | {r['accepted']} | {r['summary']['successful_matches']} | {r['summary']['negative_source_cases']} | {r['in_scope_import_errors']} | [查看](validation/{Path(r['file']).stem}/validation.md) |")
    lines += ["", "## 3. 自动差异类别", "", "| 内部代码（含义见各组报告中文说明） | 查询数 |", "| :--- | ---: |"]
    from doris_sql_validator.report_labels import explain
    for key, count in sorted(outcomes.items()): lines.append(f"| {explain(key)}（`{key}`） | {count} |")
    lines += ["", f"MATCH 的成功/双端报错拆分见第一节。以上是运行器的互斥结果；{import_errors} 条导入失败不包含在这 {n} 条中。", "", "## 4. 导入阶段失败", "",
        "导入诊断不是 Doris 执行失败。解析失败的 SELECT 候选也保留在 YAML，通过普通 run 记录 TRANSLATION_FAILED 及具体阶段；未通过 Parser 和只读校验不会执行数据库。所有组统一使用 validation.md/json，不生成额外失败文档。保留数量与导入诊断数量可能重叠。", "",
        "输出定位规则：Importer 与 .out Parser 共用原文回显识别口径，不再把 AST 相同但原文不同的查询合并计数；字面量/引号标识符/注释之外的空白行差异可匹配，受保护内容内部仍按原内容识别。读取结果时要求紧邻本条回显，不向后借用另一条查询的输出或错误。源 SQL、.out、SQLGlot 和比较规则没有因此修改。以下列出本次导入诊断。", "",
        "| 原始脚本 | 语句编号 | 导入失败原因 |", "| :--- | ---: | :--- |"]
    from doris_sql_validator.report_labels import cell
    for r in runs:
        folder = ROOT / r["path"]
        diagnostics = json.loads((folder / "validation.json").read_text())["import_diagnostics"]
        for d in diagnostics:
            if d["disposition"] in {"error", "ambiguous"}:
                reason = re.sub(r"\x1b\[[0-9;]*m", "", d["reason"])
                lines.append(f"| {r['file']} | {d['statement_index']} | {cell(reason)} |")
    lines += ["", "### 上轮 9 条输出定位失败的本轮回归", "", "本表只说明是否恢复读取及随后实际自动比较结果；读取成功不等于 SQLGlot/Doris 已正确。", "", "| 原始脚本 | 语句编号 | 当前导入 | 本轮运行结果 |", "| :--- | ---: | :--- | :--- |"]
    previously_unreadable = {"join": [27, 29], "with": [27, 28, 29, 31], "date": [260], "timestamp": [139], "time": [41]}
    for stem, indices in previously_unreadable.items():
        report_path = OUTPUT / "validation" / stem / "validation.json"
        records = json.loads(report_path.read_text())["cases"] if report_path.exists() else []
        indices_by_id = {c.id: c.statement_index for c in load_case_file(INPUT / f"{stem}.yaml").definition.cases} if records else {}
        for index in indices:
            record = next((c for c in records if indices_by_id.get(c["id"]) == index), None)
            if record:
                lines.append(f"| {stem}.sql | {index} | 已接受并进入运行器 | {cell(explain(record['comparison']['observed_outcome']))} |")
            else:
                lines.append(f"| {stem}.sql | {index} | 未进入运行器 | 查看该组导入诊断；不能算通过 |")
    checks = Counter(c.get("reference_check", "参考输出无法解析") for c in verification["source_baselines"])
    baselines = verification["source_baselines"]
    positives = sum(c["source_success"] for c in baselines)
    negatives = len(baselines) - positives
    lines += ["", "## 5. 源参考输出与证据限制", "",
        f"数据准备阶段重新执行全部 {len(baselines)} 条 PG 查询：{positives} 条成功、{negatives} 条负向报错。参考输出解析失败与转译先失败后未取得源证据的情况不同，前者已计入导入诊断。",
        f"本次源参考核对实际统计：{dict(checks)}。",
        "负向用例不计入成功匹配；同类粗粒度错误不等于同因。参考 .out 通常不提供原生类型，MATCH 不表示完整类型、所有输入、排序唯一性或相关边界通过。",
        "当前数据与原始输入核验见 [data-preparation.md](data-preparation/data-preparation.md) 和 [data-verification.json](data-preparation/data-verification.json)。当前 PG 与 .out 不对应或无法解析的项目均保留，归因时需先阅读。",
        "两端 Session 实际值见数据准备报告；时区或转换模式不一致也可能造成差异，不能在尚未归因时全部算 SQLGlot 问题。",
        "归因与修复由用户另行显式调用；确定性验证命令不会自动启动这些阶段。",
        "不同运行应使用明确的输出目录；公开范围见 docs/PUBLISHING.md。", ""]
    (OUTPUT / "SUMMARY.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="当前人工链路的固定官方样本复现；不调用任何 AI")
    parser.add_argument("--collect-from", type=Path, help="首次只复制既有官方样本输入和语句选择，不复制旧结果")
    parser.add_argument("--prepare", action="store_true", help="显式新建独立双端数据库、装数和核验；拒绝复用已存在数据库")
    parser.add_argument("--reverify", action="store_true", help="只读重新核验本批已创建的专用库、完整记录和当前 PG/.out，不清库或重复装数")
    parser.add_argument("--validate", action="store_true", help="显式调用当前 Importer/CLI 运行 Recorded Output 首轮验证")
    parser.add_argument("--resume", action="store_true", help="仅续跑本轮中断的验证：核对已完成 YAML/报告指纹，不覆盖或重跑它们")
    parser.add_argument("--overwrite", action="store_true", help="仅在明确授权时覆盖本批 current YAML/报告并重新执行，不复用上一轮运行结果")
    parser.add_argument("--summarize", action="store_true", help="仅重新渲染本轮汇总，不连接数据库、不改逐组原始报告")
    parser.add_argument("--record-environment", action="store_true", help="只读补记当前双端 Session，不改库表或设置")
    parser.add_argument("--database", default="dsv_pg_manual_20261111")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    logging.getLogger("sqlglot").setLevel(logging.ERROR)
    if args.collect_from: collect_inputs(args.collect_from)
    if args.prepare: prepare(args.database)
    if args.reverify: reverify()
    if args.record_environment: record_environment()
    if args.validate: validate(resume=args.resume, overwrite=args.overwrite)
    if args.summarize:
        verification = json.loads((OUTPUT / "data-preparation/data-verification.json").read_text())
        runs = json.loads((OUTPUT / "validation-summary.json").read_text())["runs"]
        write_summary(load_scope(), verification, runs)
    if not any((args.collect_from, args.prepare, args.reverify, args.validate, args.summarize, args.record_environment)): parser.print_help()


if __name__ == "__main__": main()
