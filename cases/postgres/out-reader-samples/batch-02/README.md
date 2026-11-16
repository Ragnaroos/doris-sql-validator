# PostgreSQL 扩展输出读取样本

本目录只用于测试 SQL 导入、官方 `.out` 定位和结果文本读取，不包含数据库执行或验证报告。基础格式样本见 [上级目录](../README.md)。

## 上游来源

- 仓库：[postgres/postgres](https://github.com/postgres/postgres)。
- 固定 Commit：`e405a46c45bae070364ed143fb9d5a631422e5e4`。
- SQL：`src/test/regress/sql/<name>.sql`。
- 输出：`src/test/regress/expected/<name>.out`。
- `assets/` 中保存完整官方文件，未筛改源 SQL 或答案。版权说明沿用上级目录的 `UPSTREAM_COPYRIGHT`。

## 文件内容

| 文件名（各有 `.sql` 和 `.out`） | 主要查询内容 |
| :--- | :--- |
| `bit` | 定长/变长位串、转换、运算及非法输入 |
| `numerology` | 数字字面量、数值类型混合计算和转换 |
| `select_having` | HAVING、聚合与空结果 |
| `select_implicit` | 隐式输出列、分组与排序规则 |
| `select_views` | 视图查询、关联、嵌套查询与定义检查 |
| `collate` | 排序规则、字符串比较与排序 |
| `sqljson` | SQL/JSON 构造、聚合、类型和错误行为 |
| `sqljson_queryfuncs` | SQL/JSON 查询函数、路径及错误处理 |
| `rangetypes` | 范围值、范围运算、构造与边界 |
| `multirangetypes` | 多范围值、集合运算和边界 |
| `xml` | XML 文本、XPath、XMLTABLE 与展开/多行输出 |
| `domain` | Domain 类型、约束、转换及错误行为 |

这些脚本自身均有建表 DDL；完整文件还包含非查询语句、部分环境依赖和不同数据阶段。保留它们是为了测试真实回归文件的导入，不代表框架会执行 DDL/DML，也不保证脚本可在空库中独立重放。执行查询前需自行准备系统目录、排序规则、公共回归表等前提。

## 复现导入

在项目根目录执行，例如：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input cases/postgres/out-reader-samples/batch-02/assets/xml.sql \
  --recorded-output cases/postgres/out-reader-samples/batch-02/assets/xml.out \
  --output cases/postgres/out-reader-samples/batch-02/generated-xml.yaml

.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/out-reader-samples/batch-02/generated-xml.yaml
```

将 `xml` 换成表中其他文件名即可。YAML 中只保留可导入查询，并引用对应 `.out`；未导入原因保存在 `import_diagnostics`。`recorded_output` 诊断需要结合错误文字区分找不到 SQL 回显、输出格式无法读取和结果结构不完整，不能都归为 SQL 定位失败。源 SQL 解析/语句识别失败与 `.out` 读取失败分开保留。

读取器按完整外层 SQL 回显定位，并支持 XML 多行 WARNING；PREPARE、EXPLAIN 等语句内的同文 SELECT 不作为独立查询计数。PREPARE/EXPLAIN 等非查询语句不会因此被执行。

导入成功只表示当前读取器取得了结果文本或参考错误，不证明转译正确、两端语义相同，也不提供完整原生类型信息。以上导入/检查命令不执行 `run`，不连接 PG/Doris，不修改读取器或 SQLGlot，也不生成报告。
