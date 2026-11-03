---
name: iso9001-2026-upgrade
description: 针对ISO9001:2015体系组织的2026版升版差距分析与辅导；先收集运行现状与体系文件，再输出运行改进、文件变更与执行计划的网页报告；当用户需要ISO9001升版咨询、新版标准符合性评估或转版策划时使用
---

# ISO 9001:2026 质量管理体系升版辅导

## 任务目标
- 本 Skill 用于:辅导已建立 ISO 9001:2015 质量管理体系的组织开展 2026 版升版（转版）策划。
- 能力包含:新版标准变更点解读、组织运行现状与体系文件的差距分析、运行改进建议、体系文件变更建议、升版执行计划，并以美观的网页报告形式输出。
- 触发条件:用户提出"ISO 9001 升版/转版/换版咨询""评估新版标准符合性""2026 版升级辅导"等需求，或用户提供其公司现有管理体系运行情况与文件并要求据此给出升版建议。

## 前置准备
- 标准全文:本 Skill 收录两份标准原文—— [references/gbt-19001-2016.md](references/gbt-19001-2016.md)（GB/T 19001-2016，等同 ISO 9001:2015）与 [references/iso-9001-2026-zh.md](references/iso-9001-2026-zh.md)（ISO 9001:2026 中文版）。标准全文体量大，需通过 [references/standards-index.md](references/standards-index.md) 索引导航，按 `read_file(offset, limit)` 分段定位到具体条款，勿整份加载。
- 变更点知识库:核心知识库位于 [references/standard-changes.md](references/standard-changes.md)，列出了 ISO 9001:2015 与 2026 的逐条款变更点及蕴含的体系要求，辅导解读以此为依据。需核对标准原文精确措辞时，用 [references/standards-index.md](references/standards-index.md) 定位到全文条款。
- 信息收集方法:见 [references/gap-analysis-guide.md](references/gap-analysis-guide.md)，定义了强制的交互流程、需收集的信息清单、提问话术与差距分析方法论。
- 生成网页报告所需模板为 [assets/report_template.html](assets/report_template.html)，由脚本读取填充。

## 操作步骤
升版辅导需严格遵循"先收集、再分析、后建议"的顺序，禁止在未了解组织运行情况时仅凭通用知识给出升版建议。

- 标准流程:
  1. 开场声明 — 向用户说明将进行 ISO 9001:2026 升版差距辅导，建议需基于其体系实际运行现状给出，因此会先收集信息。
  2. 收集组织环境信息 — 询问行业、规模、产品/服务、体系范围、认证状态、组织架构、战略方向与是否涉及出口/低碳要求。参考 [references/gap-analysis-guide.md](references/gap-analysis-guide.md) 的"第1类"清单。
  3. 收集体系运行现状 — 按变更点逐项确认"实际如何运行"（重点：质量文化/道德、气候变化评估、风险与机遇拆分、变更管理、数字化记录、供应链韧性、管理评审输入）。参考"第2类"清单。
  4. 收集体系文件 — 请用户列出或上传质量手册、程序文件、记录清单及内审/管理评审报告。参考"第3类"清单。
  5. 差距分析 — 对照 [references/standard-changes.md](references/standard-changes.md) 的变更点逐项判定"基本符合/部分符合/存在差距"，形成每个变更点的现状摘录、差距描述、运行改进建议与文件变更建议。解读时如需核对标准原文精确措辞，用 [references/standards-index.md](references/standards-index.md) 定位到 [references/gbt-19001-2016.md](references/gbt-19001-2016.md) 或 [references/iso-9001-2026-zh.md](references/iso-9001-2026-zh.md) 中对应条款的行号后分段读取。方法详见 [references/gap-analysis-guide.md](references/gap-analysis-guide.md) 的"差距分析方法论"。
  6. 生成网页报告 — 将差距分析结果整理为 JSON，调用脚本生成 HTML 网页报告:
     - 脚本调用示例:`python scripts/generate_report.py --input analysis.json --output report.html`
     - 脚本输出 JSON 格式结果（状态、路径、统计），供确认生成成功。
  7. 交付要点 — 逐条呈现运行改进、文件变更与执行计划，并附变更点解读。注意：建议须针对该组织现状，若某项信息不足应在报告中标注"需补充运行现状后确定"，不得泛泛建议。

