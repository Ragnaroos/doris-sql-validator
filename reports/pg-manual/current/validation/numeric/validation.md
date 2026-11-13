# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:17.168775+00:00 至 2026-11-11T09:40:17.838437+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/numeric.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**25**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/25 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/11 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**14**；不计入上述成功匹配分子。
- 需要分析的查询：**25**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**4**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 18 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 7 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 25 条只读查询、跳过 1013 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–5 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 6–6 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 7–7 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 4 | 8–8 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 5 | 9–9 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 6 | 10–10 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 7 | 11–11 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 8 | 12–12 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 9 | 13–13 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 10 | 15–15 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 12 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 25–25 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 14 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 15 | 27–27 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 28–28 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 17 | 29–29 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 30–30 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 19 | 31–31 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 32–32 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 21 | 33–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 22 | 34–34 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 23 | 35–35 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 24 | 36–36 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 25 | 37–37 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 26 | 38–38 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 27 | 39–39 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 28 | 40–40 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 29 | 41–41 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 30 | 42–42 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 31 | 43–43 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 32 | 44–44 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 33 | 45–45 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 34 | 46–46 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 35 | 47–47 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 36 | 48–48 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 37 | 49–49 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 38 | 50–50 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 39 | 51–51 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 40 | 52–52 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 41 | 53–53 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 42 | 54–54 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 43 | 55–55 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 44 | 56–56 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 45 | 57–57 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 46 | 58–58 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 47 | 59–59 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 48 | 60–60 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 49 | 61–61 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 50 | 62–62 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 51 | 63–63 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 52 | 64–64 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 53 | 65–65 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 54 | 66–66 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 55 | 67–67 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 56 | 68–68 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 57 | 69–69 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 58 | 70–70 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 59 | 71–71 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 60 | 72–72 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 61 | 73–73 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 62 | 74–74 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 63 | 75–75 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 64 | 76–76 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 65 | 77–77 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 66 | 78–78 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 67 | 79–79 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 68 | 80–80 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 69 | 81–81 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 70 | 82–82 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 71 | 83–83 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 72 | 84–84 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 73 | 85–85 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 86–86 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 75 | 87–87 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 88–88 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 77 | 89–89 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 78 | 90–90 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 79 | 91–91 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 80 | 92–92 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 81 | 93–93 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 82 | 94–94 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 83 | 95–95 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 84 | 96–96 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 85 | 97–97 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 86 | 98–98 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 87 | 99–99 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 88 | 100–100 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 89 | 101–101 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 90 | 102–102 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 91 | 103–103 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 92 | 104–104 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 93 | 105–105 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 94 | 106–106 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 95 | 107–107 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 96 | 108–108 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 97 | 109–109 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 98 | 110–110 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 99 | 111–111 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 100 | 112–112 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 101 | 113–113 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 102 | 114–114 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 103 | 115–115 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 104 | 116–116 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 105 | 117–117 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 106 | 118–118 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 107 | 119–119 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 108 | 120–120 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 109 | 121–121 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 110 | 122–122 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 111 | 123–123 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 112 | 124–124 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 113 | 125–125 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 114 | 126–126 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 115 | 127–127 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 116 | 128–128 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 117 | 129–129 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 118 | 130–130 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 119 | 131–131 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 120 | 132–132 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 121 | 133–133 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 122 | 134–134 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 123 | 135–135 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 124 | 136–136 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 125 | 137–137 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 126 | 138–138 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 127 | 139–139 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 128 | 140–140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 129 | 141–141 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 130 | 142–142 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 131 | 143–143 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 132 | 144–144 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 133 | 145–145 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 134 | 146–146 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 135 | 147–147 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 136 | 148–148 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 137 | 149–149 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 138 | 150–150 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 139 | 151–151 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 140 | 152–152 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 141 | 153–153 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 142 | 154–154 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 143 | 155–155 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 144 | 156–156 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 145 | 157–157 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 146 | 158–158 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 147 | 159–159 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 148 | 160–160 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 149 | 161–161 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 150 | 162–162 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 151 | 163–163 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 152 | 164–164 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 153 | 165–165 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 154 | 166–166 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 155 | 167–167 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 156 | 168–168 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 157 | 169–169 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 158 | 170–170 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 159 | 171–171 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 160 | 172–172 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 161 | 173–173 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 162 | 174–174 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 163 | 175–175 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 164 | 176–176 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 165 | 177–177 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 166 | 178–178 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 167 | 179–179 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 168 | 180–180 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 169 | 181–181 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 170 | 182–182 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 171 | 183–183 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 172 | 184–184 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 173 | 185–185 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 174 | 186–186 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 175 | 187–187 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 176 | 188–188 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 177 | 189–189 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 178 | 190–190 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 179 | 191–191 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 180 | 192–192 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 181 | 193–193 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 182 | 194–194 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 183 | 195–195 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 184 | 196–196 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 185 | 197–197 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 186 | 198–198 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 187 | 199–199 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 188 | 200–200 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 189 | 201–201 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 190 | 202–202 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 191 | 203–203 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 192 | 204–204 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 193 | 205–205 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 194 | 206–206 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 195 | 207–207 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 196 | 208–208 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 197 | 209–209 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 198 | 210–210 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 199 | 211–211 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 200 | 212–212 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 201 | 213–213 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 202 | 214–214 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 203 | 215–215 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 204 | 216–216 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 205 | 217–217 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 206 | 218–218 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 207 | 219–219 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 208 | 220–220 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 209 | 221–221 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 210 | 222–222 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 211 | 223–223 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 212 | 224–224 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 213 | 225–225 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 214 | 226–226 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 215 | 227–227 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 216 | 228–228 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 217 | 229–229 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 218 | 230–230 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 219 | 231–231 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 220 | 232–232 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 221 | 233–233 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 222 | 234–234 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 223 | 235–235 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 224 | 236–236 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 225 | 237–237 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 226 | 238–238 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 227 | 239–239 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 228 | 240–240 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 229 | 241–241 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 230 | 242–242 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 231 | 243–243 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 232 | 244–244 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 233 | 245–245 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 234 | 246–246 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 235 | 247–247 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 236 | 248–248 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 237 | 249–249 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 238 | 250–250 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 239 | 251–251 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 240 | 252–252 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 241 | 253–253 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 242 | 254–254 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 243 | 255–255 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 244 | 256–256 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 245 | 257–257 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 246 | 258–258 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 247 | 259–259 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 248 | 260–260 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 249 | 261–261 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 250 | 262–262 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 251 | 263–263 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 252 | 264–264 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 253 | 265–265 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 254 | 266–266 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 255 | 267–267 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 256 | 268–268 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 257 | 269–269 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 258 | 270–270 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 259 | 271–271 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 260 | 272–272 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 261 | 273–273 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 262 | 274–274 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 263 | 275–275 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 264 | 276–276 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 265 | 277–277 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 266 | 278–278 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 267 | 279–279 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 268 | 280–280 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 269 | 281–281 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 270 | 282–282 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 271 | 283–283 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 272 | 284–284 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 273 | 285–285 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 274 | 286–286 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 275 | 287–287 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 276 | 288–288 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 277 | 289–289 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 278 | 290–290 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 279 | 291–291 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 280 | 292–292 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 281 | 293–293 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 282 | 294–294 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 283 | 295–295 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 284 | 296–296 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 285 | 297–297 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 286 | 298–298 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 287 | 299–299 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 288 | 300–300 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 289 | 301–301 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 290 | 302–302 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 291 | 303–303 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 292 | 304–304 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 293 | 305–305 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 294 | 306–306 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 295 | 307–307 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 296 | 308–308 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 297 | 309–309 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 298 | 310–310 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 299 | 311–311 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 300 | 312–312 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 301 | 313–313 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 302 | 314–314 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 303 | 315–315 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 304 | 316–316 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 305 | 317–317 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 306 | 318–318 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 307 | 319–319 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 308 | 320–320 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 309 | 321–321 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 310 | 322–322 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 311 | 323–323 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 312 | 324–324 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 313 | 325–325 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 314 | 326–326 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 315 | 327–327 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 316 | 328–328 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 317 | 329–329 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 318 | 330–330 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 319 | 331–331 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 320 | 332–332 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 321 | 333–333 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 322 | 334–334 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 323 | 335–335 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 324 | 336–336 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 325 | 337–337 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 326 | 338–338 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 327 | 339–339 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 328 | 340–340 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 329 | 341–341 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 330 | 342–342 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 331 | 343–343 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 332 | 344–344 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 333 | 345–345 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 334 | 346–346 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 335 | 347–347 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 336 | 348–348 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 337 | 349–349 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 338 | 350–350 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 339 | 351–351 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 340 | 352–352 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 341 | 353–353 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 342 | 354–354 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 343 | 355–355 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 344 | 356–356 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 345 | 357–357 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 346 | 358–358 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 347 | 359–359 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 348 | 360–360 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 349 | 361–361 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 350 | 362–362 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 351 | 363–363 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 352 | 364–364 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 353 | 365–365 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 354 | 366–366 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 355 | 367–367 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 356 | 368–368 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 357 | 369–369 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 358 | 370–370 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 359 | 371–371 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 360 | 372–372 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 361 | 373–373 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 362 | 374–374 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 363 | 375–375 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 364 | 376–376 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 365 | 377–377 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 366 | 378–378 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 367 | 379–379 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 368 | 380–380 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 369 | 381–381 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 370 | 382–382 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 371 | 383–383 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 372 | 384–384 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 373 | 385–385 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 374 | 386–386 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 375 | 387–387 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 376 | 388–388 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 377 | 389–389 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 378 | 390–390 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 379 | 391–391 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 380 | 392–392 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 381 | 393–393 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 382 | 394–394 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 383 | 395–395 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 384 | 396–396 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 385 | 397–397 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 386 | 398–398 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 387 | 399–399 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 388 | 400–400 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 389 | 401–401 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 390 | 402–402 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 391 | 403–403 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 392 | 404–404 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 393 | 405–405 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 394 | 406–406 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 395 | 407–407 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 396 | 408–408 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 397 | 409–409 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 398 | 410–410 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 399 | 411–411 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 400 | 412–412 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 401 | 413–413 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 402 | 414–414 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 403 | 415–415 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 404 | 416–416 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 405 | 417–417 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 406 | 418–418 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 407 | 419–419 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 408 | 420–420 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 409 | 421–421 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 410 | 422–422 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 411 | 423–423 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 414 | 426–426 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 415 | 427–427 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 416 | 428–428 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 417 | 429–429 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 418 | 430–430 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 419 | 431–431 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 420 | 432–432 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 421 | 433–433 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 422 | 434–434 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 423 | 435–435 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 426 | 438–438 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 427 | 439–439 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 428 | 440–440 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 429 | 441–441 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 430 | 442–442 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 431 | 443–443 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 432 | 444–444 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 433 | 445–445 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 434 | 446–446 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 435 | 447–447 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 438 | 450–450 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 439 | 451–451 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 440 | 452–452 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 441 | 453–453 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 442 | 454–454 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 443 | 455–455 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 444 | 456–456 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 445 | 457–457 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 446 | 458–458 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 447 | 459–459 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 450 | 462–462 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 451 | 463–463 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 452 | 464–464 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 453 | 465–465 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 454 | 466–466 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 455 | 467–467 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 456 | 468–468 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 457 | 469–469 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 458 | 470–470 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 459 | 471–471 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 462 | 474–474 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 463 | 475–475 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 464 | 476–476 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 465 | 477–477 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 466 | 478–478 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 467 | 479–479 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 468 | 480–480 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 469 | 481–481 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 470 | 482–482 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 471 | 483–483 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 473 | 486–490 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 474 | 491–491 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 475 | 492–492 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 476 | 493–493 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 477 | 494–494 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 478 | 495–495 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 479 | 496–496 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 480 | 497–497 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 489 | 508–515 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 490 | 516–517 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 492 | 523–523 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 493 | 524–525 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 495 | 531–534 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 496 | 535–536 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 498 | 542–542 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 499 | 543–544 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 501 | 550–553 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 502 | 554–555 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 504 | 561–561 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 505 | 562–563 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 507 | 569–572 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 508 | 573–575 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 510 | 581–581 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 511 | 582–584 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 513 | 590–593 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 514 | 594–595 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 516 | 601–604 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 517 | 605–607 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 519 | 613–616 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 520 | 617–619 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 522 | 625–628 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 523 | 629–631 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 584 | 762–763 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 585 | 764–764 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 586 | 765–765 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 587 | 766–766 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 588 | 766–767 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 589 | 768–768 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 590 | 769–769 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 591 | 769–770 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 592 | 771–771 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 593 | 772–772 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 594 | 773–773 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 595 | 773–774 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 597 | 776–776 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 632 | 816–817 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 633 | 818–818 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 634 | 819–819 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 635 | 820–820 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 636 | 821–821 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 637 | 822–822 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 638 | 823–823 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 639 | 824–824 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 641 | 826–826 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 672 | 880–881 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 673 | 883–883 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 674 | 884–905 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 682 | 932–932 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 746 | 1067–1069 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 793 | 1126–1126 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 794 | 1128–1132 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 795 | 1134–1135 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 796 | 1136–1136 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 797 | 1137–1137 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 798 | 1138–1138 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 799 | 1139–1139 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 800 | 1140–1140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 801 | 1141–1141 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 802 | 1142–1142 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 803 | 1143–1143 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 804 | 1144–1144 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 805 | 1145–1145 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 806 | 1146–1146 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 807 | 1147–1147 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 808 | 1148–1148 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 809 | 1149–1149 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 810 | 1150–1150 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 811 | 1151–1151 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 812 | 1152–1152 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 813 | 1153–1153 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 814 | 1154–1154 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 815 | 1155–1155 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 816 | 1156–1156 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 817 | 1157–1157 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 818 | 1158–1158 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 819 | 1160–1161 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 820 | 1162–1162 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 821 | 1163–1163 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 822 | 1164–1164 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 823 | 1165–1165 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 824 | 1166–1166 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 825 | 1167–1167 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 826 | 1168–1168 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 827 | 1169–1169 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 828 | 1170–1170 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 829 | 1171–1171 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 830 | 1172–1172 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 831 | 1173–1173 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 832 | 1174–1174 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 833 | 1175–1175 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 834 | 1176–1176 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 835 | 1177–1177 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 836 | 1178–1178 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 837 | 1179–1179 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 838 | 1180–1180 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 839 | 1181–1181 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 840 | 1182–1182 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 841 | 1183–1183 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 842 | 1184–1184 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 843 | 1185–1185 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 844 | 1186–1186 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 845 | 1187–1187 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 855 | 1201–1211 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 18.   CREATE TABLE num_typemod_test (   millions [4mnumeric[0m(3, -6),   thousands numeric(3, -3),   units numeric(3, 0),   thousandths numeric(3, 3),   millionth |
| 856 | 1212–1215 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 857 | 1216–1216 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 858 | 1217–1217 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 859 | 1218–1218 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 860 | 1219–1219 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 861 | 1220–1220 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 862 | 1221–1221 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 863 | 1222–1222 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 864 | 1223–1223 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 866 | 1227–1228 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 867 | 1229–1229 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 868 | 1230–1230 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 869 | 1231–1231 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 870 | 1232–1232 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 871 | 1233–1233 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1026 | 1501–1504 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1027 | 1505–1505 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1028 | 1506–1506 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1029 | 1507–1507 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1030 | 1508–1508 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1031 | 1509–1509 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1034 | 1516–1516 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 1035 | 1517–1517 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1036 | 1518–1518 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1039 | 1522–1523 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 1040 | 1524–1524 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1043 | 1529–1529 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 1044 | 1530–1530 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1045 | 1531–1531 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1048 | 1535–1535 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 491 | 518–521 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 494 | 526–529 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 497 | 537–540 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 500 | 545–548 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 503 | 556–559 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 506 | 564–567 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 509 | 576–579 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 512 | 585–588 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 515 | 596–599 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 518 | 608–611 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 521 | 620–623 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 524 | 632–635 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 550 | 716–716 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 551 | 717–717 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 552 | 718–718 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 553 | 719–719 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 554 | 720–720 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 555 | 721–721 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 556 | 722–722 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 557 | 723–723 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 558 | 724–724 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 559 | 726–730 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 560 | 732–732 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 561 | 733–733 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 562 | 734–734 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 563 | 735–735 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 564 | 736–736 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 565 | 737–737 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 566 | 738–738 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 567 | 739–739 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 568 | 740–740 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 569 | 741–741 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 570 | 742–742 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 571 | 743–743 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 572 | 744–744 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 573 | 745–745 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 574 | 746–746 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 575 | 747–747 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 576 | 748–748 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 577 | 749–749 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 578 | 750–750 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 579 | 752–756 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 580 | 757–757 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 581 | 758–758 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 582 | 759–759 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 583 | 760–760 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 596 | 774–775 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 598 | 778–779 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 599 | 779–780 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 600 | 780–781 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 601 | 781–782 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 602 | 782–783 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 603 | 783–784 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 604 | 784–785 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 605 | 785–786 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 606 | 786–787 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 607 | 787–788 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 608 | 788–789 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 609 | 789–790 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 610 | 790–793 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 611 | 794–794 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 612 | 795–795 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 613 | 796–796 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 614 | 797–797 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 615 | 798–798 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 616 | 799–799 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 617 | 800–800 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 618 | 801–801 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 619 | 802–802 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 620 | 803–803 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 621 | 804–804 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 622 | 805–805 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 623 | 806–806 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 624 | 807–807 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 625 | 808–808 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 626 | 809–809 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 627 | 810–810 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 628 | 811–811 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 629 | 812–812 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 630 | 813–813 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 631 | 814–814 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 640 | 825–825 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 642 | 828–836 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 643 | 838–839 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 644 | 840–840 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 645 | 841–841 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 646 | 841–842 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 647 | 842–843 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 648 | 843–844 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 649 | 844–847 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 650 | 848–848 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 651 | 849–849 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 652 | 850–850 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 653 | 852–853 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 654 | 854–854 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 655 | 854–855 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 656 | 855–856 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 657 | 856–859 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 658 | 860–860 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 659 | 861–861 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 660 | 863–867 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 661 | 868–868 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 662 | 869–869 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 663 | 870–870 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 664 | 871–871 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 665 | 872–872 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 666 | 873–873 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 667 | 874–874 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 668 | 875–875 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 669 | 876–876 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 670 | 877–877 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 671 | 878–878 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 675 | 907–919 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 676 | 921–923 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 677 | 923–924 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 678 | 924–926 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 679 | 927–927 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 680 | 927–928 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 681 | 928–930 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 683 | 934–937 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 684 | 938–940 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 685 | 941–942 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 686 | 943–943 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 687 | 944–944 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 688 | 945–945 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 689 | 947–964 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 690 | 965–966 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 691 | 967–967 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 692 | 969–973 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 693 | 975–976 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 694 | 978–979 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 695 | 981–982 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 696 | 984–984 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 697 | 985–985 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 698 | 986–986 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 699 | 987–987 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 700 | 988–988 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 701 | 989–989 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 702 | 990–990 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 703 | 991–991 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 704 | 992–992 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 705 | 993–993 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 706 | 994–994 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 707 | 995–995 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 708 | 996–996 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 709 | 997–997 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 710 | 998–998 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 711 | 999–999 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 712 | 1000–1000 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 713 | 1001–1001 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 714 | 1002–1002 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 715 | 1003–1003 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 716 | 1005–1011 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 717 | 1013–1018 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 718 | 1020–1026 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 719 | 1028–1034 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 720 | 1036–1036 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 721 | 1037–1037 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 722 | 1038–1038 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 723 | 1039–1039 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 724 | 1040–1040 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 725 | 1042–1042 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 726 | 1043–1043 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 727 | 1044–1044 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 728 | 1045–1045 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 729 | 1046–1046 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 730 | 1047–1047 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 731 | 1048–1048 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 732 | 1049–1049 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 733 | 1051–1051 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 734 | 1052–1052 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 735 | 1053–1053 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 736 | 1055–1056 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 737 | 1057–1057 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 738 | 1058–1058 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 739 | 1059–1059 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 740 | 1060–1060 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 741 | 1061–1061 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 742 | 1062–1062 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 743 | 1063–1063 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 744 | 1064–1064 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 745 | 1065–1065 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 747 | 1070–1070 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 748 | 1071–1071 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 749 | 1072–1072 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 750 | 1073–1073 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 751 | 1074–1074 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 752 | 1075–1075 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 753 | 1076–1076 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 754 | 1077–1077 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 755 | 1078–1078 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 756 | 1079–1079 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 757 | 1080–1080 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 758 | 1081–1081 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 759 | 1082–1082 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 760 | 1083–1083 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 761 | 1084–1084 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 762 | 1085–1085 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 763 | 1086–1086 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 764 | 1087–1087 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 765 | 1088–1088 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 766 | 1089–1089 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 767 | 1090–1090 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 768 | 1091–1091 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 769 | 1092–1092 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 770 | 1094–1099 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 771 | 1101–1102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 772 | 1103–1103 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 773 | 1104–1104 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 774 | 1105–1105 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 775 | 1106–1106 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 776 | 1107–1108 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 777 | 1109–1109 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 778 | 1110–1110 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 779 | 1111–1111 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 780 | 1112–1112 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 781 | 1113–1113 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 782 | 1114–1114 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 783 | 1115–1115 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 784 | 1116–1116 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 785 | 1117–1117 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 786 | 1118–1118 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 787 | 1119–1119 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 788 | 1120–1120 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 789 | 1121–1121 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 790 | 1122–1122 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 791 | 1123–1123 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 792 | 1124–1124 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 846 | 1189–1189 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 847 | 1191–1192 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 848 | 1193–1193 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 849 | 1194–1194 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 850 | 1195–1195 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 851 | 1196–1196 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 852 | 1197–1197 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 853 | 1198–1198 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 854 | 1199–1199 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 865 | 1225–1225 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 872 | 1235–1239 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 873 | 1241–1241 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 874 | 1243–1243 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 875 | 1245–1245 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 876 | 1247–1247 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 877 | 1249–1253 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 878 | 1254–1254 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 879 | 1255–1255 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 880 | 1256–1256 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 881 | 1257–1257 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 882 | 1258–1258 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 883 | 1259–1259 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 884 | 1260–1260 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 885 | 1261–1261 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 886 | 1262–1262 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 887 | 1263–1263 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 888 | 1264–1264 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 889 | 1265–1265 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 890 | 1266–1266 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 891 | 1267–1267 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 892 | 1268–1268 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 893 | 1270–1274 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 894 | 1275–1275 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 895 | 1276–1276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 896 | 1277–1277 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 897 | 1278–1278 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 898 | 1279–1279 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 899 | 1280–1280 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 900 | 1281–1281 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 901 | 1283–1287 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 902 | 1288–1288 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 903 | 1289–1289 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 904 | 1290–1290 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 905 | 1292–1293 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 906 | 1294–1294 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 907 | 1295–1295 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 908 | 1296–1296 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 909 | 1297–1297 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 910 | 1298–1298 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 911 | 1299–1299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 912 | 1301–1302 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 913 | 1303–1303 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 914 | 1304–1304 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 915 | 1306–1307 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 916 | 1308–1308 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 917 | 1309–1309 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 918 | 1310–1310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 919 | 1311–1311 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 920 | 1313–1315 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 921 | 1317–1322 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 922 | 1323–1323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 923 | 1324–1324 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 924 | 1325–1325 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 925 | 1327–1328 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 926 | 1329–1329 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 927 | 1330–1330 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 928 | 1331–1331 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 929 | 1332–1332 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 930 | 1334–1335 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 931 | 1336–1336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 932 | 1338–1339 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 933 | 1340–1340 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 934 | 1341–1341 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 935 | 1342–1342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 936 | 1344–1345 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 937 | 1347–1352 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 938 | 1353–1353 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 939 | 1354–1354 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 940 | 1355–1355 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 941 | 1356–1356 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 942 | 1357–1357 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 943 | 1358–1358 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 944 | 1359–1359 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 945 | 1361–1362 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 946 | 1363–1363 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 947 | 1364–1364 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 948 | 1365–1365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 949 | 1367–1368 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 950 | 1370–1373 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 951 | 1374–1374 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 952 | 1375–1375 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 953 | 1376–1377 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 954 | 1378–1378 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 955 | 1379–1379 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 956 | 1380–1380 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 957 | 1381–1381 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 958 | 1382–1382 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 959 | 1383–1383 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 960 | 1384–1388 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 961 | 1389–1390 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 962 | 1391–1391 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 963 | 1392–1392 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 964 | 1394–1399 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 965 | 1400–1400 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 966 | 1402–1403 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 967 | 1404–1404 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 968 | 1405–1405 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 969 | 1406–1406 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 970 | 1407–1407 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 971 | 1408–1408 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 972 | 1409–1409 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 973 | 1410–1410 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 974 | 1412–1417 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 975 | 1418–1418 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 976 | 1420–1421 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 977 | 1422–1422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 978 | 1423–1423 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 979 | 1424–1424 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 980 | 1425–1425 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 981 | 1426–1426 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 982 | 1428–1433 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 983 | 1434–1434 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 984 | 1435–1435 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 985 | 1436–1436 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 986 | 1437–1437 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 987 | 1438–1438 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 988 | 1440–1441 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 989 | 1442–1442 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 990 | 1443–1443 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 991 | 1444–1444 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 992 | 1446–1450 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 993 | 1451–1451 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 994 | 1452–1452 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 995 | 1453–1453 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 996 | 1454–1454 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 997 | 1455–1455 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 998 | 1456–1456 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 999 | 1457–1457 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1000 | 1458–1458 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1001 | 1459–1459 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1002 | 1461–1465 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1003 | 1465–1466 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1004 | 1466–1467 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1005 | 1467–1468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1006 | 1468–1469 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1007 | 1469–1470 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1008 | 1470–1471 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1009 | 1471–1472 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1010 | 1472–1473 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1011 | 1473–1474 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1012 | 1474–1475 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1013 | 1475–1476 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1014 | 1476–1482 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1015 | 1483–1483 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1016 | 1484–1484 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1017 | 1485–1485 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1018 | 1486–1486 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1019 | 1487–1487 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1020 | 1488–1488 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1021 | 1489–1489 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1022 | 1490–1490 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1023 | 1491–1491 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1024 | 1493–1498 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1025 | 1499–1499 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1032 | 1511–1512 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1037 | 1519–1519 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1041 | 1525–1525 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1046 | 1532–1532 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1049 | 1537–1550 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1050 | 1552–1566 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1051 | 1568–1568 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1052 | 1568–1573 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1053 | 1574–1574 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1054 | 1575–1575 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1055 | 1576–1576 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1056 | 1577–1577 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1057 | 1579–1582 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1058 | 1583–1583 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1059 | 1584–1584 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1060 | 1585–1585 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1061 | 1586–1586 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1062 | 1587–1587 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/numeric.out`；SHA-256（文件内容指纹）：`7fdd536a0413dc8f91f1abf121936d7b73f0db70f417cc0a05f372996ba64acb`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 25/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 25/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 11/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 11/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 11/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-numeric-0525-c4b5f8ba` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan')) SELECT x1, x2,   x1 + x2 AS sum,   x1 - x2 AS diff,   x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0526-8a2839bf` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan')) SELECT x1, x2,   x1 / x2 AS quot,   x1 % x2 AS mod,   div(x1, x2) AS div FROM v AS v1(x1), v AS v2(x2) WHERE x2 != 0; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0527-853087af` | SELECT 'inf'::numeric / '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0528-5c708c93` | SELECT '-inf'::numeric / '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0529-d53a9922` | SELECT 'nan'::numeric / '0'; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0530-92fc4082` | SELECT '0'::numeric / '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0531-005b6940` | SELECT 'inf'::numeric % '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0532-970512c5` | SELECT '-inf'::numeric % '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0533-2a259c60` | SELECT 'nan'::numeric % '0'; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0534-066224c8` | SELECT '0'::numeric % '0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0535-fc163301` | SELECT div('inf'::numeric, '0'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0536-4370cc9d` | SELECT div('-inf'::numeric, '0'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0537-76b7cab4` | SELECT div('nan'::numeric, '0'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0538-739933ff` | SELECT div('0'::numeric, '0'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0539-e8cd2f84` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan')) SELECT x, -x as minusx, abs(x), floor(x), ceil(x), sign(x), numeric_inc(x) as inc FROM v; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0540-4f39a445` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan')) SELECT x, round(x), round(x,1) as round1, trunc(x), trunc(x,1) as trunc1 FROM v; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0541-215fd527` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('1e340'),('-1e340'),          ('inf'),('-inf'),('nan'),          ('inf'),('-inf'),('nan')) SELECT substring(x::text, 1, 32) FROM v ORDER BY x; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0542-ec3f1242` | WITH v(x) AS   (VALUES('0'::numeric),('1'),('4.2'),('inf'),('nan')) SELECT x, sqrt(x) FROM v; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0543-0a26f3a1` | SELECT sqrt('-1'::numeric); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0544-97db210d` | SELECT sqrt('-inf'::numeric); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0545-f34f959e` | WITH v(x) AS   (VALUES('1'::numeric),('4.2'),('inf'),('nan')) SELECT x,   log(x),   log10(x),   ln(x) FROM v; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numeric-0546-e870226f` | SELECT ln('0'::numeric); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0547-c845e747` | SELECT ln('-1'::numeric); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0548-84f27093` | SELECT ln('-inf'::numeric); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numeric-0549-3d2249da` | WITH v(x) AS   (VALUES('2'::numeric),('4.2'),('inf'),('nan')) SELECT x1, x2,   log(x1, x2) FROM v AS v1(x1), v AS v2(x2); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-numeric-0525-c4b5f8ba — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan'))
SELECT x1, x2,
  x1 + x2 AS sum,
  x1 - x2 AS diff,
  x1 * x2 AS prod
FROM v AS v1(x1), v AS v2(x2);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：49；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, sum: unknown / 原生类型未知, diff: unknown / 原生类型未知, prod: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "1",
    "1",
    "-1",
    "0"
  ],
  [
    "0",
    "-1",
    "-1",
    "1",
    "0"
  ],
  [
    "0",
    "4.2",
    "4.2",
    "-4.2",
    "0.0"
  ],
  [
    "0",
    "Infinity",
    "Infinity",
    "-Infinity",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 22.0 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 279)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 279)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
