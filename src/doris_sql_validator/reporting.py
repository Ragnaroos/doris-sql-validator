"""One compact validation JSON: run identity, summary, one record per query."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .comparison import _is_environment_error
from .models import CaseRunReport, LoadedCaseFile, SuiteReport
from .report_labels import ERRORS, explain
from .sql_utils import file_sha256


def load_validation_report(path: Path) -> dict[str, Any]:
    """Read the compact report used directly by attribution and probes."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"无法读取验证 JSON {path}：{exc}") from exc
    if not isinstance(document, dict) or set(document) != {"run", "summary", "queries"}:
        raise ValueError("验证报告必须包含 run、summary、queries 三部分；请重新运行生成报告")
    if not isinstance(document["run"], dict) or not isinstance(document["summary"], dict) or not isinstance(document["queries"], list):
        raise ValueError("验证报告的 run/summary 必须是对象，queries 必须是查询记录列表")
    seen = set()
    for query in document["queries"]:
        if not isinstance(query, dict) or not all(query.get(key) for key in ("id", "source_sql", "result")):
            raise ValueError("查询记录缺少 id、source_sql 或 result")
        if query["id"] in seen:
            raise ValueError(f"验证报告存在重复查询编号：{query['id']}")
        seen.add(query["id"])
    return document


def validate_report_inputs(document: dict[str, Any], loaded: LoadedCaseFile) -> None:
    """Check report/YAML/source correspondence in memory; never hash .out."""
    run, definition = document["run"], loaded.definition
    if run.get("source") != definition.source.model_dump(mode="json"):
        raise ValueError("报告源数据库配置与 YAML 不对应")
    target = {"dialect": "doris", "engine": "doris", **definition.target.model_dump(mode="json")}
    if run.get("target") != target:
        raise ValueError("报告目标数据库配置与 YAML 不对应")
    if run.get("validation_mode") != definition.validation_mode:
        raise ValueError("报告验证模式与 YAML 不对应")
    if run.get("case_file") and run["case_file"].get("sha256") != file_sha256(loaded.path.read_bytes()):
        raise ValueError("YAML 已在报告生成后修改，请重新运行验证")
    expected = definition.recorded_output
    if expected:
        recorded = run.get("recorded_output", {})
        actual_path = (loaded.base_dir / expected.file).resolve()
        if recorded.get("format") != expected.format or recorded.get("file") != str(actual_path):
            raise ValueError("报告与 YAML 引用的 .out 路径或格式不同")
    if definition.input.file:
        source_path = (loaded.base_dir / definition.input.file).resolve()
        if not source_path.is_file() or (
            definition.input.sha256 and file_sha256(source_path.read_bytes()) != definition.input.sha256
        ):
            raise ValueError("原始 SQL 文件不存在或已改变，请重新导入并运行验证")
    definitions = {case.id: case for case in definition.cases}
    definitions.update({d.case_id: d for d in definition.import_diagnostics if d.case_id and d.sql})
    for query in document["queries"]:
        original = definitions.get(query["id"])
        if original is None or query["source_sql"].strip() != original.sql.strip():
            raise ValueError(f"报告查询与 YAML 不对应：{query['id']}")


def write_reports(report: SuiteReport, output_path: Path, *, case_file_path: Path | None = None) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_validation_report(report, case_file_path=case_file_path)
    # Metadata is readable; each query is serialized once on one logical line.
    # SQL newlines are JSON-escaped, not removed (which could alter semantics).
    head = json.dumps({key: payload[key] for key in ("run", "summary")}, ensure_ascii=False, indent=2, default=str)
    records = ["    " + json.dumps(query, ensure_ascii=False, separators=(", ", ": "), default=str)
               for query in payload["queries"]]
    text = head[:-2] + ',\n  "queries": [\n' + ",\n".join(records) + "\n  ]\n}\n"
    output_path.write_text(text, encoding="utf-8")
    return output_path


