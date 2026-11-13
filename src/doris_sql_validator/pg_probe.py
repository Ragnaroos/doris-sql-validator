"""Explicit PostgreSQL/Doris diagnostic execution; never generates AI SQL."""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
import json
import math
from pathlib import Path
import re

import sqlglot
from sqlglot import exp

from .case_loader import load_case_file
from .execution.common import classify_error
from .execution.doris import DorisAdapter, _doris_type_name
from .execution.postgres import PostgresAdapter
from .source_provider import RecordedOutputProvider
from .sql_utils import file_sha256, parse_read_only_query
from .report_labels import ERRORS, explain


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
    def keys(result, other):
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
    try:
        sk, tk = keys(source, target), keys(target, source)
        checks["记录值及重复次数"] = "一致" if Counter(sk) == Counter(tk) else "不同"
        checks["最终行顺序"] = ("本次顺序一致，排序键唯一性未证明" if sk == tk else "不同，需检查并列排序") if tree.args.get("order") else "无最终 ORDER BY，忽略结果行顺序但保留重复次数"
    except (ValueError, TypeError) as exc:
        checks["记录值及重复次数"] = "无法可靠归一化，需人工核对：" + str(exc)
    checks["浮点容差"] = "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略"
    checks["证据范围"] = "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"
    return checks


def execute_query(engine, sql, database, *, timeout=10, row_limit=10000):
    # Check before connection: no multi-statement, DDL/DML, SELECT INTO or locks.
    tree = parse_read_only_query(sql, "postgres" if engine == "postgres" else "doris")
    if tree.find(exp.Into) or tree.find(exp.Lock):
        raise ValueError("诊断不允许 SELECT INTO 或加锁查询")
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


