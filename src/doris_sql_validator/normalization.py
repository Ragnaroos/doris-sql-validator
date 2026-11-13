from __future__ import annotations

import base64
import math
import re
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any


def canonical_type(database_type: str | None) -> str:
    if not database_type:
        return "unknown"
    value = database_type.lower()
    if any(token in value for token in ("bool",)):
        return "boolean"
    if any(token in value for token in ("tinyint", "smallint", "bigint", "integer", "int", "long")):
        return "integer"
    if "decimal" in value or "numeric" in value:
        match = re.search(r"(?:decimal|numeric)\s*\((\d+)\s*,\s*(\d+)\)", value)
        return f"decimal({match.group(1)},{match.group(2)})" if match else "decimal"
    if any(token in value for token in ("float", "double", "real")):
        return "float"
    if any(token in value for token in ("binary", "blob")):
        return "binary"
    if "timestamp" in value or "datetime" in value:
        return "timestamp"
    if re.search(r"\bdate\b", value):
        return "date"
    if re.search(r"\btime\b", value):
        return "time"
    if "array" in value:
        return "array"
    if "map" in value:
        return "map"
    if "struct" in value or "row" in value:
        return "struct"
    if any(token in value for token in ("char", "string", "text", "json")):
        return "string"
    return value


def normalize_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, Decimal):
        return {"$decimal": format(value, "f")}
    if isinstance(value, float):
        if math.isnan(value):
            return {"$float": "nan"}
        if math.isinf(value):
            return {"$float": "infinity" if value > 0 else "-infinity"}
        return value
    if isinstance(value, bytes):
        return {"$binary": base64.b64encode(value).decode("ascii")}
    if isinstance(value, datetime):
        return {"$timestamp": value.isoformat(timespec="microseconds")}
    if isinstance(value, date):
        return {"$date": value.isoformat()}
    if isinstance(value, time):
        return {"$time": value.isoformat(timespec="microseconds")}
    if isinstance(value, (list, tuple)):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        pairs = [
            [normalize_value(key), normalize_value(item)] for key, item in value.items()
        ]
        return {"$map": sorted(pairs, key=stable_key)}
    return {"$repr": repr(value)}


def stable_key(value: Any) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

