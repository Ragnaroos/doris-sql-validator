# PostgreSQL → Doris：SQLGlot 功能补充任务

参考评估日期：2026-11-13。PG-DORIS-001 等是追踪编号，标题说明实际问题。20 项包含受限修复建议与研究/限制事项；不是 20 个可直接提交的已确认通用缺陷。

目标为相邻的 ../sqlglot checkout；评估所用社区提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9。[归因汇总](attribution-summary.md) / [逐组明细](attribution-details.md)。

## 1. 任务汇总


| 编号 | 问题 | 优先级 | 证据阶段 | 代表 |
| :--- | :--- | :--- | :--- | :--- |
| PG-DORIS-001 | Doris 数组元素构造器不应沿用 MySQL 的整体禁用 | P0 | 可实施的小范围修复 | pg-aggregates-0010-12bf388c |
| PG-DORIS-002 | 启用经实测支持的 Doris 原生 NULL 排序 | P0 | 可实施的小范围修复 | pg-union-0001-8842af4e |
| PG-DORIS-003 | 将命名 WINDOW 内联到实际窗口表达式 | P0 | 可实施的小范围修复 | pg-window-0006-bf2d68e1 |
| PG-DORIS-004 | 支持基表别名后的列名列表 | P1 | 已有无需 Schema 的对照，需完善作用域规则 | pg-join-0028-f25eea71 |
| PG-DORIS-005 | 修正 JSON 文本提取、路径参数和 JSON null | P1 | 可先修已验证标量范围；对象文本需研究 | pg-json-0153-859161a9 |
| PG-DORIS-006 | 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子 | P1 | 直接函数范围有执行证据；算子需类型分析 | pg-jsonb-0135-6b4dd957 |
| PG-DORIS-007 | 正确区分 PG 非十进制整数与位串/字节串 | P0 | 可实施，但涉及 Tokenizer/Parser 和跨方言回归 | pg-numerology-0002-4393fd29 |
| PG-DORIS-008 | 保留合法 PostgreSQL 布尔文本前缀 | P1 | 已验证正常输入，可实施受限规则 | pg-boolean-0010-222849e6 |
| PG-DORIS-009 | 对齐递归 CTE 的锚点和递归列类型 | P1 | 已有可执行对照，需类型推断方案 | pg-with-0003-18c284af |
| PG-DORIS-010 | 保留已知整数输入的 PostgreSQL 除法 | P1 | 有明确反例和对照，默认无 Schema 路径需限定 | pg-window-0050-8b853a62 |
| PG-DORIS-011 | 将多参数 GROUPING 对齐为 Doris GROUPING_ID | P1 | 已有行值与类型检查，需扩大分组边界 | pg-groupingsets-0012-47939b25 |
| PG-DORIS-012 | 避免 NATURAL FULL JOIN 在 MySQL 兼容变换中崩溃 | P0 | 代码异常已定位，Doris 显式 ON 对照已执行 | pg-join-0084-d692d7c3 |
| PG-DORIS-013 | 解析 PostgreSQL ORDER BY USING 内建比较操作符 | P1 | 合法源语法已证实，尚未修改 Parser | pg-select-distinct-on-0001 |
| PG-DORIS-014 | 保留合法 PostgreSQL 日期字面量格式 | P2 | 已确认当前格式差异，扩展格式需研究 | pg-date-0024-afe42f36 |
| PG-DORIS-015 | 为合法 MAKE_DATE 输入补充 Doris 构造规则 | P2 | 由负向线索补正常输入后取得证据 | 正常 MAKE_DATE 新变体 |
| PG-DORIS-016 | 对未映射的 PG 特有类型给出明确能力边界 | P2 | 研究/诊断改进，不是已找到等价改写 | pg-money-0057-a1bdd31a |
| PG-DORIS-017 | 研究整数 AVG 的 Decimal 精度和舍入契约 | P2 | 研究任务，当前候选不能直接提交 | pg-aggregates-0006-86de303b |
| PG-DORIS-018 | 单独评估 PG_INPUT_IS_VALID 的目标实现范围 | P2 | 研究任务，禁止用一次 TRY_CAST 代替全部类型规则 | pg-boolean-0028-50f4807b |
| PG-DORIS-019 | DISTINCT ON 降级时保留最终 ORDER BY | P0 | 代码和执行顺序差异已确认 | pg-select-distinct-on-0001 |
| PG-DORIS-020 | 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围 | P2 | 研究/限制说明，不自动补排序或修复 | pg-window-0055-461f08dc |


## PG-DORIS-001：Doris 数组元素构造器不应沿用 MySQL 的整体禁用

- [ ] 尚未实施；P0；可实施的小范围修复。

### 源端成功复现与实际差异


~~~sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/aggregates.out)；语句 10，同文回显第 1 次。

当前社区输出/错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

