# select_distinct_on：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 3 | 2 | 1 | 0 | 2 |


[YAML](../../../../../../cases/postgres/manual/current/select_distinct_on.yaml)；[首轮 Markdown](../../../validation/select_distinct_on/validation.md) / [首轮 JSON](../../../validation/select_distinct_on/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-select-distinct-on-0001

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/select_distinct_on.out)；原语句 1，源行 1–7，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

SQLGlot 原错误：


~~~text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
~~~

#### 代码依据、候选与执行

PG-DORIS-013 解析 PostgreSQL ORDER BY USING 内建比较操作符：2 条 .out 成功查询因 USING </> 被 Parser 拒绝；另 1 条源端本身报错，已排除。使用 ASC/DESC 的规范化源变体可实际执行。

代码位置：[sqlglot/parser.py:5877](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parser.py#L5877)（行 5877）；[sqlglot/parsers/postgres.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py)。

PG-DORIS-019 DISTINCT ON 降级时保留最终 ORDER BY：eliminate_distinct_on 把 order.pop() 移入 ROW_NUMBER 窗口，外层不再排序。规范化源变体的第一次候选行值相同但顺序不同；补外层 ORDER BY 后对齐。

代码位置：[sqlglot/transforms.py:144](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L144)（行 144）；[sqlglot/transforms.py:168](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L168)（行 168）；[sqlglot/generators/mysql.py:189](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L189)（行 189）。

第一次候选：


~~~sql
SELECT string4, two, ten FROM (SELECT string4 AS string4, two AS two, ten AS ten, ROW_NUMBER() OVER (PARTITION BY string4 ORDER BY string4 ASC NULLS LAST, two DESC NULLS FIRST, ten ASC NULLS LAST) AS _row_number FROM onek) AS _t WHERE _row_number = 1;
~~~

后续候选 probe-02：


~~~sql
SELECT string4,two,ten FROM (SELECT string4,two,ten,ROW_NUMBER() OVER(PARTITION BY string4 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST) AS rn FROM onek) q WHERE rn=1 ORDER BY string4 ASC NULLS LAST,two DESC NULLS FIRST,ten ASC NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-select-distinct-on-0001/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-select-distinct-on-0001/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-select-distinct-on-0001/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-select-distinct-on-0001/probe-02/probe-report.md)。

#### 最新候选分维度比较

实测源端为明确保存的规范化语法变体；原文成功证据仍来自 .out，不冒充原 SQL 实测。


~~~sql
SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 ASC, two DESC, ten ASC;
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


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

为 PG 解析内建 USING </> 并映射正确方向及默认 NULL 顺序；自定义操作符不应盲目当成 ASC/DESC。 限制：本轮因原语法触发共同 Parser，工具执行的是标明的规范化源变体；原文成功证据来自原 .out。依赖 PG-DORIS-019 保留最终顺序。

保留用于选择组内第一行的窗口排序，同时重建外层最终排序；处理投影未暴露排序键、Alias、NULL、LIMIT/OFFSET。 限制：当前两个 NAME 字段受外部类型映射限制；不把行值与顺序对齐说成全类型等价。

修复任务：[PG-DORIS-013](../sqlglot-tasks.md)；[PG-DORIS-019](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-select-distinct-on-0003

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/select_distinct_on.out)；原语句 3，源行 14–16，同文回显第 1 次；历史成功 40 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT DISTINCT ON (string4, ten) string4, ten, two
   FROM onek
   ORDER BY string4 using <, ten using >, two using <;
~~~

SQLGlot 原错误：


~~~text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4, ten) string4, ten, two
   FROM onek
   ORDER BY string4 using <, ten using >, two using <;
~~~

#### 代码依据、候选与执行

PG-DORIS-013 解析 PostgreSQL ORDER BY USING 内建比较操作符：2 条 .out 成功查询因 USING </> 被 Parser 拒绝；另 1 条源端本身报错，已排除。使用 ASC/DESC 的规范化源变体可实际执行。

代码位置：[sqlglot/parser.py:5877](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parser.py#L5877)（行 5877）；[sqlglot/parsers/postgres.py](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py)。

PG-DORIS-019 DISTINCT ON 降级时保留最终 ORDER BY：eliminate_distinct_on 把 order.pop() 移入 ROW_NUMBER 窗口，外层不再排序。规范化源变体的第一次候选行值相同但顺序不同；补外层 ORDER BY 后对齐。

代码位置：[sqlglot/transforms.py:144](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L144)（行 144）；[sqlglot/transforms.py:168](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/transforms.py#L168)（行 168）；[sqlglot/generators/mysql.py:189](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L189)（行 189）。

第一次候选：


~~~sql
SELECT string4, ten, two FROM (SELECT string4 AS string4, ten AS ten, two AS two, ROW_NUMBER() OVER (PARTITION BY string4, ten ORDER BY string4 ASC NULLS LAST, ten DESC NULLS FIRST, two ASC NULLS LAST) AS _row_number FROM onek) AS _t WHERE _row_number = 1;
~~~

后续候选 probe-02：


~~~sql
SELECT string4,ten,two FROM (SELECT string4,ten,two,ROW_NUMBER() OVER(PARTITION BY string4,ten ORDER BY string4 ASC NULLS LAST,ten DESC NULLS FIRST,two ASC NULLS LAST) AS rn FROM onek) q WHERE rn=1 ORDER BY string4 ASC NULLS LAST,ten DESC NULLS FIRST,two ASC NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-select-distinct-on-0003/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-select-distinct-on-0003/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-select-distinct-on-0003/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-select-distinct-on-0003/probe-02/probe-report.md)。

#### 最新候选分维度比较

实测源端为明确保存的规范化语法变体；原文成功证据仍来自 .out，不冒充原 SQL 实测。


~~~sql
SELECT DISTINCT ON (string4, ten) string4, ten, two
   FROM onek
   ORDER BY string4 ASC, ten DESC, two ASC;
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


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

为 PG 解析内建 USING </> 并映射正确方向及默认 NULL 顺序；自定义操作符不应盲目当成 ASC/DESC。 限制：本轮因原语法触发共同 Parser，工具执行的是标明的规范化源变体；原文成功证据来自原 .out。依赖 PG-DORIS-019 保留最终顺序。

保留用于选择组内第一行的窗口排序，同时重建外层最终排序；处理投影未暴露排序键、Alias、NULL、LIMIT/OFFSET。 限制：当前两个 NAME 字段受外部类型映射限制；不把行值与顺序对齐说成全类型等价。

修复任务：[PG-DORIS-013](../sqlglot-tasks.md)；[PG-DORIS-019](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-select-distinct-on-0002 / SELECT DISTINCT ON (string4, ten) string4, two, ten<br>   FROM onek<br>   ORDER BY string4 using <, two using <, ten using <; / [.out](../../../../../../cases/postgres/manual/current/assets/select_distinct_on.out)，语句 2 | SELECT DISTINCT ON expressions must match initial ORDER BY expressions | SQLGlot 解析/生成失败；ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.<br>  SELECT DISTINCT ON (string4, ten) string4, two, ten<br>   FROM onek<br>   ORDER BY string4 using <, two using <, ten using <; | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

