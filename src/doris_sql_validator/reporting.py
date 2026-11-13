from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any
from .sql_utils import file_sha256

from .comparison import result_digest
from .models import CaseRunReport, QueryResult, SuiteReport
from .normalization import normalize_value
from .report_labels import ERRORS, OUTCOMES, cell, explain


def write_reports(report: SuiteReport, output_dir: Path, *, case_file_path: Path | None = None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path, markdown_path = output_dir / "validation.json", output_dir / "validation.md"
    payload = _report_payload(report)
    if case_file_path is not None:
        payload["case_file"] = {"path": str(case_file_path.resolve()), "sha256": file_sha256(case_file_path.read_bytes())}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def _case_outcome(case: CaseRunReport) -> str:
    if case.comparison:
        return case.comparison.observed_outcome
    return {"SOURCE_EVIDENCE_FAILED": "SOURCE_EVIDENCE_UNAVAILABLE"}.get(case.status, case.status if case.status != "COMPLETED" else "UNKNOWN")


def _successful_match(case: CaseRunReport) -> bool:
    return bool(_case_outcome(case) == "MATCH" and case.source_evidence and case.source_evidence.result.success and case.target_result and case.target_result.success)


def _negative(case: CaseRunReport) -> bool:
    return bool(case.source_evidence and not case.source_evidence.result.success)


def _needs_detail(case: CaseRunReport) -> bool:
    return not _successful_match(case)


def _result_summary(result: QueryResult) -> dict[str, Any]:
    normalized = [[normalize_value(value) for value in row] for row in result.rows]
    return {
        "engine": result.engine, "success": result.success,
        "columns": [c.model_dump(mode="json") for c in result.columns],
        "row_count": len(result.rows), "row_sample": normalized[:5],
        "result_digest": result_digest(normalized) if result.success else None,
        "error": result.error.model_dump(mode="json") if result.error else None,
        "elapsed_ms": result.elapsed_ms, "query_id": result.query_id,
    }


def _report_statistics(report: SuiteReport) -> dict[str, Any]:
    outcomes = Counter(_case_outcome(c) for c in report.cases)
    success = sum(_successful_match(c) for c in report.cases)
    known_source_success = sum(bool(c.source_evidence and c.source_evidence.result.success) for c in report.cases)
    return {
        "total": len(report.cases), "matched": outcomes.get("MATCH", 0),
        "non_matching": sum(v for k, v in outcomes.items() if k != "MATCH"),
        "successful_matches": success, "negative_source_cases": sum(_negative(c) for c in report.cases),
        "needs_review": sum(_needs_detail(c) for c in report.cases),
        "known_source_success": known_source_success,
        "successful_match_rate_all": success / len(report.cases) if report.cases else None,
        "successful_match_rate_source_success": success / known_source_success if known_source_success else None,
        "translation_failed": outcomes.get("TRANSLATION_FAILED", 0),
        "source_evidence_failed": outcomes.get("SOURCE_EVIDENCE_UNAVAILABLE", 0),
        "doris_execution_failed": sum(bool(c.target_result and not c.target_result.success) for c in report.cases),
        "schema_mismatch": outcomes.get("RESULT_SCHEMA_MISMATCH", 0),
        "row_count_mismatch": outcomes.get("ROW_COUNT_MISMATCH", 0),
        "row_value_mismatch": outcomes.get("ROW_VALUE_MISMATCH", 0),
        "inconclusive": sum(bool(c.comparison and c.comparison.semantic_assessment == "INCONCLUSIVE") for c in report.cases),
        "outcomes": dict(sorted(outcomes.items())),
        "run_statuses": dict(sorted(Counter(c.status for c in report.cases).items())),
    }


def _report_payload(report: SuiteReport) -> dict[str, Any]:
    payload = report.model_dump(mode="python")
    payload.update(started_at=report.started_at.isoformat(), finished_at=report.finished_at.isoformat(), summary=_report_statistics(report))
    payload["target"] = {"dialect": "doris", "engine": "doris", **payload["target"]}
    payload["中文字段说明"] = {
        "summary": "统计。successful_matches 只统计两端成功且匹配；matched 保留旧比较器代码计数，可能包含两端同类报错，不是通过数。",
        "cases": "逐条源 SQL、社区输出、比较结果及有限结果样本。",
        "source_evidence": "参考结果来源；recorded_output 表示读取 .out，没有执行源数据库。",
        "data_assurance": "unverified 表示验证器不负责核验基表；外部数据准备报告须另外提供，不是本轮失败原因判定。",
        "comparison": "自动观察到的差异，不是 SQLGlot 缺陷归因。equivalent 仅是已有证据下旧比较器的判断，不证明完整类型、所有输入或负向错误原因等价。",
        "result_digest": "完整结果归一化后的摘要指纹，不代表类型和顺序均通过。",
        "row_sample": "最多前五行，仅供定位；不是完整结果，也不能用于宣称全量值相同。",
        "internal_codes": "稳定程序字段保留英文；含义见结果代码中文说明。",
    }
    payload["结果代码中文说明"] = OUTCOMES
    for document, case in zip(payload["cases"], report.cases, strict=True):
        document["中文结论"] = _conclusion(case)
        if case.source_evidence:
            document["source_evidence"]["result"] = _result_summary(case.source_evidence.result)
        if case.target_result:
            document["target_result"] = _result_summary(case.target_result)
    return payload


def _conclusion(case: CaseRunReport) -> str:
    if _negative(case) and _case_outcome(case) == "MATCH":
        return "两端同类报错，具体原因尚未确认；不计入成功结果匹配数"
    return explain(_case_outcome(case))


def _source_status(case: CaseRunReport) -> str:
    if case.status == "TRANSLATION_FAILED":
        return "未执行（SQLGlot 解析或生成先失败）"
    if not case.source_evidence:
        return "未取得（可能因转译先失败）"
    return _execution_status(case.source_evidence.result)


def _execution_status(result: QueryResult | None) -> str:
    if result is None:
        return "未取得执行结果"
    return "成功" if result.success else "失败：" + explain(result.error.category if result.error else "UNKNOWN", ERRORS)


def _rate(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator} = {numerator/denominator:.2%}" if denominator else "无可计算分母"


def render_markdown(report: SuiteReport) -> str:
    stats = _report_statistics(report)
    recorded = report.validation_mode == "recorded_output"
    lines = [f"# {report.source.dialect} → Doris 确定性验证报告", "",
        f"- 执行时间：{report.started_at.isoformat()} 至 {report.finished_at.isoformat()}",
        f"- SQLGlot 版本：`{report.sqlglot_version}`；提交：`{report.sqlglot_commit or '未取得'}`。",
        f"- 原始输入：`{report.input.file or '手工 YAML'}`；格式：`{report.input.format}`。",
        f"- 源结果来源：{'读取 .out 历史输出；不连接源数据库，转译成功后才读取对应结果并执行 Doris' if recorded else '转译成功后连接源数据库和 Doris，分别执行查询'}。", "",
        "## 1. 总体结果", "",
        f"- 本轮查询总数：**{stats['total']}**；两端成功且已有证据匹配：**{stats['successful_matches']}**。",
        f"- 成功结果匹配占全部查询比例：**{_rate(stats['successful_matches'], stats['total'])}**。这是结果匹配比例，不是全部语义或类型验证通过率。",
        f"- 已取得成功源结果的查询匹配率：**{_rate(stats['successful_matches'], stats['known_source_success'])}**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。",
        f"- 源端报错的负向用例：**{stats['negative_source_cases']}**；不计入上述成功匹配分子。",
        f"- 需要分析的查询：**{stats['needs_review']}**；包括报错原因待确认的负向用例。",
        f"- SQLGlot 转译失败：**{stats['translation_failed']}**；源参考结果不可用：**{stats['source_evidence_failed']}**；Doris 执行失败：**{stats['doris_execution_failed']}**。", "",
        "本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。", "",
        "### 差异分类统计", "", "| 自动结果及含义 | 查询数 |", "| :--- | ---: |"]
    for outcome, count in stats["outcomes"].items():
        lines.append(f"| {explain(outcome)}（`{outcome}`） | {count} |")
    lines += ["", "这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。", "",
        "## 2. 输入处理与证据限制", "",
        f"导入时保留 {report.import_summary.accepted} 条待验证查询、跳过 {report.import_summary.skipped} 条非查询、{report.import_summary.ambiguous} 条待确认、{report.import_summary.errors} 条解析或输出配对诊断。保留的查询可包含 Parser 尚不支持的语法；解析失败由普通运行记录为转译失败，不会执行数据库查询。诊断数与保留数可能重叠。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。", "",
        "验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。", "",
        "DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。", ""]
    if report.import_diagnostics:
        lines += ["| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |", "| ---: | :--- | :--- | :--- |"]
        for d in report.import_diagnostics:
            label = {"skipped": "跳过非查询", "ambiguous": "需确认", "error": "导入失败"}[d.disposition]
            lines.append(f"| {d.statement_index} | {d.line_start}–{d.line_end} | {label}；类型 `{cell(d.statement_type)}` | {cell(d.reason)} |")
        lines.append("")
    if report.recorded_output:
        lines += [f"参考输出：`{report.recorded_output.file}`；SHA-256（文件内容指纹）：`{report.recorded_output.sha256}`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。", ""]
    evidence = [c.source_evidence for c in report.cases if c.source_evidence]
    lines += ["### 能比较什么", "", "| 比较内容 | 本轮证据情况 |", "| :--- | :--- |"]
    for title, field in [("执行成功或失败", "execution_status"), ("错误类别", "error_category"), ("返回字段数量", "column_count"), ("返回字段名称", "column_names"), ("字段类型", "column_types"), ("返回记录数", "row_count"), ("复杂类型", "complex_types")]:
        count = sum(getattr(e.capabilities, field) for e in evidence)
        lines.append(f"| {title} | {count}/{len(evidence)} 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |")
    lines += ["", ".out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。", "",
        "比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。", "",
        "## 3. 全部查询结果", "", "成功匹配的查询在下表简写；其他查询在下一节展开。", "",
        "| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |", "| :--- | :--- | :--- | :--- | :--- | :--- |"]
    for c in report.cases:
        target_status = "未执行（SQLGlot 解析或生成先失败）" if c.status == "TRANSLATION_FAILED" else _execution_status(c.target_result)
        lines.append(f"| `{c.id}` | {cell(c.source_sql)} | {'失败' if c.status == 'TRANSLATION_FAILED' else '已生成'} | {cell(_source_status(c))} | {cell(target_status)} | {cell(_conclusion(c))} |")
    lines += ["", "## 4. 不匹配、执行失败及负向错误详情", ""]
    detailed = [c for c in report.cases if _needs_detail(c)]
    if not detailed:
        lines += ["没有需要展开的查询。仍需结合上面的证据限制理解匹配范围。", ""]
    for c in detailed:
        lines += [f"### {c.id} — {_conclusion(c)}", "", "#### 源 SQL", "", "```sql", c.source_sql, "```", ""]
        if c.status == "TRANSLATION_FAILED":
            stage = "源 SQL 解析（SQLGlot Parser）" if c.failure_stage == "source_parse" else "SQLGlot 解析或生成"
            lines += [f"失败阶段：**{stage}**。源参考结果获取、Doris 执行和结果比较均未执行，不计为 Doris 执行错误。", ""]
        if c.target_sql:
            lines += ["#### 社区 SQLGlot 生成的 Doris SQL", "", "```sql", c.target_sql, "```", ""]
        for title, error in [("SQLGlot 转译错误原文", c.transpilation_error), ("源参考结果获取错误原文", c.source_evidence_error)]:
            if error:
                lines += [f"#### {title}", "", "```text", error, "```", ""]
        if c.source_evidence:
            _render_result(lines, "源端参考结果", c.source_evidence.result)
        if c.target_result:
            _render_result(lines, "Doris 实际结果", c.target_result)
        lines += ["#### 后续应如何判断", "", *_next_steps(c), ""]
        if c.comparison:
            lines += ["自动比较器诊断原文（可能含英文程序字段，不是最终根因）：", "", "```text", c.comparison.summary,
                *[d for d in c.comparison.details if not d.startswith(("source_digest=", "doris_digest=", "source_sample=", "doris_sample="))], "```", ""]
    return "\n".join(lines)


def _render_result(lines: list[str], title: str, result: QueryResult) -> None:
    lines += [f"#### {title}", "", f"- 执行状态：{_execution_status(result)}；耗时 {result.elapsed_ms:.1f} ms。"]
    if result.error:
        lines += [f"- 错误类别：{explain(result.error.category, ERRORS)}（`{result.error.category}`）；错误码：`{result.error.code or '未取得'}`。", "", "错误原文：", "", "```text", result.error.message, "```", ""]
    else:
        lines += [f"- 返回行数：{len(result.rows)}；字段：{cell(', '.join(c.name + ': ' + c.canonical_type + ' / ' + (c.database_type or '原生类型未知') for c in result.columns))}。",
            "- 结果样本（最多前五行，完整结果并未保存在此样本中）：", "", "```json",
            json.dumps(_result_summary(result)["row_sample"], ensure_ascii=False, indent=2), "```", ""]


def _next_steps(case: CaseRunReport) -> list[str]:
    if _negative(case):
        return ["- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。"]
    outcome = _case_outcome(case)
    if outcome == "TRANSLATION_FAILED":
        return ["- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。"]
    if "ENVIRONMENT" in outcome or outcome == "SOURCE_EVIDENCE_UNAVAILABLE":
        return ["- 先核对连接、数据库/表/权限、输入输出配对及外部数据准备记录；当前证据不足以判定 SQLGlot 缺陷。"]
    return ["- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。",
        "- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。",
        "- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。"]
