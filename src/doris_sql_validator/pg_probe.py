"""Explicit PostgreSQL/Doris diagnostic execution; never generates AI SQL."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
import json
import math
from pathlib import Path
import re

import sqlglot
from sqlglot import exp
from pydantic import BaseModel, ConfigDict, Field, StrictStr

from .case_loader import load_case_file
from .models import LoadedCaseFile
from .execution.common import classify_error
from .execution.doris import DorisAdapter, _doris_type_name
from .execution.postgres import PostgresAdapter
from .source_provider import RecordedOutputProvider
from .sql_utils import file_sha256, parse_read_only_query
from .report_labels import ERRORS, explain
from .reporting import load_validation_report, validate_report_inputs


def pack(value):
    if isinstance(value, Decimal):
        return {"十进制数": str(value)}
    if isinstance(value, bytes):
        return {"二进制十六进制": value.hex()}
    if isinstance(value, (date, datetime, time)):
        return value.isoformat()
    if isinstance(value, timedelta):
        return {"时间间隔秒": str(Decimal(value.days * 86400 + value.seconds) + Decimal(value.microseconds) / 1000000)}
    if isinstance(value, float) and not math.isfinite(value):
        return {"特殊浮点数": str(value)}
    if isinstance(value, (list, tuple)):
        return [pack(v) for v in value]
    if isinstance(value, dict):
        return {str(k): pack(v) for k, v in value.items()}
    return value


def family(column):
    t = (column.get("原生类型") or "").lower().replace(" ", "")
    if t.startswith(("_", "array")): return "数组"
    if "json" in t: return "JSON"
    if t in {"bool", "boolean"}: return "布尔"
    if t in {"int2", "int4", "int8", "tinyint", "smallint", "int", "integer", "bigint", "largeint"}: return "整数"
    if "numeric" in t or "decimal" in t: return "十进制数"
    if t in {"float4", "float8", "float", "double", "real", "doubleprecision"}: return "浮点数"
    if t in {"bytea", "binary", "varbinary"}: return "二进制"
    if "timestamp" in t or "datetime" in t: return "时间戳"
    if t in {"date", "datev2"}: return "日期"
    if t.startswith(("time", "timetz")): return "时间"
    if t == "interval": return "时间间隔"
    if any(s in t for s in ("char", "text", "string", "name")): return "字符串"
    return "未知"


def declared_type(column):
    t = (column.get("原生类型") or "").lower().replace(" ", "")
    aliases = {"int2": "int16", "smallint": "int16", "int4": "int32", "integer": "int32", "int": "int32", "int8": "int64", "bigint": "int64", "tinyint": "int8", "float4": "float32", "real": "float32", "float": "float32", "float8": "float64", "double": "float64", "bool": "boolean", "jsonb": "json", "bytea": "binary", "varbinary": "binary", "text": "unbounded-string", "varchar": "unbounded-string"}
    return aliases.get(t, re.sub(r"^decimalv[23]", "decimal", t)) or None


def number_key(value):
    """Remove insignificant zeroes without Decimal context rounding."""
    number = Decimal(str(value))
    if not number.is_finite(): return str(number)
    if number == 0: return "0"
    sign, digits, exponent = number.as_tuple()
    digits = list(digits)
    while digits and digits[-1] == 0:
        digits.pop()
        exponent += 1
    return ("-" if sign else "") + "".join(map(str, digits)) + "e" + str(exponent)


def canonical(value, column, *, structured=False):
    if value is None: return ["SQL NULL"]
    if isinstance(value, dict):
        if "十进制数" in value: value = Decimal(value["十进制数"])
        elif "二进制十六进制" in value: return ["字节", value["二进制十六进制"]]
        elif "特殊浮点数" in value: return ["特殊浮点数", value["特殊浮点数"]]
    kind = family(column)
    if structured and kind in {"JSON", "数组"}:
        if isinstance(value, str): value = json.loads(value, parse_float=Decimal)
        def nested(v):
            if kind == "数组" and isinstance(v, dict) and set(v) == {"十进制数"}:
                return ["数值", number_key(v["十进制数"])]
            if isinstance(v, dict): return {k: nested(x) for k, x in sorted(v.items())}
            if isinstance(v, list): return [nested(x) for x in v]
            if isinstance(v, (int, float, Decimal)) and not isinstance(v, bool): return ["数值", number_key(v)]
            return v
        return [kind, nested(value)]
    if isinstance(value, bool) or (kind == "布尔" and value in (0, 1)):
        return ["布尔", bool(value)]
    if isinstance(value, (int, float, Decimal)): return ["数值", number_key(value)]
    if isinstance(value, str) and kind in {"日期", "时间戳", "时间"}:
        try:
            if kind == "时间戳":
                dt = datetime.fromisoformat(value)
                if dt.tzinfo: dt = dt.astimezone(timezone.utc)
                value = dt.isoformat(timespec="microseconds")
            elif kind == "时间": value = time.fromisoformat(value).isoformat(timespec="microseconds")
        except ValueError:
            pass
    return ["值", value]


def _comparison_keys(result, other):
    values = []
    for row in result["记录"]:
        normalized = []
        for i, v in enumerate(row):
            col = result["字段"][i] if i < len(result["字段"]) else {}
            peer = other["字段"][i] if i < len(other["字段"]) else {}
            structured = family(col) == family(peer) and family(col) in {"JSON", "数组"}
            normalized.append(canonical(v, col, structured=structured))
        values.append(json.dumps(normalized, ensure_ascii=False, sort_keys=True, default=str))
    return values


def compare_probe(source, target, source_sql):
    """Report independent dimensions; unknown metadata is not a passing type check."""
    checks = {"执行状态": "一致" if source["成功"] == target["成功"] else "不同"}
    if not source["成功"] or not target["成功"]:
        checks["错误原因"] = "两端均失败，但是否同因仍需阅读错误原文" if not source["成功"] and not target["成功"] else "一端成功一端失败"
        checks["结果字段和记录"] = "至少一端没有完整成功结果，未比较"
        return checks
    tree = parse_read_only_query(source_sql, "postgres")
    checks["字段数量"] = "一致" if len(source["字段"]) == len(target["字段"]) else "不同"
    checks["显式别名"] = "未发现需检查的显式别名" if isinstance(tree, exp.Select) else "集合查询别名尚未检查"
    if isinstance(tree, exp.Select):
        aliases = [(i, e.alias) for i, e in enumerate(tree.expressions) if isinstance(e, exp.Alias)]
        if aliases:
            checks["显式别名"] = "一致" if all(i < len(target["字段"]) and target["字段"][i]["名称"].lower() == name.lower() for i, name in aliases) else "不同"
    checks["字段类型"] = []
    for index, (s, t) in enumerate(zip(source["字段"], target["字段"])):
        sf, tf = family(s), family(t)
        sd, td = declared_type(s), declared_type(t)
        sp, ss = s.get("精度"), s.get("小数位数")
        tp, ts = t.get("精度"), t.get("小数位数")
        m = re.search(r"decimal\w*\((\d+),\s*(\d+)\)", t.get("原生类型") or "", re.I)
        if m: tp, ts = map(int, m.groups())
        precision = "不适用"
        if sf in {"十进制数", "时间戳", "时间"} or tf in {"十进制数", "时间戳", "时间"}:
            precision = "信息不足" if None in (sp, ss, tp, ts) else ("一致" if (sp, ss) == (tp, ts) else "不同")
        checks["字段类型"].append({"字段位置": index + 1, "源原生类型": s.get("原生类型"), "Doris原生类型": t.get("原生类型"),
            "逻辑类型": "信息不足" if "未知" in (sf, tf) else ("一致" if sf == tf else "不同"),
            "类型声明": "信息不足" if not sd or not td else ("一致" if sd == td else "不同"),
            "精度与小数位": precision})
    checks["记录行数"] = "一致" if len(source["记录"]) == len(target["记录"]) else "不同"
    checks["双端行数"] = {"PostgreSQL": len(source["记录"]), "Doris": len(target["记录"])}
    try:
        sk, tk = _comparison_keys(source, target), _comparison_keys(target, source)
        checks["记录值及重复次数"] = "一致" if Counter(sk) == Counter(tk) else "不同"
        if Counter(sk) != Counter(tk):
            source_extra, target_extra = Counter(sk) - Counter(tk), Counter(tk) - Counter(sk)
            def examples(keys, rows, counts):
                values = dict(zip(keys, rows))
                return [{"记录": values[key], "多出次数": count} for key, count in list(counts.items())[:3]]
            checks["行值反例"] = {
                "PostgreSQL多出": examples(sk, source["记录"], source_extra),
                "Doris多出": examples(tk, target["记录"], target_extra),
                "未展示的不同记录种类": max(0, len(source_extra) - 3) + max(0, len(target_extra) - 3),
            }
        if tree.args.get("order") and sk != tk:
            differences = [i for i in range(min(len(sk), len(tk))) if sk[i] != tk[i]]
            checks["顺序反例"] = [{"行号": i + 1, "PostgreSQL": source["记录"][i], "Doris": target["记录"][i]} for i in differences[:3]]
            checks["未展示的不同位置数"] = max(0, len(differences) - 3)

        checks["最终行顺序"] = ("本次顺序一致，排序键唯一性未证明" if sk == tk else "不同，需检查并列排序") if tree.args.get("order") else "无最终 ORDER BY，忽略结果行顺序但保留重复次数"
    except (ValueError, TypeError) as exc:
        checks["记录值及重复次数"] = "无法可靠归一化，需人工核对：" + str(exc)
    checks["浮点容差"] = "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略"
    checks["证据范围"] = "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"
    return checks


def execute_query(engine, sql, database, *, timeout=10, row_limit=10000):
    # Check before connection: no multi-statement, DDL/DML, SELECT INTO or locks.
    _validate_probe_query(sql, "postgres" if engine == "postgres" else "doris")
    result = {"引擎": engine, "SQL": sql, "成功": False, "字段": [], "记录": [], "错误": None}
    connection = None
    try:
        adapter = PostgresAdapter() if engine == "postgres" else DorisAdapter()
        connection = adapter.connect(database=database)
        with connection.cursor() as cursor:
            if engine == "postgres":
                from psycopg.types.json import set_json_loads
                from psycopg.types.string import TextLoader
                set_json_loads(lambda v: v.decode() if isinstance(v, bytes) else v, connection)
                for oid in (1082, 1083, 1114, 1184, 1186, 1266):
                    connection.adapters.register_loader(oid, TextLoader)
                cursor.execute("SET default_transaction_read_only = on")
                cursor.execute(f"SET statement_timeout = '{int(timeout)}s'")
                cursor.execute("SET timezone = 'UTC'")
                cursor.execute("SET datestyle = 'ISO, MDY'")
                cursor.execute("SELECT oid, typname FROM pg_type")
                names = dict(cursor.fetchall())
                cursor.execute("SELECT current_database(), version(), current_setting('TimeZone'), current_setting('DateStyle'), current_setting('extra_float_digits')")
                result["版本与会话"] = dict(zip(["实际数据库", "数据库版本", "时区", "日期格式", "浮点显示额外位数"], cursor.fetchone()))
            else:
                cursor.execute("SET time_zone = '+00:00'")
                cursor.execute(f"SET query_timeout = {int(timeout)}")
                cursor.execute("SELECT DATABASE(), VERSION()")
                result["数据库与版本函数返回值"] = dict(zip(["实际数据库", "版本函数返回值"], cursor.fetchone()))
                cursor.execute("SHOW VARIABLES LIKE 'enable_strict_cast'")
                result["类型转换会话设置"] = pack(cursor.fetchall())
            cursor.execute(sql)
            if not cursor.description:
                raise ValueError("查询没有返回结果集")
            if engine == "postgres":
                result["字段"] = [{"名称": d.name, "PostgreSQL类型编号": d.type_code, "原生类型": names.get(d.type_code), "精度": d.precision, "小数位数": d.scale} for d in cursor.description]
            else:
                result["字段"] = [{"名称": d[0], "协议类型": _doris_type_name(d[1], f), "原生类型": None, "精度": d[4], "小数位数": d[5]} for d, f in zip(cursor.description, cursor._result.fields)]
            rows = cursor.fetchmany(row_limit + 1)
            if len(rows) > row_limit:
                result["错误"] = {"类别": "证据采集上限", "原文": f"返回超过 {row_limit} 行；未保存截断结果冒充完整结果"}
                return result
            result.update(成功=True, 记录=pack(rows))
            if engine == "doris":
                try:
                    cursor.execute("EXPLAIN VERBOSE " + sql.rstrip().rstrip(";"))
                    lines = [str(row[0]) for row in cursor.fetchall()]
                    descriptors = {int(m[1]): m[2] for line in lines if (m := re.search(r"SlotDescriptor\{id=(\d+),.*? type=(.*?), nullable=", line))}
                    ids, in_output = [], False
                    for line in lines:
                        if "OUTPUT EXPRS:" in line:
                            in_output = True
                            continue
                        if in_output and "PARTITION:" in line: break
                        if in_output and (m := re.search(r"\[#(\d+)\]", line)): ids.append(int(m[1]))
                    if len(ids) == len(result["字段"]):
                        for col, oid in zip(result["字段"], ids): col["原生类型"] = descriptors.get(oid)
                    result["类型证据说明"] = "原生类型来自 EXPLAIN VERBOSE；未解析到的位置保留未知，不用协议 STRING 猜 JSON/数组类型"
                except Exception as exc:
                    result["类型证据说明"] = "未取得完整执行计划类型：" + str(exc)
    except Exception as exc:
        code = classify_error(exc).category
        result["错误"] = {"类别": explain(code, ERRORS), "程序错误代码": code, "异常类": type(exc).__name__, "PostgreSQL标准错误状态码": getattr(exc, "sqlstate", None), "原文": str(exc)}
    finally:
        if connection is not None: connection.close()
    return result


def _validate_probe_query(sql: str, dialect: str) -> None:
    tree = parse_read_only_query(sql, dialect)
    if tree.find(exp.Into) or tree.find(exp.Lock):
        raise ValueError("诊断不允许 SELECT INTO 或加锁查询")


@dataclass
class _ProbeContext:
    loaded: LoadedCaseFile
    report_path: Path
    report: dict
    cases: dict
    baselines: dict
    report_sha256: str
    tool_sha256: str
    provider: RecordedOutputProvider | None = None


class ProbeRequest(BaseModel):
    """One independent attempt; repeated case IDs are deliberately allowed."""
    model_config = ConfigDict(extra="forbid")

    case_id: StrictStr = Field(min_length=1)
    candidate_sql: StrictStr = Field(min_length=1)
    source_variant_sql: StrictStr | None = Field(default=None, min_length=1)


def _load_probe_context(case_path: Path, report_path: Path) -> _ProbeContext:
    loaded = load_case_file(case_path)
    definition = loaded.definition
    if definition.source.engine not in {"postgres", "postgresql"}:
        raise ValueError("该诊断命令仅支持 PostgreSQL → Doris")
    report = load_validation_report(report_path)
    validate_report_inputs(report, loaded)
    return _ProbeContext(
        loaded=loaded, report_path=report_path.resolve(), report=report,
        cases={c.id: c for c in definition.cases},
        baselines={c["id"]: c for c in report["queries"]},
        report_sha256=file_sha256(report_path.read_bytes()),
        tool_sha256=file_sha256(Path(__file__).read_bytes()),
    )


def _prepare_probe(context: _ProbeContext, request: ProbeRequest) -> dict:
    """Validate all three queries and source evidence before any connection."""
    loaded, cases = context.loaded, context.cases
    definition, run = loaded.definition, context.report["run"]
    case_id, candidate_sql = request.case_id, request.candidate_sql
    if case_id not in cases:
        raise ValueError("YAML 中不存在该查询编号")
    baseline = context.baselines.get(case_id)
    if baseline is None or baseline["source_sql"].strip() != cases[case_id].sql.strip():
        raise ValueError("首轮报告与查询原文不对应")
    is_variant = request.source_variant_sql is not None
    source_sql = request.source_variant_sql if is_variant else cases[case_id].sql
    community = baseline.get("target_sql") if not is_variant else None
    # Validate every SQL before even the first diagnostic connection.
    _validate_probe_query(source_sql, "postgres")
    _validate_probe_query(candidate_sql, "doris")
    if community:
        _validate_probe_query(community, "doris")

    record = {
        "查询编号": case_id, "执行时间": datetime.now(timezone.utc).isoformat(),
        "源SQL": source_sql, "首次源SQL": cases[case_id].sql, "是否边界变体": is_variant,
        "首轮报告": str(context.report_path), "Case YAML": str(loaded.path),
        "首轮报告SHA256": context.report_sha256,
        "首轮SQLGlot版本": run.get("sqlglot_version"), "首轮SQLGlot提交": run.get("sqlglot_commit"),
        "本次工具SQLGlot版本": sqlglot.__version__,
        "对照工具代码SHA256": context.tool_sha256,
        "社区DorisSQL": community, "独立DorisSQL": candidate_sql,
        "候选与社区输出相同": bool(community and community.strip().rstrip(";") == candidate_sql.strip().rstrip(";")),
        "说明": "只读执行事实，不生成文件、不调用模型、不判定根因；由调用者将实际结果和分析写入本 Case Markdown",
    }
    if definition.recorded_output and not is_variant:
        if context.provider is None:
            context.provider = RecordedOutputProvider(definition.recorded_output, base_dir=loaded.base_dir, dialect=definition.source.dialect)
        reference = context.provider.get_result(cases[case_id])
        record["历史输出参考"] = reference.model_dump(mode="json")
        record["历史输出限制"] = "仅原 .out 显示文本；未自动证明其与当前 PG 的类型、状态和结果一致，需在 Case Markdown 核对数据阶段与 Session"
    if not community:
        record["社区输出未重放原因"] = "显式边界变体没有对应首轮生成 SQL" if is_variant else baseline.get("transpilation_error", "首轮未保存目标 SQL，不猜测重建历史输出")
    return record


def _execute_probe(context: _ProbeContext, record: dict) -> dict:
    definition = context.loaded.definition
    source_sql, candidate_sql = record["源SQL"], record["独立DorisSQL"]
    community = record["社区DorisSQL"]
    source = execute_query("postgres", source_sql, definition.source.database)
    record["PostgreSQL实际结果"] = source
    if community:
        actual = execute_query("doris", community, definition.target.database)
        record["社区Doris实际结果"] = actual
        record["社区输出比较"] = compare_probe(source, actual, source_sql)
    candidate = execute_query("doris", candidate_sql, definition.target.database)
    record["独立Doris实际结果"] = candidate
    record["独立候选比较"] = compare_probe(source, candidate, source_sql)
    source_repeat = execute_query("postgres", source_sql, definition.source.database)
    target_repeat = execute_query("doris", candidate_sql, definition.target.database)
    record["源端重复执行结果"] = source_repeat
    record["目标重复执行结果"] = target_repeat
    record["源端重复稳定性"] = compare_probe(source, source_repeat, source_sql)
    record["重复执行独立候选比较"] = compare_probe(source_repeat, target_repeat, source_sql)
    record["未自动验证范围"] = "全部参数边界、完整类型域、数组下界、排序键唯一性、基表一致性，以及原 .out 与当前 PG 的完整对应关系"
    return record


def probe_postgres_case(
    case_path: Path,
    report_path: Path,
    case_id: str,
    candidate_sql: str,
    *,
    source_variant_sql: str | None = None,
) -> dict:
    """Execute explicit SQL and return facts in memory; never create files."""
    context = _load_probe_context(case_path, report_path)
    request = ProbeRequest(case_id=case_id, candidate_sql=candidate_sql, source_variant_sql=source_variant_sql)
    return _execute_probe(context, _prepare_probe(context, request))


def probe_postgres_cases(case_path: Path, report_path: Path, requests: list) -> dict:
    """One stage per batch; no DB result cache, pooling, file writes or AI calls."""
    if not isinstance(requests, list) or not requests:
        raise ValueError("批量候选必须是非空 JSON 数组")
    context = _load_probe_context(case_path, report_path)
    attempts = []
    for index, item in enumerate(requests, 1):
        attempt = {"请求序号": index, "请求": item}
        attempts.append(attempt)
        try:
            request = ProbeRequest.model_validate(item)
            record = _prepare_probe(context, request)
        except Exception as exc:
            attempt.update(处理状态="未执行", 错误={"阶段": "输入、只读检查或源证据读取", "异常类": type(exc).__name__, "原文": str(exc)})
            continue
        try:
            attempt["事实"] = summarize_probe(_execute_probe(context, record))
            attempt["处理状态"] = "已完成"
        except Exception as exc:
            # A comparison/tool error must not hide the rest of the batch or
            # erase execution facts already collected for this attempt.
            attempt.update(处理状态="工具处理失败", 事实=summarize_probe(record),
                           错误={"阶段": "执行或比较；可能已执行部分查询", "异常类": type(exc).__name__, "原文": str(exc)})
    return {
        "共同输入": {"Case YAML": str(context.loaded.path), "首轮报告": str(context.report_path),
                     "PostgreSQL数据库": context.loaded.definition.source.database,
                     "Doris数据库": context.loaded.definition.target.database,
                     "首轮SQLGlot版本": context.report["run"].get("sqlglot_version"),
                     "首轮SQLGlot提交": context.report["run"].get("sqlglot_commit"),
                     "首轮报告SHA256": context.report_sha256,
                     "对照工具代码SHA256": context.tool_sha256,
                     "本次工具SQLGlot版本": sqlglot.__version__},
        "批次统计": summarize_probe_batch(attempts),
        "逐条请求": attempts,
        "限制": "仅复用输入读取，不缓存数据库结果、不合并查询、不跨阶段复用会话；统计不是根因或等价性结论。每条仍单独连接、限时、采集有限完整结果并重复执行。",
    }


def summarize_probe_batch(attempts: list[dict]) -> dict:
    completed = [a["事实"] for a in attempts if a["处理状态"] == "已完成"]
    checks = [r["独立候选比较"] for r in completed]
    return {
        "请求总数": len(attempts),
        "请求中不同Case编号数": len({a["请求"]["case_id"] for a in attempts if isinstance(a["请求"], dict) and isinstance(a["请求"].get("case_id"), str)}),
        "完成对照请求数": len(completed),
        "未执行请求数": sum(a["处理状态"] == "未执行" for a in attempts),
        "工具处理失败请求数": sum(a["处理状态"] == "工具处理失败" for a in attempts),
        "边界变体请求数": sum(r["是否边界变体"] for r in completed),
        "候选与社区相同的控制重跑数": sum(r["候选与社区输出相同"] for r in completed),
        "完成请求的候选观察（可重叠）": {
            "源端执行失败": sum(not r["PostgreSQL实际结果"]["成功"] for r in completed),
            "候选执行失败": sum(not r["独立Doris实际结果"]["成功"] for r in completed),
            "行值及重复次数一致": sum(c.get("记录值及重复次数") == "一致" for c in checks),
            "行值及重复次数不同": sum(c.get("记录值及重复次数") == "不同" for c in checks),
            "行值未比较或无法归一化": sum(c.get("记录值及重复次数") not in {"一致", "不同"} for c in checks),
            "类型不同、信息不足或未比较": sum(c.get("字段数量") != "一致" or any(
                t[key] not in {"一致", "不适用"} for t in c.get("字段类型", [])
                for key in ("逻辑类型", "类型声明", "精度与小数位")
            ) for c in checks),
            "最终顺序观察不同": sum(c.get("最终行顺序", "").startswith("不同") for c in checks),
        },
        "统计口径": "请求含原句候选、重试与边界；不同编号数按输入字符串去重，包含无效编号，不表示有效调查覆盖。完成对照、未执行、工具处理失败三项互斥且合计请求总数；观察只统计完成请求，可以重叠。完成仅指工具处理完成，不表示执行成功、全部维度一致或已确认根因；边界不是新增原查询。",
    }


def summarize_probe(record: dict, *, sample_limit: int = 3) -> dict:
    """Bound CLI output only after full in-memory comparison has completed."""
    def execution_summary(result):
        summary = {key: value for key, value in result.items() if key != "记录"}
        rows = result["记录"]
        summary["行数"] = len(rows) if result["成功"] else None
        summary["记录样本"] = rows[:sample_limit]
        summary["未展示行数"] = max(0, len(rows) - sample_limit)
        return summary

    compact = {}
    for key, value in record.items():
        if isinstance(value, dict) and "成功" in value and "记录" in value:
            compact[key] = execution_summary(value)
        elif key == "历史输出参考":
            compact[key] = {name: item for name, item in value.items() if name != "result"}
            result = value["result"]
            compact[key]["结果摘要"] = {
                "成功": result["success"], "字段": result["columns"], "错误": result["error"],
                "行数": len(result["rows"]) if result["success"] else None,
                "记录样本": result["rows"][:sample_limit],
                "未展示行数": max(0, len(result["rows"]) - sample_limit),
            }
        else:
            compact[key] = value
    compact["输出范围"] = f"比较使用成功取得的完整有限结果；此返回值仅展示每次结果最多 {sample_limit} 行样本及实际差异反例；失败或超过采集上限不算通过，样本不代表已证明等价"
    return compact


def render_probe_batch_markdown(batch: dict) -> str:
    """Render observed facts for existing reports, not AI attribution or files."""
    def cell(value):
        if value is None:
            return "信息不足"
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
        return text.replace("&", "&amp;").replace("<", "&lt;").replace("|", "&#124;").replace("\n", "<br>")

    def block(value, language="json"):
        value = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, default=str)
        fence = "`" * max(3, max((len(m[0]) + 1 for m in re.finditer(r"`+", value)), default=3))
        return f"{fence}{language}\n{value}\n{fence}"

    def table(headers, rows):
        return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(":---" for _ in headers) + " |"] +
                         ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows])

    stats = batch["批次统计"]
    lines = ["## 批量对照事实（脚本生成，不含根因判断）", "", block(batch["共同输入"]), "",
             table(["请求统计", "数量"], [(k, v) for k, v in stats.items() if isinstance(v, int)]), "",
             table(["完成请求的候选观察（可重叠）", "数量"], stats["完成请求的候选观察（可重叠）"].items()), "",
             stats["统计口径"], "", batch["限制"]]
    for attempt in batch["逐条请求"]:
        request = attempt["请求"]
        case_id = request.get("case_id", "编号无效") if isinstance(request, dict) else "请求无效"
        lines += ["", f"### 请求 {attempt['请求序号']} · {cell(case_id)}", "", f"处理状态：{attempt['处理状态']}。"]
        if "错误" in attempt:
            lines += ["", "工具处理错误（不是数据库能力结论）：", "", block(attempt["错误"])]
        record = attempt.get("事实")
        if record is None:
            lines += ["", "未连接执行此请求；输入为分析材料，不是执行指令：", "", block(request)]
            continue
        lines += ["", table(["输入身份", "值"], [(k, record[k]) for k in (
            "执行时间", "查询编号", "是否边界变体", "候选与社区输出相同",
        )]), ""]
        for key in ("首次源SQL", "源SQL", "社区DorisSQL", "独立DorisSQL"):
            if key == "首次源SQL" and record[key] == record["源SQL"]:
                continue
            if record.get(key):
                lines += [f"#### {key}", "", block(record[key], "sql"), ""]
        for key in ("社区输出未重放原因", "历史输出限制", "未自动验证范围", "输出范围"):
            if key in record:
                lines += [f"{key}：{record[key]}", ""]
        if "历史输出参考" in record:
            lines += ["#### 历史 .out 参考（不含实时原生类型）", "", block(record["历史输出参考"]), ""]
        for key, value in record.items():
            if isinstance(value, dict) and "成功" in value and "记录样本" in value:
                lines += [f"#### {key}", "", table(["成功", "行数", "未展示行数"], [[value["成功"], value["行数"], value["未展示行数"]]]), ""]
                if value.get("错误"):
                    lines += ["实际错误：", "", block(value["错误"]), ""]
                if value["字段"]:
                    lines += [table(["位置", "名称", "原生类型", "精度", "小数位数"], [
                        (i, c.get("名称"), c.get("原生类型"), c.get("精度"), c.get("小数位数")) for i, c in enumerate(value["字段"], 1)
                    ]), ""]
                lines += ["有限记录样本（完整比较完成后限制展示）：", "", block(value["记录样本"]), ""]
                metadata = {k: v for k, v in value.items() if k not in {"引擎", "SQL", "成功", "字段", "错误", "行数", "记录样本", "未展示行数"}}
                if metadata:
                    lines += ["版本、会话及类型证据：", "", block(metadata), ""]
            elif isinstance(value, dict) and "执行状态" in value:
                lines += [f"#### {key}", "", table(["比较维度", "观察"], [(k, v) for k, v in value.items() if k not in {"字段类型", "行值反例", "顺序反例"}]), ""]
                if value.get("字段类型"):
                    lines += [table(["位置", "源类型", "Doris 类型", "逻辑类型", "类型声明", "精度与小数位"], [
                        (c["字段位置"], c["源原生类型"], c["Doris原生类型"], c["逻辑类型"], c["类型声明"], c["精度与小数位"]) for c in value["字段类型"]
                    ]), ""]
                for example in ("行值反例", "顺序反例"):
                    if example in value:
                        lines += [example + "：", "", block(value[example]), ""]
    return "\n".join(lines).rstrip() + "\n"