doris_error_code=1105
```

### pg-numeric-0526-8a2839bf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan'))
SELECT x1, x2,
  x1 / x2 AS quot,
  x1 % x2 AS mod,
  div(x1, x2) AS div
FROM v AS v1(x1), v AS v2(x2) WHERE x2 != 0;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：42；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, quot: unknown / 原生类型未知, mod: unknown / 原生类型未知, div: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "1",
    "0.00000000000000000000",
    "0",
    "0"
  ],
  [
    "1",
    "1",
    "1.00000000000000000000",
    "0",
    "1"
  ],
  [
    "-1",
    "1",
    "-1.00000000000000000000",
    "0",
    "-1"
  ],
  [
    "4.2",
    "1",
    "4.2000000000000000",
    "0.2",
    "4"
  ],
  [
    "Infinity",
    "1",
    "Infinity",
    "NaN",
    "Infinity"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.1 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 297)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 297)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
doris_error_code=1105
```

### pg-numeric-0527-853087af — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'inf'::numeric / '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('inf' AS DECIMAL) / '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 20.2 ms。
- 返回行数：1；字段：CAST('inf' AS DECIMAL) / '0': float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0528-5c708c93 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-inf'::numeric / '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('-inf' AS DECIMAL) / '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.5 ms。
- 返回行数：1；字段：CAST('-inf' AS DECIMAL) / '0': float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0529-d53a9922 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::numeric / '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('nan' AS DECIMAL) / '0'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CAST('nan' AS DECIMAL) / '0': float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0530-92fc4082 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '0'::numeric / '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('0' AS DECIMAL) / '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.0 ms。
- 返回行数：1；字段：CAST('0' AS DECIMAL) / '0': float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0531-005b6940 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'inf'::numeric % '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('inf' AS DECIMAL) % '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.3 ms。
- 返回行数：1；字段：CAST('inf' AS DECIMAL) % '0': decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0532-970512c5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-inf'::numeric % '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('-inf' AS DECIMAL) % '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.8 ms。
- 返回行数：1；字段：CAST('-inf' AS DECIMAL) % '0': decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0533-2a259c60 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::numeric % '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('nan' AS DECIMAL) % '0'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 62.3 ms。
- 返回行数：1；字段：CAST('nan' AS DECIMAL) % '0': decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0534-066224c8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '0'::numeric % '0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('0' AS DECIMAL) % '0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 42.6 ms。
- 返回行数：1；字段：CAST('0' AS DECIMAL) % '0': decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0535-fc163301 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT div('inf'::numeric, '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('inf' AS DECIMAL) DIV '0' AS DECIMAL)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.0 ms。
- 返回行数：1；字段：CAST(CAST('inf' AS DECIMAL) DIV '0' AS DECIMAL): decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0536-4370cc9d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT div('-inf'::numeric, '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-inf' AS DECIMAL) DIV '0' AS DECIMAL)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.6 ms。
- 返回行数：1；字段：CAST(CAST('-inf' AS DECIMAL) DIV '0' AS DECIMAL): decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0537-76b7cab4 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT div('nan'::numeric, '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('nan' AS DECIMAL) DIV '0' AS DECIMAL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：div: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.2 ms。
- 返回行数：1；字段：CAST(CAST('nan' AS DECIMAL) DIV '0' AS DECIMAL): decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0538-739933ff — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT div('0'::numeric, '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('0' AS DECIMAL) DIV '0' AS DECIMAL)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`division by zero`。

错误原文：

```text
division by zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 100.8 ms。
- 返回行数：1；字段：CAST(CAST('0' AS DECIMAL) DIV '0' AS DECIMAL): decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=division by zero
source_error_code=division by zero
```

### pg-numeric-0539-e8cd2f84 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan'))
SELECT x, -x as minusx, abs(x), floor(x), ceil(x), sign(x), numeric_inc(x) as inc
FROM v;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x, -x AS minusx, ABS(x), FLOOR(x), CEIL(x), SIGN(x), NUMERIC_INC(x) AS inc FROM v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：8；字段：x: unknown / 原生类型未知, minusx: unknown / 原生类型未知, abs: unknown / 原生类型未知, floor: unknown / 原生类型未知, ceil: unknown / 原生类型未知, sign: unknown / 原生类型未知, inc: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0",
    "0",
    "0",
    "0",
    "1"
  ],
  [
    "1",
    "-1",
    "1",
    "1",
    "1",
    "1",
    "2"
  ],
  [
    "-1",
    "1",
    "1",
    "-1",
    "-1",
    "-1",
    "0"
  ],
  [
    "4.2",
    "-4.2",
    "4.2",
    "4",
    "5",
    "1",
    "5.2"
  ],
  [
    "-7.777",
    "7.777",
    "7.777",
    "-8",
    "-7",
    "-1",
    "-6.777"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 18.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'NUMERIC_INC'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'NUMERIC_INC'")
doris_error_code=1105
```

### pg-numeric-0540-4f39a445 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan'))
SELECT x, round(x), round(x,1) as round1, trunc(x), trunc(x,1) as trunc1
FROM v;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x, ROUND(x), ROUND(x, 1) AS round1, TRUNCATE(x, 0), TRUNCATE(x, 1) AS trunc1 FROM v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：8；字段：x: unknown / 原生类型未知, round: unknown / 原生类型未知, round1: unknown / 原生类型未知, trunc: unknown / 原生类型未知, trunc1: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0.0",
    "0",
    "0.0"
  ],
  [
    "1",
    "1",
    "1.0",
    "1",
    "1.0"
  ],
  [
    "-1",
    "-1",
    "-1.0",
    "-1",
    "-1.0"
  ],
  [
    "4.2",
    "4",
    "4.2",
    "4",
    "4.2"
  ],
  [
    "-7.777",
    "-8",
    "-7.8",
    "-7",
    "-7.7"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 28.9 ms。
- 返回行数：8；字段：x: string / STRING, ROUND(x): decimal / DECIMAL, round1: decimal / DECIMAL, TRUNCATE(x, 0): decimal / DECIMAL, trunc1: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0E-9",
    {
      "$decimal": "0"
    },
    {
      "$decimal": "0.0"
    },
    {
      "$decimal": "0"
    },
    {
      "$decimal": "0.0"
    }
  ],
  [
    "1",
    {
      "$decimal": "1"
    },
    {
      "$decimal": "1.0"
    },
    {
      "$decimal": "1"
    },
    {
      "$decimal": "1.0"
    }
  ],
  [
    "-1",
    {
      "$decimal": "-1"
    },
    {
      "$decimal": "-1.0"
    },
    {
      "$decimal": "-1"
    },
    {
      "$decimal": "-1.0"
    }
  ],
  [
    "4.2",
    {
      "$decimal": "4"
    },
    {
      "$decimal": "4.2"
    },
    {
      "$decimal": "4"
    },
    {
      "$decimal": "4.2"
    }
  ],
  [
    "-7.777",
    {
      "$decimal": "-8"
    },
    {
      "$decimal": "-7.8"
    },
    {
      "$decimal": "-7"
    },
    {
      "$decimal": "-7.7"
    }
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0541-215fd527 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('1e340'),('-1e340'),
         ('inf'),('-inf'),('nan'),
         ('inf'),('-inf'),('nan'))
SELECT substring(x::text, 1, 32)
FROM v ORDER BY x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT '1e340' UNION ALL SELECT '-1e340' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT SUBSTRING(CAST(x AS STRING), 1, 32) FROM v ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：13；字段：substring: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-Infinity"
  ],
  [
    "-Infinity"
  ],
  [
    "-1000000000000000000000000000000"
  ],
  [
    "-7.777"
  ],
  [
    "-1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 22.1 ms。
- 返回行数：13；字段：SUBSTRING(CAST(x AS STRING), 1, 32): string / STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-1"
  ],
  [
    "-1e340"
  ],
  [
    "-7.777"
  ],
  [
    "-inf"
  ],
  [
    "-inf"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0542-ec3f1242 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('4.2'),('inf'),('nan'))
SELECT x, sqrt(x)
FROM v;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x, SQRT(x) FROM v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x: unknown / 原生类型未知, sqrt: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0.000000000000000"
  ],
  [
    "1",
    "1.000000000000000"
  ],
  [
    "4.2",
    "2.049390153191920"
  ],
  [
    "Infinity",
    "Infinity"
  ],
  [
    "NaN",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 31.4 ms。
- 返回行数：5；字段：x: string / STRING, SQRT(x): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0E-9",
    0.0
  ],
  [
    "1",
    1.0
  ],
  [
    "4.2",
    2.04939015319192
  ],
  [
    "inf",
    {
      "$float": "infinity"
    }
  ],
  [
    "nan",
    {
      "$float": "nan"
    }
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0543-0a26f3a1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sqrt('-1'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SQRT(CAST('-1' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot take square root of a negative number`。

错误原文：

```text
cannot take square root of a negative number
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：SQRT(CAST('-1' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=cannot take square root of a negative number
source_error_code=cannot take square root of a negative number
```

### pg-numeric-0544-97db210d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sqrt('-inf'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SQRT(CAST('-inf' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot take square root of a negative number`。

错误原文：

```text
cannot take square root of a negative number
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.2 ms。
- 返回行数：1；字段：SQRT(CAST('-inf' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=cannot take square root of a negative number
source_error_code=cannot take square root of a negative number
```

### pg-numeric-0545-f34f959e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('1'::numeric),('4.2'),('inf'),('nan'))
SELECT x,
  log(x),
  log10(x),
  ln(x)
FROM v;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('1' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x, LOG(x), LOG(10, x), LN(x) FROM v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：x: unknown / 原生类型未知, log: unknown / 原生类型未知, log10: unknown / 原生类型未知, ln: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "0.0000000000000000",
    "0.0000000000000000",
    "0.0000000000000000"
  ],
  [
    "4.2",
    "0.6232492903979005",
    "0.6232492903979005",
    "1.4350845252893226"
  ],
  [
    "Infinity",
    "Infinity",
    "Infinity",
    "Infinity"
  ],
  [
    "NaN",
    "NaN",
    "NaN",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.9 ms。
- 返回行数：4；字段：x: string / STRING, LOG(x): float / DOUBLE, LOG(10, x): float / DOUBLE, LN(x): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.000000000",
    0.0,
    0.0,
    0.0
  ],
  [
    "4.2",
    1.435084525289323,
    0.6232492903979004,
    1.435084525289323
  ],
  [
    "inf",
    {
      "$float": "infinity"
    },
    {
      "$float": "infinity"
    },
    {
      "$float": "infinity"
    }
  ],
  [
    "nan",
    {
      "$float": "nan"
    },
    {
      "$float": "nan"
    },
    {
      "$float": "nan"
    }
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-numeric-0546-e870226f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ln('0'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LN(CAST('0' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot take logarithm of zero`。

错误原文：

```text
cannot take logarithm of zero
```

#### Doris 实际结果

- 执行状态：成功；耗时 20.5 ms。
- 返回行数：1；字段：LN(CAST('0' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=cannot take logarithm of zero
source_error_code=cannot take logarithm of zero
```

### pg-numeric-0547-c845e747 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ln('-1'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LN(CAST('-1' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot take logarithm of a negative number`。

错误原文：

```text
cannot take logarithm of a negative number
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.3 ms。
- 返回行数：1；字段：LN(CAST('-1' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=cannot take logarithm of a negative number
source_error_code=cannot take logarithm of a negative number
```

### pg-numeric-0548-84f27093 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ln('-inf'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LN(CAST('-inf' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot take logarithm of a negative number`。

错误原文：

```text
cannot take logarithm of a negative number
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.8 ms。
- 返回行数：1；字段：LN(CAST('-inf' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=EXECUTION_ERROR
source_error_message=cannot take logarithm of a negative number
source_error_code=cannot take logarithm of a negative number
```

### pg-numeric-0549-3d2249da — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH v(x) AS
  (VALUES('2'::numeric),('4.2'),('inf'),('nan'))
SELECT x1, x2,
  log(x1, x2)
FROM v AS v1(x1), v AS v2(x2);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：16；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, log: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2",
    "2",
    "1.0000000000000000"
  ],
  [
    "2",
    "4.2",
    "2.0703893278913979"
  ],
  [
    "2",
    "Infinity",
    "Infinity"
  ],
  [
    "2",
    "NaN",
    "NaN"
  ],
  [
    "4.2",
    "2",
    "0.4830009440873890"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.8 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 173)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 173)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
doris_error_code=1105
```