def _error(error) -> dict[str, Any]:
    result = {"category": ERRORS.get(error.category, error.category), "message": error.message}
    if error.code is not None:
        result["code"] = error.code
    return result


def _source_status(case: CaseRunReport) -> str:
    if case.source_evidence is None:
        return "未取得"
    return "成功" if case.source_evidence.result.success else "报错"


def _query_record(case: CaseRunReport) -> dict[str, Any]:
    record: dict[str, Any] = {"id": case.id, "source_sql": case.source_sql}
    source = case.source_evidence.result if case.source_evidence else None
    target = case.target_result
    comparison = case.comparison
    source_status = _source_status(case)
    if source and not source.success:
        environment = source.error and _is_environment_error(source.error.category)
        result = "源端环境问题" if environment else "源端负向用例"
        action = "前提排查" if environment else "默认不归因"
        reason = "源端环境或对象前提不满足，不能据此判定转换缺陷" if environment else "源端本身报错，不计成功匹配，默认不安排独立改写"
    elif case.status == "TRANSLATION_FAILED":
        result, reason = "SQLGlot 转译失败", "源 SQL 解析失败" if case.failure_stage == "source_parse" else "SQLGlot 解析或生成失败"
        action = "归因" if source_status == "成功" else "补查源证据"
    elif case.source_evidence_error or source is None:
        result, action, reason = "源参考输出读取失败", "前提排查", "未取得可用源结果，不能据此判定转换缺陷"
    elif target is not None and not target.success:
        environment = target.error and _is_environment_error(target.error.category)
        result = "Doris 环境问题" if environment else "Doris 执行失败"
        action, reason = ("前提排查", "Doris 连接、库表或权限等前提不满足") if environment else ("归因", "源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error")
    elif comparison and comparison.observed_outcome == "MATCH":
        if comparison.equivalent is True and comparison.semantic_assessment != "INCONCLUSIVE":
            return {**record, "result": "匹配"}
        result, action, reason = "证据不足", "前提排查", "可用状态或字段未发现差异，但缺少结果值等必要证据"
    elif comparison:
        result = {"RESULT_SCHEMA_MISMATCH": "字段不匹配", "ROW_COUNT_MISMATCH": "行数不匹配", "ROW_VALUE_MISMATCH": "行值或顺序不匹配"}.get(comparison.observed_outcome, "结果不匹配")
        action, reason = "归因", explain(comparison.observed_outcome)
    else:
        result, action, reason = "证据不足", "前提排查", "未形成完整的执行或比较结论"

    record.update(result=result, action=action, source_status=source_status, reason=reason)
    if case.statement_index is not None:
        record["source_location"] = {"statement": case.statement_index}
        if case.line_start is not None:
            record["source_location"]["lines"] = [case.line_start, case.line_end or case.line_start]
    if case.target_sql and result != "源端负向用例":
        record["target_sql"] = case.target_sql
    if case.transpilation_error:
        record["transpilation_error"] = case.transpilation_error
        record["failure_stage"] = case.failure_stage
    if case.source_evidence_error:
        record["source_evidence_error"] = case.source_evidence_error
    if source and source.error:
        record["source_error"] = _error(source.error)
    if target:
        record["doris_status"] = "成功" if target.success else "报错"
        if target.error:
            record["doris_error"] = _error(target.error)
    if case.difference and result not in {"源端负向用例", "源端环境问题"}:
        record["difference"] = case.difference
    return record


