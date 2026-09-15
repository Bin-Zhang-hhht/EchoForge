---
item_id: changelog-1ebd24a2575b
title: Changelog 新闻速递：Agent 编码隐忧与 Web 依赖缺口
date: '2026-09-15'
published_at: '2026-01-19'
transcribed_at: '2026-09-15'
model: GPT-5.6 Sol
source_url: https://changelog.com/news/177
source_name: The Changelog
input_type: official_transcript
transcript_url: https://changelog.com/news/177/transcript
summary: Armin Ronacher 的维护者警告、AT Protocol 的社交文件系统视角、jQuery 4 的减法式升级与一组 Postgres 约定，共同追问依赖、复用和自动生成的成本由谁承担。
tags: [AI Agent, 开发者工具, 数据库, 开放标准]
---

# Changelog 新闻速递：Agent 编码隐忧与 Web 依赖缺口

> 节目：[The Changelog](/podcasts/changelog/)
>
> 节目发布：2026-01-19 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 4141 字 · 阅读约 11 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [数据库](/tags/%E6%95%B0%E6%8D%AE%E5%BA%93/) [开放标准](/tags/%E5%BC%80%E6%94%BE%E6%A0%87%E5%87%86/)
>
> 🎧 [收听原节目](https://changelog.com/news/177) · 📄 [查看官方逐字稿](https://changelog.com/news/177/transcript)

## 速读

Armin Ronacher 的维护者警告、AT Protocol 的社交文件系统视角、jQuery 4 的减法式升级与一组 Postgres 约定，共同追问依赖、复用和自动生成的成本由谁承担。

这期约六分钟的 Changelog News #177 是新闻导读，不是独立调查。被引用作者的体验、项目介绍和主持人判断都保留原归属：Agent 使用与睡眠、成瘾或维护质量之间没有在节目中建立因果；jQuery 覆盖率没有附统计来源；Postgres 清单也没有给出适用于所有系统的证明。

节目中段从 `It's now time for sponsored news!` 开始，到 `Life altering Postgres patterns` 之前为 Sonatype 赞助内容。本文排除该区间及其中的产品、安全与效果陈述。

## 主题正文

### Armin Ronacher：生成速度把成本推给维护者

Armin 从第一人称描述一种失衡：Agent 编码让人兴奋、少睡并快速做出东西，直到协作时才发现可能做过头。他观察到 issue 和 pull request 的质量明显下降，提交者却常把生成内容视为帮助；他还担忧有人与 AI 建立拟社会关系并在社群中相互强化依赖。这些是 Armin 的个人体验和维护者观察，不是临床诊断，也不能证明 Agent 使用必然导致成瘾或睡眠问题。（原文锚点：`Many of us got hit by the agent coding addiction.`；`The most obvious example of this is the massive degradation of quality of issue reports and pull requests.`；`I see people develop parasocial relationships with their AIs`）

主持人 Jerod Santo 没有把这些担忧包装成定论，而是说软件行业都在面对一次剧烈变化，并赞赏 Armin 公开承认自己也难以看清。可执行的提醒因此不是拒绝 Agent，而是把提交成本也算进生产率：生成者节省的时间，可能变成维护者验证意图、复现问题和拒绝低质量改动的工作。（原文锚点：`even folks like him are struggling to see this new world clearly.`）

### AT Protocol：用文件系统类比社交互操作

Dan Abramov 的切入点是文件范式：应用与格式是多对多关系，不同应用可以围绕同一格式工作，不必预先知道彼此。节目据此介绍他对 AT Protocol 的“social filesystem”类比，把内容与承载它的具体社交应用分开思考。（原文锚点：`Apps and formats are many-to-many. File formats let different apps work together without knowing about each other.`；`which Dan calls a "social filesystem."`）

这个类比适合提出问题，却不是互操作已经完成的证据。短新闻没有展开 AT Protocol 的记录模型、身份、权限、迁移或治理边界，只留下一个入口：个人文件系统从文件开始，社交文件系统从什么开始？要评估实际能力仍需阅读 Dan 的完整文章与协议资料。（原文锚点：`A personal filesystem starts with a file.`；`What does a social filesystem start with?`）

### jQuery 做减法，Web 依赖仍缺公共基础设施

Jerod 介绍 jQuery 4.0 时强调，近十年后的 major release 有不少破坏性变更来自删除功能，而不是继续增加表面积。节目称 jQuery 仍运行在约 71% 的网站上，但没有给出统计来源，也没有列出移除项和迁移成本；能确认的是成熟库选择用减法控制长期负担，而不是升级必然简单。（原文锚点：`After nearly ten years, the jQuery team has released a new major version`；`Many of the breaking changes are *removing* features`）

Lea Verou 从另一端批评 Web 平台：健康生态里的依赖应当普通、低成本且是一等公民，但 Web 把依赖管理外包给第三方工具，使复用承担额外权衡。她提出一个激进方案，同时承认自己并不完全确定它会奏效；逐字稿也未解释方案细节，所以本文不替原文补齐实现。（原文锚点：`In healthy ecosystems dependencies are normal, cheap, and first-class.`；`the web platform has outsourced this fundamental functionality to third-party tooling`；`one radical solution that she isn't entirely sure will work.`）

**编辑归纳：** jQuery 讨论成熟依赖如何减负，Lea 讨论依赖能力应由谁提供；两者共同指向复用成本的分配，但这不是两位作者直接提出的联合结论。

### Postgres 清单应变成团队讨论，而不是普适定律

Ethan McCue 的 Postgres 清单包括 UUID 主键、`created_at` 与 `updated_at`、限制更新和删除、schema、枚举表、软删除、状态日志、`system_id`、谨慎使用视图和 JSON 查询。节目只说这些做法改善了作者与同事的工作，没有提供负载、迁移和故障数据，也没有逐项解释例外。（原文锚点：`Use UUID primary keys`；`Almost always soft delete`；`Represent statuses as a log`；`Use views sparingly`；`JSON Queries`）

Jerod 也只同意其中“大多数”，并明确偏好复数表名。更合适的用法是把清单逐条转成团队决策：在哪些实体上需要软删除，状态是否真要保留历史，外键限制怎样影响清理流程，JSON 字段何时会绕开约束；而不是把个人经验复制成所有数据库的默认答案。（原文锚点：`I agree with *most* of these, but plural table names FTW...`）

## 来源与定位

- 原始节目：[Agent psychosis: are we going insane? (News)](https://changelog.com/news/177)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - Armin 对 Agent 编码失衡、维护质量与拟社会关系的观察（`Many of us got hit by the agent coding addiction.`；`The most obvious example of this is the massive degradation of quality of issue reports and pull requests.`；`I see people develop parasocial relationships with their AIs`）
  - Jerod 对行业共同困惑的限定（`even folks like him are struggling to see this new world clearly.`）
  - 文件多对多范式与 AT Protocol 的 social filesystem 类比（`Apps and formats are many-to-many. File formats let different apps work together without knowing about each other.`；`which Dan calls a "social filesystem."`）
  - 社交文件系统的起点问题（`A personal filesystem starts with a file.`；`What does a social filesystem start with?`）
  - jQuery 4 的发布时间跨度与删除式破坏变更（`After nearly ten years, the jQuery team has released a new major version`；`Many of the breaking changes are *removing* features`）
  - Lea Verou 对 Web 依赖基础设施及方案不确定性的判断（`In healthy ecosystems dependencies are normal, cheap, and first-class.`；`the web platform has outsourced this fundamental functionality to third-party tooling`；`one radical solution that she isn't entirely sure will work.`）
  - Postgres 清单中的主键、软删除、状态日志、视图和 JSON 查询（`Use UUID primary keys`；`Almost always soft delete`；`Represent statuses as a log`；`Use views sparingly`；`JSON Queries`）
  - Jerod 对清单仅部分赞同及表名分歧（`I agree with *most* of these, but plural table names FTW...`）
  - Sonatype 赞助区间的起止边界，区间内容未纳入本文（`It's now time for sponsored news!`；`Life altering Postgres patterns`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- Armin Ronacher 关于 Agent 编码的内容按个人体验和维护者观察呈现，不扩写为临床判断或因果证明。
- jQuery 覆盖率与 Postgres 实践按主持人转述或作者经验保留归属；逐字稿未提供独立统计或普适性证据。
- Sonatype 内容由节目明确标为 sponsored news，本文已排除完整区间及其中全部赞助陈述。
- 整理模型：GPT-5.6 Sol
- AI 编辑整理，请以原始节目为准。
