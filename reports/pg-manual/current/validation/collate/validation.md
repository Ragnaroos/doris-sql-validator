# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:26.121768+00:00 至 2026-11-11T09:40:26.203347+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/collate.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**4**；两端成功且已有证据匹配：**3**。
- 成功结果匹配占全部查询比例：**3/4 = 75.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**3/3 = 100.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**1**；不计入上述成功匹配分子。
- 需要分析的查询：**1**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**1**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 3 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 4 条只读查询、跳过 138 条非查询、0 条待确认、4 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–13 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 14–14 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 3 | 16–19 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 4 | 21–26 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 5 | 28–30 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 6 | 32–37 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 7 | 39–39 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 40–40 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 45–47 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 14 | 48–48 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 15 | 48–52 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 16 | 53–53 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 56–59 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 19 | 60–60 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 28 | 77–83 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 29 | 85–85 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 33 | 92–94 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 34 | 95–95 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 35 | 96–96 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 48 | 119–119 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 71 | 147–149 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 83 | 180–183 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 87 | 193–194 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 90 | 200–202 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 91 | 203–203 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 92 | 204–204 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 93 | 204–205 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 94 | 207–207 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 95 | 207–208 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 97 | 213–217 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 98 | 218–218 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 99 | 219–219 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 100 | 221–221 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 101 | 222–222 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 102 | 223–223 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 103 | 224–224 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 104 | 225–225 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 105 | 225–226 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 106 | 227–227 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 107 | 228–228 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 108 | 228–229 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 109 | 230–230 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 110 | 232–232 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 111 | 233–233 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 112 | 234–234 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 113 | 237–240 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 114 | 241–242 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 115 | 245–247 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 117 | 251–251 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 118 | 251–252 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 119 | 252–253 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 120 | 253–255 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 121 | 256–256 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 122 | 257–257 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 123 | 257–259 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 124 | 260–260 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 125 | 261–261 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 126 | 261–264 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 127 | 266–268 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 128 | 269–269 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 129 | 272–272 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 20.   SELECT collation [4mfor[0m ('foo'); |
| 130 | 272–273 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 20.   SELECT collation [4mfor[0m ('foo'::text); |
| 131 | 274–274 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 20.   SELECT collation [4mfor[0m ((SELECT a FROM collate_test1 LIMIT 1)); |
| 132 | 274–275 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 20.   SELECT collation [4mfor[0m ((SELECT b FROM collate_test1 LIMIT 1)); |
| 133 | 277–280 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 134 | 281–285 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 135 | 286–287 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 136 | 288–289 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 137 | 290–291 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 138 | 292–293 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 139 | 294–295 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 140 | 296–297 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 141 | 298–299 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 142 | 300–301 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 143 | 302–303 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 144 | 305–311 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 145 | 312–313 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 146 | 315–320 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 9 | 42–42 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 10 | 43–43 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 11 | 44–44 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 12 | 45–45 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 17 | 54–54 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 20 | 61–61 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 21 | 64–64 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 22 | 65–65 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 23 | 67–67 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 24 | 69–70 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 25 | 71–71 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 30 | 87–87 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 31 | 88–88 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 32 | 90–90 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 36 | 98–99 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 37 | 102–104 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 38 | 105–105 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 39 | 106–106 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 40 | 108–108 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 41 | 109–109 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 42 | 110–110 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 43 | 112–112 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 44 | 113–113 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 45 | 114–114 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 46 | 116–116 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 47 | 117–117 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 49 | 120–120 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 50 | 121–121 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 51 | 122–122 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 52 | 123–123 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 53 | 125–125 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 54 | 126–126 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 55 | 128–128 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 56 | 129–129 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 57 | 131–132 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 58 | 132–133 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 59 | 134–134 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 60 | 135–135 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 61 | 135–137 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 62 | 138–138 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 63 | 139–139 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 64 | 140–140 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 65 | 142–142 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 66 | 142–143 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 67 | 143–144 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 68 | 144–145 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 69 | 145–146 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 70 | 146–147 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 72 | 149–152 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 73 | 152–153 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 74 | 153–154 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 75 | 154–161 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 77 | 166–167 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 78 | 168–169 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 79 | 170–170 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 81 | 176–176 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 82 | 177–177 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 84 | 185–185 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 85 | 188–190 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 86 | 191–191 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 88 | 196–196 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 89 | 197–197 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 96 | 208–210 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 116 | 249–249 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/collate.out`；SHA-256（文件内容指纹）：`4c9560d40dbaa1f6fb3227c0689103796d816a0abbf0d82ccc40309a1ecd7f37`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 4/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 4/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 3/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 3/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 3/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/4 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-collate-0026-af6ea175` | SELECT 'bbc' COLLATE "C" > 'Abc' COLLATE "C" AS "true"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-collate-0027-d8db4eff` | SELECT 'bbc' COLLATE "POSIX" < 'Abc' COLLATE "POSIX" AS "false"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-collate-0076-6c178227` | SELECT a, b, a < b as lt FROM   (VALUES ('a', 'B'), ('A', 'b' COLLATE "C")) v(a,b); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-collate-0080-62d6468d` | SELECT CAST('42' AS text COLLATE "C"); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-collate-0080-62d6468d — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT CAST('42' AS text COLLATE "C");
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('42' AS STRING COLLATE `C`)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`syntax error at or near "COLLATE"`。

错误原文：

```text
syntax error at or near "COLLATE"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing ')' at 'COLLATE'(line 1, pos 27)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=syntax error at or near "COLLATE"
source_error_code=syntax error at or near "COLLATE"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing ')' at 'COLLATE'(line 1, pos 27)\n")
doris_error_code=1105
```