独立执行：[probe-01 JSON](evidence/pg-aggregates-0010-12bf388c/probe-01/probe-evidence.json) / [可读对照](evidence/pg-aggregates-0010-12bf388c/probe-01/probe-report.md)；[aggregates 详细归因](details/aggregates.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _text → array<varchar(5)>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "_text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "array<varchar(5)>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（已核对行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（已核对行 26）。

建议改动：为元素列表构造器增加 Doris 实现；静态可知元素类型时保留 PG 的元素位宽。ARRAY(SELECT...) 单独处理，不把查询构造器伪装成元素列表。

测试：普通/NULL/空数组/嵌套；32 位整数元素；数组查询构造器保持明确限制；用真正修复后的 SQLGlot 重新生成并执行。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：_int4 与 array<tinyint> 的实际位宽不同；_int4 与 array<int> 也会被当前类型声明比较器误报。需要区分表示别名与真实类型差异。

关联已选查询：pg-aggregates-0010-12bf388c、pg-arrays-0129-97df5e76、pg-arrays-0130-1a544234、pg-arrays-0131-c7124ae8、pg-arrays-0134-9c537f22、pg-arrays-0135-33e4f75c、pg-arrays-0136-911e2fbc、pg-arrays-0137-c6d3924c、pg-arrays-0138-ae9e4f97、pg-arrays-0139-8147b663、pg-arrays-0140-1ae879f3、pg-arrays-0141-e83ebde6、pg-arrays-0143-d4ff47e9、pg-arrays-0144-215ce358、pg-arrays-0146-1dba32e8、pg-arrays-0150-c883f965、pg-arrays-0152-5f46c961、pg-arrays-0153-1bce402b、pg-arrays-0154-879640d2、pg-arrays-0158-76e9e56b、pg-arrays-0160-d80d5020、pg-arrays-0161-c1ad99d8、pg-arrays-0162-94f706e5、pg-arrays-0163-7e801567、pg-arrays-0164-eba9ca06、pg-arrays-0165-befda27f、pg-arrays-0166-8cc7f264、pg-arrays-0197-7667c505、pg-arrays-0199-5d28259f、pg-arrays-0201-43f9dae0、pg-arrays-0210-f27d4da8、pg-arrays-0211-3e580130、pg-arrays-0246-58760171、pg-arrays-0247-933ca919、pg-arrays-0248-c6f58b28、pg-arrays-0249-e2238cac、pg-arrays-0250-7b229df0、pg-arrays-0251-f4b1710d、pg-arrays-0252-ce30e209、pg-arrays-0253-be3c6fa6、pg-json-0057-738e7b11、pg-json-0060-0cb6c97c、pg-json-0064-dce5ae8b、pg-json-0161-635df7fb、pg-json-0162-6b380766、pg-json-0163-093476ed、pg-json-0164-0923d889、pg-json-0165-7c004789、pg-json-0166-6c15e0b8、pg-json-0167-f3c33896、pg-json-0168-d6b16d12、pg-json-0174-ff8d41d2、pg-json-0177-0fec5401、pg-json-0194-013c6457、pg-json-0197-ffab593b、pg-jsonb-0057-0dd4ec19、pg-jsonb-0075-27aae931、pg-jsonb-0199-6e48a507、pg-jsonb-0200-15e82b89、pg-jsonb-0201-639d32ce、pg-jsonb-0202-107bfecc、pg-jsonb-0204-522fac2b、pg-jsonb-0205-5f02749a、pg-jsonb-0206-7b83fddf、pg-jsonb-0207-007c4486、pg-jsonb-0209-2a965830、pg-jsonb-0210-b407053e、pg-jsonb-0211-0441451f、pg-jsonb-0212-60b91a2b、pg-jsonb-0214-7ee1efe4、pg-jsonb-0215-44efa3b4、pg-jsonb-0216-65489bec、pg-jsonb-0217-79898f60、pg-jsonb-0218-eb3572a8、pg-subselect-0011-ba931994、pg-subselect-0012-a01c4e7d、pg-subselect-0013-9ff200d9、pg-multirangetypes-0605-e88badff、pg-rangetypes-0377-0d6fb286、pg-xml-0034-0de0843b、pg-xml-0152-481c458f、pg-xml-0153-4b9bd07b、pg-xml-0154-303139cc、pg-rowtypes-0091-02456573、pg-rowtypes-0092-99426b72、pg-rowtypes-0093-43b5e991。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| array-null-elements | [源 SQL](evidence/boundaries/array-null-elements/source.sql) / [候选](evidence/boundaries/array-null-elements/candidate.sql) | [probe](evidence/boundaries/array-null-elements/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-empty-typed | [源 SQL](evidence/boundaries/array-empty-typed/source.sql) / [候选](evidence/boundaries/array-empty-typed/candidate.sql) | [probe](evidence/boundaries/array-empty-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-nested-typed | [源 SQL](evidence/boundaries/array-nested-typed/source.sql) / [候选](evidence/boundaries/array-nested-typed/candidate.sql) | [probe](evidence/boundaries/array-nested-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<array<int>>，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-002：启用经实测支持的 Doris 原生 NULL 排序

- [ ] 尚未实施；P0；可实施的小范围修复。

### 源端成功复现与实际差异


~~~sql
SELECT 1 AS two UNION SELECT 2 ORDER BY 1;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/union.out)；语句 1，同文回显第 1 次。

当前社区输出/错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

独立执行：[probe-01 JSON](evidence/pg-union-0001-8842af4e/probe-01/probe-evidence.json) / [可读对照](evidence/pg-union-0001-8842af4e/probe-01/probe-report.md)；[union 详细归因](details/union.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT 1 AS two UNION SELECT 2 ORDER BY 1 NULLS LAST;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L127)（已核对行 127）；[sqlglot/generator.py:3317](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L3317)（已核对行 3317）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（已核对行 26）。

建议改动：核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。

测试：位置排序、ASC/DESC、NULL、重复值、窗口 RANGE/ROWS；相关 MySQL 测试不得被改变。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

关联已选查询：pg-groupingsets-0045-e2685715、pg-groupingsets-0046-ee2dc97b、pg-union-0001-8842af4e、pg-union-0002-46978a15、pg-union-0005-4e651bba、pg-union-0006-20935b45、pg-union-0007-dee35ffd、pg-union-0008-3b1c7020、pg-union-0009-774cd2a0、pg-union-0010-84c85402、pg-union-0011-043dbbe9、pg-union-0012-69bca50e、pg-union-0013-6809b41b、pg-union-0014-e4feb980、pg-union-0015-0cb45014、pg-union-0016-75c00d8c、pg-union-0017-86fb9d5a、pg-union-0027-021c0d72、pg-union-0028-cb1f47b2、pg-union-0029-6c7c44d0、pg-window-0048-536e1e97、pg-window-0049-f467131d、pg-window-0050-8b853a62、pg-window-0051-ce3792dc、pg-window-0052-682b3131、pg-sqljson-0182-0b849be1。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](evidence/boundaries/null-order-ascending/source.sql) / [候选](evidence/boundaries/null-order-ascending/candidate.sql) | [probe](evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](evidence/boundaries/null-order-descending/source.sql) / [候选](evidence/boundaries/null-order-descending/candidate.sql) | [probe](evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-003：将命名 WINDOW 内联到实际窗口表达式

- [ ] 尚未实施；P0；可实施的小范围修复。

### 源端成功复现与实际差异


~~~sql
SELECT depname, empno, salary, sum(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname);
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/window.out)；语句 6，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT depname, empno, salary, SUM(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname)
~~~


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 48)\n")
~~~

独立执行：[probe-01 JSON](evidence/pg-window-0006-bf2d68e1/probe-01/probe-evidence.json) / [可读对照](evidence/pg-window-0006-bf2d68e1/probe-01/probe-report.md)；[window 详细归因](details/window.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT depname, empno, salary, SUM(salary) OVER (PARTITION BY depname) FROM empsalary;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: varchar → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L1058)（已核对行 1058）；[sqlglot/generators/mysql.py:189](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L189)（已核对行 189）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（已核对行 26）。

建议改动：复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。

测试：空窗口、未使用窗口、同名不同作用域、继承窗口、并列键和 NULL；同时核对 SUM 返回类型。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

关联已选查询：pg-window-0006-bf2d68e1、pg-window-0007-d8c07fd5、pg-window-0009-fbac9f79、pg-window-0010-ac7b0db2、pg-window-0036-1d9414c5、pg-window-0038-4aba58d8、pg-window-0041-1b9507b3、pg-window-0068-06f27850、pg-window-0072-75e7d362。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](evidence/boundaries/named-window-null-peers/source.sql) / [候选](evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-004：支持基表别名后的列名列表

- [ ] 尚未实施；P1；已有无需 Schema 的对照，需完善作用域规则。

### 源端成功复现与实际差异


~~~sql
SELECT *
  FROM J1_TBL AS t1 (a, b, c);
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/join.out)；语句 28，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c)
~~~


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
~~~