def build_validation_report(report: SuiteReport, *, case_file_path: Path | None = None) -> dict[str, Any]:
    """Build the shared file/stdout payload without writing any artifacts."""
    records = [_query_record(case) for case in report.cases]
    known_positions = {case.statement_index for case in report.cases}
    # Output lookup failures dropped by Importer remain visible, without
    # duplicating SELECT parser errors that already have an ordinary record.
    if not report.filtered:
        for diagnostic in report.import_diagnostics:
            if diagnostic.sql and diagnostic.case_id and diagnostic.statement_index not in known_positions:
                records.append({"id": diagnostic.case_id, "source_sql": diagnostic.sql,
                    "result": "导入时参考输出读取失败", "source_status": "未取得", "action": "前提排查",
                    "reason": diagnostic.reason,
                    "source_location": {"statement": diagnostic.statement_index, "lines": [diagnostic.line_start, diagnostic.line_end]}})
                known_positions.add(diagnostic.statement_index)
    positions = {case.id: case.statement_index or index + 1 for index, case in enumerate(report.cases)}
    positions.update({d.case_id: d.statement_index for d in report.import_diagnostics if d.case_id})
    records.sort(key=lambda record: positions[record["id"]])
    matched = sum(query["result"] == "匹配" for query in records)
    source_success = sum(bool(case.source_evidence and case.source_evidence.result.success) for case in report.cases)
    outcomes = Counter(query["result"] for query in records)
    run: dict[str, Any] = {
        "started_at": report.started_at.isoformat(), "finished_at": report.finished_at.isoformat(),
        "sqlglot_version": report.sqlglot_version, "sqlglot_commit": report.sqlglot_commit,
        "validation_mode": report.validation_mode, "source": report.source.model_dump(mode="json"),
        "target": {"dialect": "doris", "engine": "doris", **report.target.model_dump(mode="json")},
        "input": report.input.model_dump(mode="json", exclude_none=True), "filtered": report.filtered,
        "comparison_rules": {"row_order": "最终有 ORDER BY 时逐行，否则忽略顺序但保留重复次数",
            "column_names": "仅识别到全部输出均为显式 Alias 时比较名称",
            "column_types": "仅源证据提供字段类型时比较", "typed_float_tolerance": 1e-12,
            "recorded_values": "按源输出显示文本比较，不自动套用数值容差"},
    }
    if case_file_path:
        run["case_file"] = {"path": str(case_file_path.resolve()), "sha256": file_sha256(case_file_path.read_bytes())}
        base = case_file_path.resolve().parent
        if report.input.file:
            run["input"]["file"] = str((base / report.input.file).resolve())
    if report.recorded_output:
        run["recorded_output"] = report.recorded_output.model_dump(mode="json", exclude_none=True)
        if case_file_path:
            run["recorded_output"]["file"] = str((case_file_path.resolve().parent / report.recorded_output.file).resolve())
    limitations = ["只记录观测差异，不自动确定 SQLGlot/Doris/框架的最终责任。",
        "基表、数据阶段和 Session 由外部准备；本报告不证明数据相同。",
        "差异最多保存三个字段或每侧三种记录反例，不保存全量结果或重复的前五行样本。"]
    if report.validation_mode == "recorded_output":
        limitations.append(".out 通常缺少原生类型，并可能混淆 NULL/空字符串或复杂类型显示；匹配不代表这些维度已验证。")
    if report.filtered:
        limitations.append("本次按 Case ID 筛选运行；导入计数仍属于整个 YAML，未运行查询不计匹配。")
    summary = {
        "total": len(records), "processed_queries": len(report.cases), "successful_matches": matched,
        "known_source_success": source_success, "negative_source_cases": outcomes.get("源端负向用例", 0),
        "needs_attribution": sum(query.get("action") == "归因" for query in records),
        "prerequisite_issues": sum(query.get("action") in {"前提排查", "补查源证据"} for query in records),
        "successful_match_rate": {"numerator": matched, "denominator": source_success,
            "value": matched / source_success if source_success else None,
            "meaning": "成功匹配 / 已取得成功源结果；包含已读到成功 .out 的转译失败，不含源端报错或源结果未知"},
        "outcomes": dict(sorted(outcomes.items())),
        "failure_counts": {key: value for key, value in sorted(outcomes.items()) if key not in {"匹配", "源端负向用例"}},
        "import": report.import_summary.model_dump(mode="json"), "evidence_limits": limitations,
    }
    return {"run": run, "summary": summary, "queries": records}