def probe_postgres_case(case_path: Path, report_path: Path, case_id: str, candidate_path: Path, output_dir: Path, *, source_variant: Path | None = None):
    loaded = load_case_file(case_path)
    definition = loaded.definition
    if definition.source.engine not in {"postgres", "postgresql"}:
        raise ValueError("该诊断命令仅支持 PostgreSQL → Doris")
    cases = {c.id: c for c in definition.cases}
    if case_id not in cases: raise ValueError("YAML 中不存在该查询编号")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    baseline = next((c for c in report.get("cases", []) if c["id"] == case_id), None)
    if baseline is None or baseline["source_sql"].strip() != cases[case_id].sql.strip():
        raise ValueError("首轮报告与查询原文不对应")
    if report.get("source", {}).get("database") != definition.source.database or report.get("target", {}).get("database") != definition.target.database:
        raise ValueError("报告与 YAML 的数据库不对应；不得把改库后的查询当成同一执行环境")
    if report.get("source", {}).get("engine") not in {"postgres", "postgresql"}:
        raise ValueError("首轮报告不是 PostgreSQL 源端")
    source_sql = source_variant.read_text(encoding="utf-8") if source_variant else cases[case_id].sql
    candidate_sql = candidate_path.read_text(encoding="utf-8")
    parse_read_only_query(source_sql, "postgres")
    parse_read_only_query(candidate_sql, "doris")
    community = baseline.get("target_sql") if not source_variant else None
    if community: parse_read_only_query(community, "doris")
    destination = output_dir.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("对照输出目录非空，请使用新的目录，避免覆盖证据")
    destination.mkdir(parents=True, exist_ok=True)
    record = {"查询编号": case_id, "执行时间": datetime.now(timezone.utc).isoformat(), "源SQL": source_sql,
        "首次源SQL": cases[case_id].sql, "是否边界变体": source_variant is not None,
        "首轮报告SHA256": file_sha256(report_path.read_bytes()), "首轮SQLGlot版本": report.get("sqlglot_version"),
        "首轮SQLGlot提交": report.get("sqlglot_commit"), "本次工具SQLGlot版本": sqlglot.__version__,
        "对照工具代码SHA256": file_sha256(Path(__file__).read_bytes()),
        "独立DorisSQL": candidate_sql,
        "候选与社区输出相同": bool(community and community.strip().rstrip(";") == candidate_sql.strip().rstrip(";")),
        "说明": "只读对照工具，不生成 AI 改写、不修改数据库数据、不判定最终根因；边界变体需由调用者明确提供，未执行不算通过"}
    if definition.recorded_output and not source_variant:
        reference = RecordedOutputProvider(definition.recorded_output, base_dir=loaded.base_dir, dialect=definition.source.dialect).get_result(cases[case_id])
        record["历史输出参考"] = reference.model_dump(mode="json")
        record["历史输出限制"] = "仅保留原 .out 的显示文本证据；未自动证明它与本次实时 PG 的类型、错误细节和格式完全一致，需结合会话和数据阶段核对"
    source = execute_query("postgres", source_sql, definition.source.database)
    record["PostgreSQL实际结果"] = source
    if community:
        actual = execute_query("doris", community, definition.target.database)
        record["社区Doris实际结果"] = actual
        record["社区输出比较"] = compare_probe(source, actual, source_sql)
    else:
        record["社区输出未重放原因"] = "这是显式边界变体，没有对应首轮生成 SQL" if source_variant else baseline.get("transpilation_error", "首轮无 Doris SQL")
    candidate = execute_query("doris", candidate_sql, definition.target.database)
    record["独立Doris实际结果"] = candidate
    record["独立候选比较"] = compare_probe(source, candidate, source_sql)
    source_repeat = execute_query("postgres", source_sql, definition.source.database)
    target_repeat = execute_query("doris", candidate_sql, definition.target.database)
    record["源端重复执行结果"] = source_repeat
    record["目标重复执行结果"] = target_repeat
    record["源端重复稳定性"] = compare_probe(source, source_repeat, source_sql)
    record["重复执行独立候选比较"] = compare_probe(source_repeat, target_repeat, source_sql)
    (destination / "probe-evidence.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {case_id}：只读独立对照记录", "", "本记录是实际执行证据，不是最终归因；没有自动生成或修复 SQL。", "",
        f"- {'本次是调用者提供的边界变体，不是原输入。' if source_variant else '本次重放原始查询。'}",
        f"- {'候选 SQL 与社区输出相同，只算原句重跑，不能算新改写。' if record['候选与社区输出相同'] else '候选与社区输出不同或社区没有输出；文本不同不证明同义。'}",
        "- 完整结果和重复执行记录保存在同目录 JSON；这里只展开比较维度和错误。", "",
        "## 1. SQL", "", "源 PostgreSQL：", "", "```sql", source_sql, "```", "", "社区 Doris：", "", "```sql", community or "-- 首轮没有可重放的社区输出", "```", "", "独立 Doris：", "", "```sql", candidate_sql, "```", "",
        "## 2. 分维度比较", "", "类型不同不会阻断行值比较；未知类型不算匹配；重复次数与最终顺序分开记录。"]
    for title in ["社区输出比较", "独立候选比较", "源端重复稳定性", "重复执行独立候选比较"]:
        if title in record:
            lines += ["", f"### {title}", "", "```json", json.dumps(record[title], ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 3. 实际错误与证据缺口", ""]
    for title in ["PostgreSQL实际结果", "社区Doris实际结果", "独立Doris实际结果", "源端重复执行结果", "目标重复执行结果"]:
        if title in record:
            r = record[title]
            lines += [f"### {title}", "", f"- {'成功；记录数 ' + str(len(r['记录'])) if r['成功'] else '失败或未取得完整结果'}。", ""]
            if r.get("错误"): lines += ["```json", json.dumps(r["错误"], ensure_ascii=False, indent=2), "```", ""]
    lines += ["未自动完成的检查：全部参数边界、数组下界/维度、完整类型域、排序键唯一性、基表一致性，以及 .out 与当前 PG 环境的完整对应关系。归因 Skill 必须区分已执行与未执行，不得把本文件当作通用同义证明。", ""]
    path = destination / "probe-report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
