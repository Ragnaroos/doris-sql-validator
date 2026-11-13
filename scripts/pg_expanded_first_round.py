#!/usr/bin/env python3
"""Explicit local corpus expansion; setup/LLM calls are not part of the validator."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
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
from doris_sql_validator.models import (
    CaseDefinition, CaseFile, ImportDiagnostic, ImportSummary, InputSpec,
    RecordedOutputSpec, SourceSpec, TargetSpec,
)
from doris_sql_validator.report_labels import explain
from doris_sql_validator.sql_utils import file_sha256
from pg_manual_sample import bag_evidence


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "cases/postgres/manual/current"
EXTRA = ROOT / "cases/postgres/out-reader-samples"
INPUT = SEED / "expanded"
OUTPUT = ROOT / "reports/pg-manual/current"
NONDETERMINISTIC = {
    "random", "rand", "now", "version", "clock_timestamp", "statement_timestamp",
    "transaction_timestamp", "timeofday", "current_setting", "set_config",
    "nextval", "currval", "setval", "pg_sleep", "pg_backend_pid", "gen_random_uuid",
}


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def fingerprint(path: Path) -> str:
    return file_sha256(path.read_bytes())


def check_environment():
    """Read-only external check; does not alter the prior preparation evidence."""
    original_path = OUTPUT / "data-preparation/data-verification.json"
    original = json.loads(original_path.read_text())
    database = original["database"]
    if not re.fullmatch(r"dsv_pg_manual_[a-z0-9_]+", database):
        raise ValueError("不能确认已有独立测试库，停止，不新建或修改库表")
    pg, doris = PostgresAdapter(), DorisAdapter()
    evidence = {
        "database": database, "checked_at": datetime.now(timezone.utc).isoformat(),
        "original_preparation_sha256": fingerprint(original_path),
        "action": "框架外只读复核原有 21 张表/视图；未执行 DDL/DML/导入或 AI。",
        "tables": {},
    }
    with pg.connect(database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SET default_transaction_read_only = on")
            cursor.execute("SET statement_timeout = '5s'")
            cursor.execute("SET extra_float_digits = 3")
            cursor.execute("SELECT version(), current_setting('TimeZone'), current_setting('DateStyle')")
            evidence["postgres_environment"] = cursor.fetchone()
            cursor.execute("SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='pg_catalog'")
            builtin_functions = {row[0].lower() for row in cursor.fetchall()}
            cursor.execute("SELECT t.typname FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='pg_catalog'")
            builtin_types = {row[0].lower() for row in cursor.fetchall()}
        for name, saved in original["tables"].items():
            if not re.fullmatch(r"[a-z0-9_]+", name):
                raise ValueError("准备证据中包含不安全的对象名")
            with connection.cursor() as cursor:
                cursor.execute("SELECT column_name,data_type,udt_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position", (name,))
                columns = [list(row) for row in cursor.fetchall()]
                if columns != saved["source_columns"]:
                    raise RuntimeError(f"源表结构已改变：{name}")
            source_columns = ",".join(f'CAST("{col}" AS DOUBLE PRECISION)' if udt in {"float4", "float8"} else f'"{col}"' for col, _, udt in columns)
            target_columns = ",".join(f"CAST(`{col}` AS DOUBLE)" if udt in {"float4", "float8"} else f"`{col}`" for col, _, udt in columns)
            with connection.cursor(binary=True) as cursor:
                cursor.execute(f'SELECT {source_columns} FROM "{name}"')
                source_rows = cursor.fetchall()
            target_connection = doris.connect(database=database)
            try:
                with target_connection.cursor() as cursor:
                    cursor.execute(f"DESCRIBE `{name}`")
                    if [list(row) for row in cursor.fetchall()] != saved["target_columns"]:
                        raise RuntimeError(f"目标表结构已改变：{name}")
                    cursor.execute(f"SELECT {target_columns} FROM `{name}`")
                    target_rows = cursor.fetchall()
                    if saved["source_spelling"] != name:
                        alias = saved["source_spelling"]
                        if not re.fullmatch(r"[A-Za-z0-9_]+", alias):
                            raise ValueError("不安全的大小写别名")
                        cursor.execute(f"SELECT {target_columns} FROM `{alias}`")
                        if bag_evidence(cursor.fetchall())[0] != bag_evidence(target_rows)[0]:
                            raise RuntimeError(f"别名数据不一致：{alias}")
            finally:
                target_connection.close()
            source_bag, source_digest = bag_evidence(source_rows)
            target_bag, target_digest = bag_evidence(target_rows)
            initial = (saved.get("initial_source_digest", saved["source_digest"]), saved.get("initial_target_digest", saved["target_digest"]))
            if source_bag != target_bag or initial != (source_digest, target_digest):
                raise RuntimeError(f"数据不同或偏离最初准备状态：{name}")
            evidence["tables"][name] = {
                "rows": len(source_rows), "source_digest": source_digest,
                "target_digest": target_digest, "unchanged": True,
            }
            print(f"只读核验 {name}: {len(source_rows)} 行，一致且未改变", flush=True)
    target_connection = doris.connect(database=database)
    try:
        with target_connection.cursor() as cursor:
            cursor.execute("SHOW FRONTENDS")
            evidence["doris_frontends"] = [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]
            evidence["doris_session"] = {}
            for setting in ("time_zone", "sql_mode", "enable_strict_cast"):
                cursor.execute(f"SHOW VARIABLES LIKE '{setting}'")
                evidence["doris_session"][setting] = cursor.fetchall()
    finally:
        target_connection.close()
    evidence["builtin_catalog_sha256"] = hashlib.sha256(json.dumps([sorted(builtin_functions), sorted(builtin_types)]).encode()).hexdigest()
    return database, builtin_functions, builtin_types, evidence


def exclusion_reason(sql: str, builtins: set[str], created: set[str]) -> str | None:
    if "<!doctype" in sql.lower() or "<!entity" in sql.lower():
        return "XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询"
    node = sqlglot.parse_one(sql, read="postgres")
    if next(node.find_all(exp.Table), None) is not None:
        return "依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段"
    if any(getattr(t.this, "name", "") == "USERDEFINED" for t in node.find_all(exp.DataType)):
        return "依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象"
    for function in node.find_all(exp.Func):
        name = (function.name if isinstance(function, exp.Anonymous) else function.sql_name()).lower()
        if name in NONDETERMINISTIC or re.match(r"^(?:current_|localtime|localtimestamp)", name):
            return "依赖时间、随机、Session、版本或有状态函数；不作为固定输出回归"
        if name.startswith("pg_get_") or name in {"pg_basetype", "regtype", "regclass"}:
            return "依赖源库对象或系统目录状态；本次未准备相应对象"
        if name.startswith(("pg_read_", "pg_write_", "pg_ls_", "pg_advisory_", "pg_try_advisory_", "pg_terminate_", "pg_cancel_", "lo_", "dblink")):
            return "涉及文件、外部连接、锁或管理操作；不作为本轮只读结果验证"
        if isinstance(function, exp.Anonymous) and name not in builtins | {"row", "all", "any"}:
            return f"依赖自定义/无法确认的函数或构造器：{name}；本次不安装 UDF"
    for literal in node.find_all(exp.Literal):
        if not literal.is_string:
            continue
        text = literal.this.lower()
        if "<!doctype" in text or "<!entity" in text:
            return "XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询"
        if text in {"now", "today", "tomorrow", "yesterday"}:
            return "包含相对当前时间的输入；历史输出不能作为稳定基线"
        if text in created:
            return "字符串参数引用了原脚本创建的对象；本次未准备该对象"
    return None


def prepare_inputs(database: str, builtins: set[str]):
    prepare_seed_parser_cases(database)
    assets = INPUT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    scope = {"database": database, "selection_rule": "保留原有 750 条已准备数据用例；新增仅纳入无表引用、无自定义对象依赖且输出可固定的查询。未修改源 SQL 或官方答案。", "groups": [], "deferred_cases": []}
    groups = []
    for path in sorted(SEED.glob("*.yaml")):
        definition = load_case_file(path).definition
        groups.append({"name": path.stem, "yaml": str(path.relative_to(ROOT)), "queries": len(definition.cases), "import_errors": definition.import_summary.errors})
    # Copy all new originals so each generated YAML remains self-contained.
    for path in sorted(EXTRA.rglob("*.yaml")):
        old = load_case_file(path).definition
        raw_path = path.parent / old.input.file
        out_path = path.parent / old.recorded_output.file
        if fingerprint(raw_path) != old.input.sha256 or fingerprint(out_path) != old.recorded_output.sha256:
            raise RuntimeError(f"输入指纹改变：{path}")
        raw = raw_path.read_text()
        created = {m.group(1).lower() for m in re.finditer(r'(?i)CREATE\s+(?:OR\s+REPLACE\s+)?(?:FUNCTION|TYPE|DOMAIN)\s+"?([A-Za-z_][A-Za-z_0-9]*)', raw)}
        selected, diagnostics = [], list(old.import_diagnostics)
        for case in old.cases:
            reason = exclusion_reason(case.sql, builtins, created)
            if reason:
                scope["deferred_cases"].append({"file": raw_path.name, "case_id": case.id, "source_sql": case.sql, "reason": reason})
                diagnostics.append(ImportDiagnostic(statement_index=case.statement_index, line_start=case.line_start or 1, line_end=case.line_end or 1, disposition="skipped", statement_type="deferred_environment_dependency", reason=reason))
            else:
                selected.append(case)
        info = {"name": path.stem, "available_readable_queries": len(old.cases), "queries": len(selected), "deferred": len(old.cases)-len(selected), "import_errors": old.import_summary.errors}
        for original in (raw_path, out_path):
            destination = assets / original.name
            if destination.exists() and fingerprint(destination) != fingerprint(original):
                raise RuntimeError(f"不覆盖不同内容的输入：{destination}")
            shutil.copyfile(original, destination)
        if selected:
            counts = Counter(d.disposition for d in diagnostics)
            definition = old.model_copy(deep=True)
            definition.source.database = database
            definition.target.database = database
            definition.cases = selected
            definition.import_diagnostics = diagnostics
            definition.import_summary = ImportSummary(accepted=len(selected), skipped=counts["skipped"], errors=counts["error"], ambiguous=counts["ambiguous"])
            target = INPUT / f"{path.stem}.yaml"
            write_case_file(definition, target)
            load_case_file(target)
            info["yaml"] = str(target.relative_to(ROOT))
            groups.append(info)
        scope["groups"].append(info)
        print(f"新增 {path.stem}: 纳入 {len(selected)}，暂不运行 {info['deferred']}", flush=True)
    scope["runtime_groups"] = groups
    scope["original_seed_parser_failure_candidates"] = 3
    dump(INPUT / "selection.json", scope)
    return scope


def archive_previous() -> Path:
    archive = ROOT / "reports/pg-manual/archive" / ("first-round-before-expansion-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    archive.mkdir(parents=True, exist_ok=False)
    inventory = []
    # Exact generated first-round paths only; never move preparation/handoff.
    for name in ("validation", "validation.md", "validation.json", "SUMMARY.md", "validation-summary.json", "environment-check.json"):
        source = OUTPUT / name
        if not source.exists():
            continue
        files = sorted(source.rglob("*")) if source.is_dir() else [source]
        inventory.extend({"original_path": str(p.relative_to(ROOT)), "sha256": fingerprint(p)} for p in files if p.is_file())
        shutil.move(str(source), str(archive / name))
    dump(archive / "archive-index.json", inventory)
    return archive


def prepare_seed_parser_cases(database: str):
    """Keep the selected unsupported queries in the same YAML/run path."""
    scope = json.loads((SEED / "scope.json").read_text())
    rejected = [c for c in scope["cases"] if c["file"] == "select_distinct_on.sql"]
    source = SEED / "assets/select_distinct_on.sql"
    output = SEED / "assets/select_distinct_on.out"
    definition = CaseFile(
        source=SourceSpec(dialect="postgres", engine="postgres", connection_profile="postgres-local", database=database),
        target=TargetSpec(database=database),
        input=InputSpec(format="pg-regress", file="assets/select_distinct_on.sql", sha256=fingerprint(source)),
        recorded_output=RecordedOutputSpec(format="pg-regress", file="assets/select_distinct_on.out", sha256=fingerprint(output)),
        import_summary=ImportSummary(accepted=len(rejected), skipped=0, ambiguous=0, errors=0),
        cases=[CaseDefinition(id=c["id"], statement_index=i, line_start=c["line_start"], line_end=c["line_end"],
                              sql=c["source_sql"], output_occurrence=c["official_occurrence"])
               for i, c in enumerate(rejected, 1)],
    )
    write_case_file(definition, SEED / "select_distinct_on.yaml")


def summarize(scope, archive: Path):
    runs = []
    outcomes = Counter()
    sql_texts = set()
    for group in scope["runtime_groups"]:
        report_path = OUTPUT / "validation" / group["name"] / "validation.json"
        payload = json.loads(report_path.read_text())
        if payload["case_file"]["sha256"] != fingerprint(ROOT / group["yaml"]):
            raise RuntimeError("报告与 YAML 指纹不一致")
        statistics = payload["summary"]
        sql_texts.update(case["source_sql"].strip() for case in payload["cases"])
        outcomes.update(statistics["outcomes"])
        # Older selection manifests may contain a batch-specific 'kind'. It
        # describes input folders, not execution history; never publish it.
        runs.append({**{k: v for k, v in group.items() if k != "kind"}, "summary": statistics, "report": str(report_path.relative_to(ROOT))})
    total = sum(r["queries"] for r in runs)
    success = sum(r["summary"]["successful_matches"] for r in runs)
    negative = sum(r["summary"]["negative_source_cases"] for r in runs)
    executed = sum(r["queries"] - r["summary"]["translation_failed"] - r["summary"]["source_evidence_failed"] for r in runs)
    dump(OUTPUT / "validation-summary.json", {"database": scope["database"], "total": total, "distinct_sql_texts": len(sql_texts), "successful_matches": success, "outcomes": dict(outcomes), "archive": str(archive.relative_to(ROOT)), "runs": runs,
         "report_update_note": scope.get("report_update_note")})
    lines = ["# PostgreSQL → Doris：扩展语料首轮验证报告", "", "## 1. 本轮结果", "",
        f"- 本次输入并进入验证器：**{total} 条用例**。报告统计来自本次运行结果，不按历史运行情况区分新旧 SQL。",
        f"- 按源 SQL 原文去重为 **{len(sql_texts)} 条**；同文但来源/用例编号不同的记录保留，数量与去重 SQL 数分开说明。",
        f"- 两端成功且参考输出匹配：**{success} 条（{success/total:.2%}）**。这是固定数据与现有文本证据下的匹配率，不是完整语义证明。",
        f"- SQLGlot 转译失败：**{outcomes['TRANSLATION_FAILED']} 条**；实际取得 Doris 执行结果：**{executed} 条**。",
        f"- 运行时读取到源端报错的负向用例：**{negative} 条**；其中 **{outcomes['MATCH']-success} 条**两端粗粒度错误类别相同，不计入成功匹配，也不证明同因。",
        f"- 测试库：`{scope['database']}`。源结果读官方 `.out`；验证器只执行 Doris。没有执行 AI 改写、归因或修复。", "",
        "## 2. 范围与数据前提", "",
        "本批表查询使用已准备的 21 张逻辑表/视图；运行前在框架外只读检查了结构、完整记录和初始指纹。证据见 [environment-check.json](environment-check.json)，数据准备文件没有删除或改写。",
        "另外两批 20 组官方脚本中，仅纳入不引用表、没有自定义类型/函数依赖且可固定输出的查询；未运行新的 DDL/DML，没有为新表编造数据。含表值函数的查询也保守留待数据准备。这是本批输入的准备条件，不是验证器对执行历史的记忆。",
        f"本批可读取但因环境/对象、确定性或外部资源安全条件未纳入：**{len(scope['deferred_cases'])} 条**。完整 SQL、排除原因和每组数量见 [selection.json](../../../cases/postgres/manual/current/expanded/selection.json)；未纳入不表示通过。",
        "3 条 ORDER BY ... USING 查询已纳入普通 YAML 和本轮查询总数；SQLGlot Parser 拒绝的语法记为转译失败，后续参考输出读取、Doris 执行及比较未执行。原文和错误见 [该组验证报告](validation/select_distinct_on/validation.md)。其他未保留为 Case 的导入诊断不计入运行查询分母，也不能直接归为 SQLGlot 缺陷。",
        "`.out` 缺少原生类型和完整 NULL 表示信息；类型、Session、数据库能力、Adapter、比较器或数据前提仍可能导致差异。首轮报告只描述观察到的结果，不提前把不匹配归因给 SQLGlot。", "",
        "## 3. 互斥结果分类", "", "| 结果 | 查询数 |", "| :--- | ---: |"]
    for outcome, count in sorted(outcomes.items()):
        lines.append(f"| {explain(outcome)}（`{outcome}`） | {count} |")
    lines += ["", "MATCH 包含两端同类报错；成功匹配数已在第一节单独统计。环境错误也单独保留，不隐藏在 SQLGlot 缺陷中。", "", "## 4. 分组详细报告", "", "| 输入文件 | 查询数 | 成功结果匹配 | SQLGlot 转译失败 | 详细报告 |", "| :--- | ---: | ---: | ---: | :--- |"]
    for run in runs:
        stats = run["summary"]
        lines.append(f"| {run['name']}.sql | {run['queries']} | {stats['successful_matches']} | {stats['translation_failed']} | [查看](validation/{run['name']}/validation.md) |")
    lines += ["", "## 5. 未进入执行与后续处理", "",
        "- 没有选中查询的输入脚本：" + ("、".join(g["name"] for g in scope["groups"] if not g["queries"]) or "无") + "。依赖本轮未准备的表或对象时不执行，不能把空结果算成通过。",
        "- 所有已运行查询的源 SQL、生成的 Doris SQL、执行错误与比较差异见逐组报告；匹配条目简写，不匹配及负向错误条目展开。",
        "- 旧首轮报告已从 current 移除，恢复副本位于 `" + str(archive.relative_to(ROOT)) + "`，默认不发布到远程。数据准备和其他历史归因文件未删除。",
        "- 下一步可以由人调用归因 Skill 分析本轮报告；本次没有自动执行该步骤。", ""]
    if scope.get("report_update_note"):
        lines += ["本次报告更新范围：" + scope["report_update_note"], ""]
    (OUTPUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"TOTAL {total}; successful matches {success}; report {OUTPUT/'SUMMARY.md'}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-and-replace", action="store_true", help="明确替换旧首轮报告，并实际执行 Doris")
    arguments = parser.parse_args()
    load_dotenv(ROOT / ".env")
    logging.getLogger("sqlglot").setLevel(logging.ERROR)
    database, builtin_functions, builtin_types, environment = check_environment()
    scope = prepare_inputs(database, builtin_functions | builtin_types)
    print("Prepared", sum(g["queries"] for g in scope["runtime_groups"]), "queries", flush=True)
    if not arguments.run_and_replace:
        dump(INPUT / "environment-check.json", environment)
        return
    archive = archive_previous()
    dump(OUTPUT / "environment-check.json", environment)
    print("Previous reports moved to", archive, flush=True)
    for group in scope["runtime_groups"]:
        destination = OUTPUT / "validation" / group["name"]
        command = [str(ROOT / ".venv/bin/doris-sql-validator"), "run", "--path", str(ROOT / group["yaml"]), "--output-dir", str(destination)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        if result.returncode not in {0, 1} or not (destination / "validation.json").exists():
            raise RuntimeError(f"运行失败，未伪造报告：{group['name']}\n{result.stdout}\n{result.stderr}")
        stats = json.loads((destination / "validation.json").read_text())["summary"]
        print(group["name"], "queries=", group["queries"], "successful_matches=", stats["successful_matches"], "translation_failed=", stats["translation_failed"], flush=True)
    summarize(scope, archive)


if __name__ == "__main__":
    main()
