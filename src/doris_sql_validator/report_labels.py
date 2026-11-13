"""Chinese explanations for stable machine-readable result codes."""

OUTCOMES = {
    "MATCH": "已有证据未发现差异（不代表所有类型和输入均已验证）",
    "TRANSLATION_FAILED": "SQLGlot 解析或生成失败",
    "SOURCE_EVIDENCE_UNAVAILABLE": "无法取得或解析源端参考结果",
    "TARGET_EXECUTION_FAILED": "Doris 执行流程失败",
    "EXECUTION_STATUS_MISMATCH": "两端执行状态不同：一端成功、一端失败",
    "ERROR_BEHAVIOR_MISMATCH": "两端均报错，但错误类别不同",
    "RESULT_SCHEMA_MISMATCH": "返回字段数量、名称或类型不同",
    "ROW_COUNT_MISMATCH": "返回记录行数不同",
    "ROW_VALUE_MISMATCH": "返回记录值、重复次数或要求的顺序不同",
    "SOURCE_ENVIRONMENT_ERROR": "源数据库环境不可用",
    "TARGET_ENVIRONMENT_ERROR": "Doris 环境不可用，例如数据库、表或权限缺失",
    "ENVIRONMENT_ERROR": "至少一端环境不可用",
    "UNKNOWN": "没有形成比较结论",
}

ERRORS = {
    "CONNECTION_ERROR": "连接失败", "DATABASE_NOT_FOUND": "数据库不存在或未选择",
    "TABLE_NOT_FOUND": "表不存在", "PERMISSION_DENIED": "权限不足",
    "TIMEOUT": "执行超时", "PARSE_ERROR": "语法解析失败",
    "FUNCTION_NOT_FOUND": "函数不存在或调用形式不受支持",
    "CAST_ERROR": "类型转换失败", "EXECUTION_ERROR": "执行失败，需阅读具体错误",
    "UNKNOWN": "错误类别未知",
}


def explain(code: str, labels=OUTCOMES) -> str:
    return labels.get(code, "未识别的内部代码，请结合完整执行证据判断")


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