独立执行：[probe-01 JSON](evidence/pg-join-0028-f25eea71/probe-01/probe-evidence.json) / [可读对照](evidence/pg-join-0028-f25eea71/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-join-0028-f25eea71/probe-02/probe-evidence.json) / [可读对照](evidence/pg-join-0028-f25eea71/probe-02/probe-report.md)；[join 详细归因](details/join.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT * FROM (SELECT i AS a, j AS b, t AS c FROM J1_TBL) AS t1;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


候选 probe-02（原始源 SQL）：


~~~sql
WITH _dsv_t1(a,b,c) AS (SELECT * FROM J1_TBL) SELECT * FROM _dsv_t1 AS t1;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

AS t(a,b,c) 被直接生成到 Doris 后失败。显式投影候选可行；后续 CTE 列名列表候选也已实测，可避免默认读取表 Schema。

代码位置：[sqlglot/generator.py:1628](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L1628)（已核对行 1628）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（已核对行 26）。

建议改动：研究将基表列重命名下沉到 CTE 列别名，或在已有 Schema 时改写投影；处理命名冲突和作用域，不硬编码 J1_TBL 的列。

测试：单表、双表 JOIN、部分列引用、重复列名、CTE 冲突、列数不符；区分源表 TEXT→VARCHAR(512) 的准备限制。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：现有表数据类型映射限制不是本规则造成；不能把有限 VARCHAR 说成全域 TEXT。

关联已选查询：pg-join-0028-f25eea71、pg-join-0029-f25eea71、pg-join-0030-8603f3ed、pg-join-0031-f4169150。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-005：修正 JSON 文本提取、路径参数和 JSON null

- [ ] 尚未实施；P1；可先修已验证标量范围；对象文本需研究。

### 源端成功复现与实际差异


~~~sql
select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6');
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/json.out)；语句 153，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6')
~~~

独立执行：[probe-01 JSON](evidence/pg-json-0153-859161a9/probe-01/probe-evidence.json) / [可读对照](evidence/pg-json-0153-859161a9/probe-01/probe-report.md)；[json 详细归因](details/json.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6'), NULL, JSON_EXTRACT_STRING('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6'));
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: text → json，逻辑=不同，声明=不同，精度/小数位=不适用 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L75)（已核对行 75）；[sqlglot/parsers/postgres.py:151](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py#L151)（已核对行 151）。

建议改动：为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。

测试：字符串、JSON null、SQL NULL、缺失键、嵌套路径、数组索引、换行/反斜杠；对象返回的 TEXT 不能做 JSON 归一化。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

关联已选查询：pg-json-0135-0315e130、pg-json-0153-859161a9、pg-json-0155-579440b1、pg-json-0156-f9da221f、pg-json-0158-382f7a2f、pg-json-0160-7531df7d、pg-jsonb-0124-ce70ecc5。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](evidence/boundaries/json-text-json-null/source.sql) / [候选](evidence/boundaries/json-text-json-null/candidate.sql) | [probe](evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](evidence/boundaries/json-text-missing/source.sql) / [候选](evidence/boundaries/json-text-missing/candidate.sql) | [probe](evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](evidence/boundaries/json-text-string/source.sql) / [候选](evidence/boundaries/json-text-string/candidate.sql) | [probe](evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

对象 TEXT 仍有带空格和紧凑文本差异。json-text-string 的首次反斜杠候选错误已另存 candidate-02 修正，不算 SQLGlot 缺陷；两次证据保留。

## PG-DORIS-006：补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子

- [ ] 尚未实施；P1；直接函数范围有执行证据；算子需类型分析。

### 源端成功复现与实际差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"b"}');
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/jsonb.out)；语句 135，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}')
~~~


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
~~~

独立执行：[probe-01 JSON](evidence/pg-jsonb-0135-6b4dd957/probe-01/probe-evidence.json) / [可读对照](evidence/pg-jsonb-0135-6b4dd957/probe-01/probe-report.md)；[jsonb 详细归因](details/jsonb.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}') AS BOOLEAN);
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（已核对行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（已核对行 654）。

建议改动：先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。

测试：对象包含/不包含、JSON null、SQL NULL、数组重复元素、标量/对象混合、返回 BOOLEAN；未知类型不猜测。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