- 可选分支:
  - 当用户仅要求变更点解读（不涉及本公司转版）:执行步骤 2-6 的"变更点解读"部分，直接依据 [references/standard-changes.md](references/standard-changes.md) 讲解差异与要求，无需收集公司信息、不生成报告。
  - 当用户已上传体系文件:在步骤 4 通读文件提取现状，并就文件中未体现的"实际执行情况"再向用户澄清后进入步骤 5，识别"文件符合但运行未落地"的差距。

## 使用示例
- 示例1（完整转版辅导，全新客户）:
  - 场景/输入:某制造企业提出"帮我们做 ISO 9001:2026 升版"，提供了公司简述与质量手册。
  - 预期产出:一份包含变更点解读、差距总览、运行改进建议、文件变更建议与分阶段执行计划的 HTML 网页报告。
  - 关键要点:必须按流程先收集组织环境、运行现状与文件；对质量文化(5.1)、风险/机遇拆分(6.1)、数字化记录(7.5)、供应链韧性(8.4)、气候变化(4.1)等变更点逐项结合其现状给出针对性建议；执行计划给出 2029-09-15 前的阶段安排。
- 示例2（仅解读变更点）:
  - 场景/输入:用户未提供本公司信息，只问"ISO 9001 2026 版和 2015 版有什么区别"。
  - 预期产出:关于变更点及其体系要求的解读说明，无需生成网页报告。
  - 关键要点:直接使用 [references/standard-changes.md](references/standard-changes.md) 作答；不编造公司现状。
- 示例3（评估现有体系符合性并转版策划）:
  - 场景/输入:用户提供内审报告、管理评审报告与程序文件清单，希望评估转版差距。
  - 预期产出:基于文件与陈述的差距判定（基本符合/部分符合/存在差距），并给出针对性升版计划。
  - 关键要点:交叉分析变更点间联动（如质量文化影响培训与方针、气候风险影响风险登记与管理评审）；对文件与运行不一致处重点提示。

## 资源索引
- 脚本:见 [scripts/generate_report.py](scripts/generate_report.py)(用途与参数:读取"analysis.json"并基于模板生成"report.html";`--input` 传分析结果 JSON,`--output` 输出网页路径，二者必填)。
- 参考:见 [references/standard-changes.md](references/standard-changes.md)(何时读取:进行任何变更点解读、差距分析时读取，是核心知识库)。
- 参考:见 [references/gap-analysis-guide.md](references/gap-analysis-guide.md)(何时读取:执行信息收集与差距分析流程时读取)。
- 参考:见 [references/standards-index.md](references/standards-index.md)(何时读取:需要核查标准原文精确措辞、定位某条款行号时优先读取，作为全文的索引导航)。
- 参考:见 [references/gbt-19001-2016.md](references/gbt-19001-2016.md)(何时读取:需核对 2015 版条文原文精确措辞时，按索引定位后分段读取;体量大勿整份加载)。
- 参考:见 [references/iso-9001-2026-zh.md](references/iso-9001-2026-zh.md)(何时读取:需核对 2026 版条文原文精确措辞时，按索引定位后分段读取;体量大勿整份加载)。
- 资产:见 [assets/report_template.html](assets/report_template.html)(用途:网页报告的母版，含样式与版式，由 generate_report.py 自动读取填充，无需外部手动修改)。

## 注意事项
- 严禁在未收集组织运行现状与体系文件时给出泛泛的升版建议;务必"先收集、再分析、后建议"。
- 变更点解读与建议应以 [references/standard-changes.md](references/standard-changes.md) 为依据;核对标准原文精确措辞时，通过 [references/standards-index.md](references/standards-index.md) 定位到两份全文对应条款后分段读取，勿整份加载大文件。
- 转版关键时间节点:ISO 9001:2026 于 2026-09-16 发布;2029-09-15 后 2015 版证书失效。执行计划应在此窗口前完成。
- 生成报告需使用脚本并校验结果;JSON 输入必须包含"change_points"数组，字段含义见脚本 docstring 与 [references/gap-analysis-guide.md](references/gap-analysis-guide.md)。
- 报告中的建议务必针对该组织，避免照搬通用模板;信息不足项标注"需补充"。