关联已选查询：pg-jsonb-0135-6b4dd957、pg-jsonb-0136-4e07d50c、pg-jsonb-0137-26e8e6c3、pg-jsonb-0138-0f3fc6a3、pg-jsonb-0139-c3fabcbb、pg-jsonb-0140-6b4dd957。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](evidence/boundaries/json-containment-null/source.sql) / [候选](evidence/boundaries/json-containment-null/candidate.sql) | [probe](evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](evidence/boundaries/json-containment-sql-null/source.sql) / [候选](evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-007：正确区分 PG 非十进制整数与位串/字节串

- [ ] 尚未实施；P0；可实施，但涉及 Tokenizer/Parser 和跨方言回归。

### 源端成功复现与实际差异


~~~sql
SELECT 0o273;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；语句 2，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT 0 AS o273
~~~

独立执行：[probe-01 JSON](evidence/pg-numerology-0002-4393fd29/probe-01/probe-evidence.json) / [可读对照](evidence/pg-numerology-0002-4393fd29/probe-01/probe-report.md)；[numerology 详细归因](details/numerology.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT CAST(187 AS INT);
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/tokenizer_core.py#L1041)（已核对行 1041）；[sqlglot/tokenizer_core.py:1051](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/tokenizer_core.py#L1051)（已核对行 1051）；[sqlglot/parser.py:5877](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parser.py#L5877)（已核对行 5877）。

建议改动：在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。

测试：零、32/64 位边界、超 BIGINT、下划线、显式 Alias、负号；新边界 0o0 AS value 被 Parser 拒绝也须补回归。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

关联已选查询：pg-numerology-0001-bf1fea25、pg-numerology-0002-4393fd29、pg-numerology-0003-bc278c1f、pg-numerology-0004-5b3e7f7e、pg-numerology-0005-68d49865、pg-numerology-0006-2c1a7e8b、pg-numerology-0007-113b58a4、pg-numerology-0008-e7bc3623、pg-numerology-0009-69ae7cae、pg-numerology-0016-554fa98c、pg-numerology-0017-73d4763f、pg-numerology-0018-7a05d9a2、pg-numerology-0019-335c2dae、pg-numerology-0020-885d9173、pg-numerology-0021-65b661c9、pg-numerology-0049-9b45177b、pg-numerology-0050-0c169c9a、pg-numerology-0051-33408a72。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](evidence/boundaries/numeric-octal-zero/source.sql) / [候选](evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-008：保留合法 PostgreSQL 布尔文本前缀

- [ ] 尚未实施；P1；已验证正常输入，可实施受限规则。

### 源端成功复现与实际差异


~~~sql
SELECT bool 'y' AS true;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；语句 10，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT CAST('y' AS BOOLEAN) AS `true`
~~~

独立执行：[probe-01 JSON](evidence/pg-boolean-0010-222849e6/probe-01/probe-evidence.json) / [可读对照](evidence/pg-boolean-0010-222849e6/probe-01/probe-report.md)；[boolean 详细归因](details/boolean.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT CAST(CASE WHEN LOWER(TRIM('y')) IN ('true', 't', 'tr', 'tru', 'yes', 'y', 'ye', 'on', '1') THEN 'true' WHEN LOWER(TRIM('y')) IN ('false', 'f', 'fa', 'fal', 'fals', 'no', 'n', 'off', 'of', '0') THEN 'false' ELSE 'y' END AS BOOLEAN) AS `true`;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

PG 的 y/n/of 是合法输入；当前 Doris CAST 返回 NULL。基于 LOWER/TRIM 的合法前缀规范化候选取得相同 BOOLEAN 和行值。

代码位置：[sqlglot/generator.py:4281](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L4281)（已核对行 4281）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）。

建议改动：对明确文本→BOOLEAN 转换进行规范化，支持合法前缀、大小写和空白；不从返回值拼常量，不默认承担非法输入错误复刻。

测试：y/n/of、完整 true/false、空白大小写、SQL NULL；动态文本参数；非法输入仅在专项验收时检查错误行为。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：不能把接受前缀的规则应用到所有类型或把含糊的 o 当成合法值。

关联已选查询：pg-boolean-0010-222849e6、pg-boolean-0013-41441aee、pg-boolean-0018-0e6e96f9。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| boolean-case-space | [源 SQL](evidence/boundaries/boolean-case-space/source.sql) / [候选](evidence/boundaries/boolean-case-space/candidate.sql) | [probe](evidence/boundaries/boolean-case-space/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| boolean-sql-null | [源 SQL](evidence/boundaries/boolean-sql-null/source.sql) / [候选](evidence/boundaries/boolean-sql-null/candidate.sql) | [probe](evidence/boundaries/boolean-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-009：对齐递归 CTE 的锚点和递归列类型

- [ ] 尚未实施；P1；已有可执行对照，需类型推断方案。

### 源端成功复现与实际差异


~~~sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/with.out)；语句 3，同文回显第 1 次。

当前社区输出/错误：


~~~sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT 1) AS _values UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t
~~~


~~~text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
~~~

独立执行：[probe-01 JSON](evidence/pg-with-0003-18c284af/probe-01/probe-evidence.json) / [可读对照](evidence/pg-with-0003-18c284af/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-with-0003-18c284af/probe-02/probe-evidence.json) / [可读对照](evidence/pg-with-0003-18c284af/probe-02/probe-report.md)；[with 详细归因](details/with.md)。

候选 probe-01（原始源 SQL）：


~~~sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT 1) AS _values UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


候选 probe-02（原始源 SQL）：


~~~sql
WITH RECURSIVE t(n) AS (SELECT CAST(1 AS INT) UNION ALL SELECT CAST(n+1 AS INT) FROM t WHERE n<100) SELECT SUM(n) FROM t;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

PG 锚点 VALUES(1) 的 INT 语义没有传到 Doris 的最小宽度字面量；当前 Doris 报 TINYINT 锚点与 SMALLINT 递归列不一致。显式双端 INT 的递归候选成功。

代码位置：[sqlglot/generator.py:1610](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L1610)（已核对行 1610）；[sqlglot/generator.py:1801](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L1801)（已核对行 1801）；[sqlglot/optimizer/annotate_types.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/optimizer/annotate_types.py)。

建议改动：在静态可推断的递归列中对齐类型，不全局把每个数字写成 INT；列、NULL、联合和溢出场景说明所需元数据。

测试：简单序列、空递归、跨最小整数宽度、NULL 锚点、多个递归列；重新运行原 WITH 查询。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：不能靠放大/缩小数据或更改递归终止条件绕过问题。

关联已选查询：pg-with-0003-18c284af。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| recursive-cte-integer-anchor | [源 SQL](evidence/boundaries/recursive-cte-integer-anchor/source.sql) / [候选](evidence/boundaries/recursive-cte-integer-anchor/candidate.sql) | [probe](evidence/boundaries/recursive-cte-integer-anchor/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-010：保留已知整数输入的 PostgreSQL 除法

- [ ] 尚未实施；P1；有明确反例和对照，默认无 Schema 路径需限定。

### 源端成功复现与实际差异


~~~sql
SELECT four, ten/4 as two,
	sum(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row),
	last_value(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/window.out)；语句 50，同文回显第 1 次。

当前社区输出/错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
~~~

独立执行：[probe-01 JSON](evidence/pg-window-0050-8b853a62/probe-01/probe-evidence.json) / [可读对照](evidence/pg-window-0050-8b853a62/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-window-0050-8b853a62/probe-02/probe-evidence.json) / [可读对照](evidence/pg-window-0050-8b853a62/probe-02/probe-report.md)；[window 详细归因](details/window.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT four, ten / 4 AS two, SUM(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → double，逻辑=不同，声明=不同，精度/小数位=不适用；3: int8 → double，逻辑=不同，声明=不同，精度/小数位=不适用；4: int4 → double，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


候选 probe-02（原始源 SQL）：


~~~sql
SELECT four, CAST(ten DIV 4 AS INT) AS two, SUM(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

窗口查询中的整数列除法在 Doris 变成分数，改变 ORDER BY/RANGE 的分组和结果；DIV 加 INT 类型对齐候选修复了两个具体样本的行值。

代码位置：[sqlglot/generator.py:4621](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L4621)（已核对行 4621）；[sqlglot/parsers/postgres.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py)；[sqlglot/optimizer/annotate_types.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/optimizer/annotate_types.py)。

建议改动：利用可靠类型信息生成整数除法和正确返回位宽，保留朝零截断；未知列类型时不得把所有 / 改成 DIV。

测试：正/负、NULL、整数位宽、DECIMAL/DOUBLE 不受影响、窗口 RANGE 和普通投影；明确默认未传 Schema 时的限制。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：若必须依赖 annotate_types/Schema，说明调用条件，不能在验证器中偷偷补类型或注入改写。

关联已选查询：pg-window-0050-8b853a62、pg-window-0051-ce3792dc。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| integer-division-negative | [源 SQL](evidence/boundaries/integer-division-negative/source.sql) / [候选](evidence/boundaries/integer-division-negative/candidate.sql) | [probe](evidence/boundaries/integer-division-negative/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

这两个窗口样本还依赖 PG-DORIS-002；多个规则组合成功不能证明仅改除法即可。显式传 Schema/annotate_types 与默认无 Schema 链路分别验收。

## PG-DORIS-011：将多参数 GROUPING 对齐为 Doris GROUPING_ID

- [ ] 尚未实施；P1；已有行值与类型检查，需扩大分组边界。

### 源端成功复现与实际差异


~~~sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b);
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/groupingsets.out)；语句 12，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b)
~~~


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
~~~

独立执行：[probe-01 JSON](evidence/pg-groupingsets-0012-47939b25/probe-01/probe-evidence.json) / [可读对照](evidence/pg-groupingsets-0012-47939b25/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-groupingsets-0012-47939b25/probe-02/probe-evidence.json) / [可读对照](evidence/pg-groupingsets-0012-47939b25/probe-02/probe-report.md)；[groupingsets 详细归因](details/groupingsets.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT a,b,GROUPING_ID(a,b),SUM(v),COUNT(*),MAX(v) FROM gstest1 GROUP BY ROLLUP(a,b);
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；5: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；6: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


候选 probe-02（原始源 SQL）：


~~~sql
SELECT a,b,CAST(GROUPING_ID(a,b) AS INT),SUM(v),COUNT(*),MAX(v) FROM gstest1 GROUP BY ROLLUP(a,b);
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；5: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；6: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

当前 GROUPING(a,b) 在 Doris 失败；GROUPING_ID(a,b) 可以执行。后续候选显式转 INT 以保留 PG grouping 返回类型。

代码位置：[sqlglot/expressions/aggregate.py:144](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/aggregate.py#L144)（已核对行 144）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）。

建议改动：为多参数 Grouping 建立 Doris 生成规则，核实位序和返回类型；不要混淆 Grouping 与 GroupingId。

测试：ROLLUP/CUBE/空分组、真实 NULL 与汇总 NULL、参数位序、单参数；同时检查 SUM 类型。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：当前只对选中 gstest1 样本实际对照，复杂 ordered-set 聚合不是本任务已修内容。

关联已选查询：pg-groupingsets-0012-47939b25。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-012：避免 NATURAL FULL JOIN 在 MySQL 兼容变换中崩溃

- [ ] 尚未实施；P0；代码异常已定位，Doris 显式 ON 对照已执行。

### 源端成功复现与实际差异


~~~sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL FULL JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/join.out)；语句 84，同文回显第 1 次。

当前社区输出/错误：


~~~text
TypeError: 'NoneType' object is not iterable
~~~

独立执行：[probe-02 JSON](evidence/pg-join-0084-d692d7c3/probe-02/probe-evidence.json) / [可读对照](evidence/pg-join-0084-d692d7c3/probe-02/probe-report.md)；[join 详细归因](details/join.md)。

候选 probe-02（原始源 SQL）：


~~~sql
SELECT COALESCE(s2.name,s3.name) AS name,s2.s2_n,s2.s2_2,s3.s3_n,s3.s3_2 FROM (SELECT name,n AS s2_n,2 AS s2_2 FROM t2) s2 FULL JOIN (SELECT name,n AS s3_n,3 AS s3_2 FROM t3) s3 ON s2.name=s3.name;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；5: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

eliminate_full_outer_join 对 NATURAL FULL JOIN 的 using=None 迭代触发 TypeError，3 条合法查询无法生成。显式 FULL JOIN ON + COALESCE 的独立候选行值一致。

代码位置：[sqlglot/transforms.py:685](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L685)（已核对行 685）；[sqlglot/transforms.py:706](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L706)（已核对行 706）；[sqlglot/generators/mysql.py:189](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L189)（已核对行 189）。

建议改动：Doris 不应无条件沿用 MySQL 的 FULL JOIN 模拟；对 NATURAL/USING 的公共列识别和投影有明确策略，不能仅吞掉 TypeError。

测试：单层/嵌套、无匹配行、NULL Key、重复行、公共列顺序；星号且无 Schema 时明确限制。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：类型受准备阶段 NAME/TEXT→VARCHAR(512) 影响，不能据本批行值一致证明全类型域。

关联已选查询：pg-join-0084-d692d7c3、pg-join-0087-f13d67d0、pg-join-0088-9518261f。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-013：解析 PostgreSQL ORDER BY USING 内建比较操作符

- [ ] 尚未实施；P1；合法源语法已证实，尚未修改 Parser。

### 源端成功复现与实际差异


~~~sql
SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/select_distinct_on.out)；语句 1，同文回显第 1 次。

当前社区输出/错误：


~~~text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

独立执行：[probe-01 JSON](evidence/pg-select-distinct-on-0001/probe-01/probe-evidence.json) / [可读对照](evidence/pg-select-distinct-on-0001/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-select-distinct-on-0001/probe-02/probe-evidence.json) / [可读对照](evidence/pg-select-distinct-on-0001/probe-02/probe-report.md)；[select_distinct_on 详细归因](details/select_distinct_on.md)。

候选 probe-01（明确标明的源语法变体）：


~~~sql
SELECT string4, two, ten FROM (SELECT string4 AS string4, two AS two, ten AS ten, ROW_NUMBER() OVER (PARTITION BY string4 ORDER BY string4 ASC NULLS LAST, two DESC NULLS FIRST, ten ASC NULLS LAST) AS _row_number FROM onek) AS _t WHERE _row_number = 1;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 不同，需检查并列排序 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: name → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "name",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "不同，需检查并列排序",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


候选 probe-02（明确标明的源语法变体）：


~~~sql
SELECT string4,two,ten FROM (SELECT string4,two,ten,ROW_NUMBER() OVER(PARTITION BY string4 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST) AS rn FROM onek) q WHERE rn=1 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: name → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "name",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

2 条 .out 成功查询因 USING </> 被 Parser 拒绝；另 1 条源端本身报错，已排除。使用 ASC/DESC 的规范化源变体可实际执行。

代码位置：[sqlglot/parser.py:5877](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parser.py#L5877)（已核对行 5877）；[sqlglot/parsers/postgres.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py)。

建议改动：为 PG 解析内建 USING </> 并映射正确方向及默认 NULL 顺序；自定义操作符不应盲目当成 ASC/DESC。

测试：内建 </>、显式 NULLS、DISTINCT ON、Alias/表达式；源端非法 DISTINCT ON 顺序保留为负向说明，不要求复刻。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：本轮因原语法触发共同 Parser，工具执行的是标明的规范化源变体；原文成功证据来自原 .out。依赖 PG-DORIS-019 保留最终顺序。

关联已选查询：pg-select-distinct-on-0001、pg-select-distinct-on-0003。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-014：保留合法 PostgreSQL 日期字面量格式

- [ ] 尚未实施；P2；已确认当前格式差异，扩展格式需研究。

### 源端成功复现与实际差异


~~~sql
SELECT date 'January 8, 1999';
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/date.out)；语句 24，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT CAST('January 8, 1999' AS DATE)
~~~

独立执行：[probe-01 JSON](evidence/pg-date-0024-afe42f36/probe-01/probe-evidence.json) / [可读对照](evidence/pg-date-0024-afe42f36/probe-01/probe-report.md)；[date 详细归因](details/date.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT CAST(STR_TO_DATE('January 8, 1999','%M %e, %Y') AS DATE);
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "date",<br>      "Doris原生类型": "date",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "date",<br>      "Doris原生类型": "datev2",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

January 8, 1999 在 PG 为成功 DATE，普通 Doris CAST 返回 NULL；指定格式 STR_TO_DATE 的候选和闰年正常变体成功。

代码位置：[sqlglot/generator.py:4281](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L4281)（已核对行 4281）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）。

建议改动：对可无歧义识别的字面量格式转换，或显式保留支持限制；不能硬编码当前日期答案。

测试：英文月份、闰日、NULL、不同合法格式；DateStyle/locale 歧义必须说明。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：只验证了列明格式；不宣称任意 PG 日期字符串、BC/Infinity 或全域日期可支持。

关联已选查询：pg-date-0024-afe42f36。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| date-month-name-leap | [源 SQL](evidence/boundaries/date-month-name-leap/source.sql) / [候选](evidence/boundaries/date-month-name-leap/candidate.sql) | [probe](evidence/boundaries/date-month-name-leap/probe/probe-evidence.json)：值与重复次数=一致；1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-015：为合法 MAKE_DATE 输入补充 Doris 构造规则

- [ ] 尚未实施；P2；由负向线索补正常输入后取得证据。

### 源端成功复现与实际差异

原非法日期只提供线索，不作为修复依据。以下新变体 PG 实测成功，不借用原负向 .out：


~~~sql
SELECT y,m,d,MAKE_DATE(y,m,d) AS value FROM (VALUES(2013,2,28),(2024,2,29),(NULL,2,28)) v(y,m,d) ORDER BY y NULLS LAST;
~~~


~~~sql
SELECT y,m,d,CAST(CONCAT(CAST(y AS STRING),'-',LPAD(CAST(m AS STRING),2,'0'),'-',LPAD(CAST(d AS STRING),2,'0')) AS DATE) AS value FROM (SELECT CAST(2013 AS INT) y,CAST(2 AS INT) m,CAST(28 AS INT) d UNION ALL SELECT CAST(2024 AS INT),CAST(2 AS INT),CAST(29 AS INT) UNION ALL SELECT CAST(NULL AS INT),CAST(2 AS INT),CAST(28 AS INT)) v ORDER BY y NULLS LAST;
~~~

[完整实际证据](evidence/boundaries/make-date-valid-and-null/probe/probe-evidence.json)。

### 修改依据、依赖与验收

原非法日期不建立修复任务。新只读变体用正常日期、闰日和 NULL 在 PG 成功，Doris 按 y/m/d 组装 DATE 的候选对齐。

代码位置：[sqlglot/parsers/postgres.py:135](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py#L135)（已核对行 135）；[sqlglot/expressions/temporal.py:293](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/temporal.py#L293)（已核对行 293）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）。

建议改动：研究 DateFromParts/匿名 MAKE_DATE 到 Doris 的规则，保留 NULL 和有效日期范围；不要把三参数 MAKE_DATE 直接改成两参数 MAKEDATE。

测试：动态 y/m/d、闰日、NULL、合法年份界限；非法日期错误仅在用户要求的专项中验收。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：本任务依据是正常输入新变体，不是原负向错误；BC/目标日期域外不在当前已验证范围。

关联已选查询：本项依据正常新变体或类型专项；不从原负向例建立修复积压。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| make-date-valid-and-null | [源 SQL](evidence/boundaries/make-date-valid-and-null/source.sql) / [候选](evidence/boundaries/make-date-valid-and-null/candidate.sql) | [probe](evidence/boundaries/make-date-valid-and-null/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

## PG-DORIS-016：对未映射的 PG 特有类型给出明确能力边界

- [ ] 尚未实施；P2；研究/诊断改进，不是已找到等价改写。

### 源端成功复现与实际差异


~~~sql
SELECT '1234567890'::money;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/expanded/assets/money.out)；语句 57，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT CAST('1234567890' AS MONEY)
~~~


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MONEY' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 28)\n")
~~~

独立执行：没有完整工具证据；[money 详细归因](details/money.md)。

代表例未取得完整工具 JSON，只能据具体错误研究，不是已经验收的改写。

### 修改依据、依赖与验收

MONEY、Range/Multirange、Interval/复合类型在多组成功源查询中被原样生成成 Doris 不接受的形式。还没有证明通用无损映射。

代码位置：[sqlglot/generator.py:1801](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L1801)（已核对行 1801）；[sqlglot/generators/doris.py:38](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L38)（已核对行 38）。

建议改动：逐类型核查可表达域和操作；不支持时给明确 unsupported，不发送显然不兼容的 CAST；不要把改报错当成已补齐能力。

测试：CAST 与合法 interval 日期运算分开；金额 locale/精度，range 边界/空区间，复合 NULL；需额外框架类型序列化支持时先列依赖。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：Doris 官方数据同步的 STRING 映射并不保留 SQL 运算语义，不能据此全局转 STRING。

关联已选查询：本项依据正常新变体或类型专项；不从原负向例建立修复积压。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-017：研究整数 AVG 的 Decimal 精度和舍入契约

- [ ] 尚未实施；P2；研究任务，当前候选不能直接提交。

### 源端成功复现与实际差异


~~~sql
SELECT avg(a) AS avg_32 FROM aggtest WHERE a < 100;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/aggregates.out)；语句 6，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT AVG(a) AS avg_32 FROM aggtest WHERE a < 100
~~~

独立执行：[probe-01 JSON](evidence/pg-aggregates-0006-86de303b/probe-01/probe-evidence.json) / [可读对照](evidence/pg-aggregates-0006-86de303b/probe-01/probe-report.md)；[aggregates 详细归因](details/aggregates.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT AVG(CAST(a AS DECIMAL(38,16))) AS avg_32 FROM aggtest WHERE a < 100;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: numeric → double，逻辑=不同，声明=不同，精度/小数位=信息不足 | 1: numeric → decimalv3(38,16)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(38,16)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

AVG(INT) 当前返回 DOUBLE；转 DECIMAL(38,16) 对 1.5 样本行值一致，但 32.6666666666666667 仍变成 ...6666。

代码位置：[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）；[sqlglot/optimizer/annotate_types.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/optimizer/annotate_types.py)。

建议改动：查清 PG NUMERIC 与 Doris AVG 的精度/舍入，不把固定 Scale 当成普适修复；先补可实施策略或标注不可无损范围。

测试：整除/循环小数、正负、NULL、空组、大数、溢出、类型/Scale；排除显示格式与真实值差异。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：不能用 Float 容差抹平 Decimal，也不能从已知源答案拼出一位尾数。

关联已选查询：pg-aggregates-0005-11b43275、pg-aggregates-0006-86de303b。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-018：单独评估 PG_INPUT_IS_VALID 的目标实现范围

- [ ] 尚未实施；P2；研究任务，禁止用一次 TRY_CAST 代替全部类型规则。

### 源端成功复现与实际差异


~~~sql
SELECT pg_input_is_valid('asdf', 'bool');
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；语句 28，同文回显第 1 次。

当前社区输出/错误：


~~~sql
SELECT PG_INPUT_IS_VALID('asdf', 'bool')
~~~


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
~~~

独立执行：[probe-01 JSON](evidence/pg-boolean-0028-50f4807b/probe-01/probe-evidence.json) / [可读对照](evidence/pg-boolean-0028-50f4807b/probe-01/probe-report.md)；[boolean 详细归因](details/boolean.md)。

候选 probe-01（原始源 SQL）：


~~~sql
SELECT PG_INPUT_IS_VALID('asdf', 'bool');
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


### 修改依据、依赖与验收

pg_input_is_valid('true','bool') 和 ('asdf','bool') 都是成功源查询，分别返回 true/false；Doris 缺少同名函数。它们不是源端负向用例。

代码位置：[sqlglot/generator.py:4148](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L4148)（已核对行 4148）；[sqlglot/parsers/postgres.py:135](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py#L135)（已核对行 135）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（已核对行 57）。

建议改动：逐源类型评估合法值检测和 NULL 行为；无法保留 PG 输入规则时明确不支持，不盲目替换成 TRY_CAST IS NOT NULL。

测试：合法/非法参数但函数成功、SQL NULL、PG 布尔前缀、数值范围、日期/JSON/数组；需类型元数据则先说明。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：正常 false 结果不可因为输入包含 bad/asdf 就排除。当前仅确认同名直译失败，没有已验收通用模拟。

关联已选查询：本项依据正常新变体或类型专项；不从原负向例建立修复积压。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## PG-DORIS-019：DISTINCT ON 降级时保留最终 ORDER BY

- [ ] 尚未实施；P0；代码和执行顺序差异已确认。

### 源端成功复现与实际差异


~~~sql
SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/select_distinct_on.out)；语句 1，同文回显第 1 次。

当前社区输出/错误：


~~~text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

独立执行：[probe-01 JSON](evidence/pg-select-distinct-on-0001/probe-01/probe-evidence.json) / [可读对照](evidence/pg-select-distinct-on-0001/probe-01/probe-report.md)；[probe-02 JSON](evidence/pg-select-distinct-on-0001/probe-02/probe-evidence.json) / [可读对照](evidence/pg-select-distinct-on-0001/probe-02/probe-report.md)；[select_distinct_on 详细归因](details/select_distinct_on.md)。

候选 probe-01（明确标明的源语法变体）：


~~~sql
SELECT string4, two, ten FROM (SELECT string4 AS string4, two AS two, ten AS ten, ROW_NUMBER() OVER (PARTITION BY string4 ORDER BY string4 ASC NULLS LAST, two DESC NULLS FIRST, ten ASC NULLS LAST) AS _row_number FROM onek) AS _t WHERE _row_number = 1;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 不同，需检查并列排序 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: name → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "name",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "不同，需检查并列排序",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


候选 probe-02（明确标明的源语法变体）：


~~~sql
SELECT string4,two,ten FROM (SELECT string4,two,ten,ROW_NUMBER() OVER(PARTITION BY string4 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST) AS rn FROM onek) q WHERE rn=1 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: name → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "name",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "name",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


### 修改依据、依赖与验收

eliminate_distinct_on 把 order.pop() 移入 ROW_NUMBER 窗口，外层不再排序。规范化源变体的第一次候选行值相同但顺序不同；补外层 ORDER BY 后对齐。

代码位置：[sqlglot/transforms.py:144](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L144)（已核对行 144）；[sqlglot/transforms.py:168](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L168)（已核对行 168）；[sqlglot/generators/mysql.py:189](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L189)（已核对行 189）。

建议改动：保留用于选择组内第一行的窗口排序，同时重建外层最终排序；处理投影未暴露排序键、Alias、NULL、LIMIT/OFFSET。

测试：普通 DISTINCT ON、USING 依赖 Parser 任务、ASC/DESC、NULL、并列选择键、非投影排序表达式；检查受公共变换影响的其他 dialect。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：当前两个 NAME 字段受外部类型映射限制；不把行值与顺序对齐说成全类型等价。

关联已选查询：pg-select-distinct-on-0001、pg-select-distinct-on-0003。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

PG-DORIS-013 是本批 ORDER BY USING 端到端依赖；普通 DISTINCT ON 最终排序可先单独修。probe-01 的行值相同/顺序不同仍保留，不能只展示 probe-02。

## PG-DORIS-020：明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围

- [ ] 尚未实施；P2；研究/限制说明，不自动补排序或修复。

### 源端成功复现与实际差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude no others),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

[.out 成功原件](../../../../../cases/postgres/manual/current/assets/window.out)；语句 55，同文回显第 1 次。

当前社区输出/错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

独立执行：[probe-02 JSON](evidence/pg-window-0055-461f08dc/probe-02/probe-evidence.json) / [可读对照](evidence/pg-window-0055-461f08dc/probe-02/probe-report.md)；[window 详细归因](details/window.md)。

候选 probe-02（原始源 SQL）：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 2 following), unique1, four FROM tenk1 WHERE unique1 < 10;
~~~


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


### 修改依据、依赖与验收

部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L3699)（已核对行 3699）；[sqlglot/generators/mysql.py:127](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L127)（已核对行 127）。

建议改动：区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。

测试：有/无 ORDER BY、并列键、ROWS/RANGE、各 EXCLUDE 形式；无确定顺序时报告非确定性，不进行虚假的严格行值验收。

验收：必须用真正修改后的 SQLGlot 从不变源 SQL 生成 Doris SQL，再按状态、字段数/显式 Alias、类型及精度/Scale、完整有限行值/重复次数和最终顺序回归；不以手写候选替代生成器回归，不改 .out、数据或放宽全部类型比较。

限制/前提：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

关联已选查询：pg-window-0055-461f08dc、pg-window-0056-323a4316、pg-window-0057-e7f23b7b、pg-window-0058-a6d78a71、pg-window-0059-b05800ec、pg-window-0060-fb3b911d、pg-window-0061-82375ee3、pg-window-0062-c3b04485、pg-window-0063-39c9997e、pg-window-0064-2e7cfd65、pg-window-0069-289c97b4、pg-window-0070-e6a99045、pg-window-0071-d0e8311e。共享规则不代表这些复杂 SQL 都已修复。

### 已测共享边界与反例

本规则没有新边界执行记录；不能宣称本例全部边界通过。

## 3. 不能直接安排 SQLGlot 补丁的事项


| 问题 | 现有证据 | 去向/原因 |
| :--- | :--- | :--- |
| PG 特有类型和缺少同名函数 | Interval、MONEY、Range/Multirange、ROW/XML 等见各组具体错误 | 研究安全映射或明确限制；一次目标失败不证明没有等价模拟，STRING 同步映射不等于 SQL 运算语义 |
| 工具执行前校验旧社区 SQL | 9 条 JSONB 顶层键操作、MONEY 等未能形成完整 probe | 先修诊断证据采集；不能说成 Doris 实际执行失败，本轮没有改框架 |
| Range/Multirange JSON 编码 | 3 条序列化失败见 probe-index.json | 框架结果编码依赖；执行尝试不等于保存了完整比较 |
| 数组声明类型别名 | _int4 与 array<int> 声明格式误报；array<tinyint> 则位宽真不同 | 统一等价别名但保留元素位宽、NULL 与数组下界，不全转字符串 |
| float4 SUM 显示/驱动/累计 | 431.773 与 431.7726 尚未充分区分 | 先查 extra_float_digits=0 与驱动解码/二进制，不能盲目 ROUND |
| 外部数据类型域 | 记录已核验，NAME/TEXT 映射为 VARCHAR(512) | 是准备限制，不证明全类型域，不修改原表来提高匹配 |
| 未执行主范围 982 条 | 各组逐条保留原 SQL/错误 | 后续补代码依据和候选执行，不当 982 个确定缺陷 |
| 源端负向 298 条 | 逐组简表保留具体错误与目标表现 | 默认不改写、不进入主修复；正常返回 false 不能误排除 |


