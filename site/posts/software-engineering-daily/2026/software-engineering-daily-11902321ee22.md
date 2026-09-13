---
item_id: software-engineering-daily-11902321ee22
title: '零信任的个人 Agent：NanoClaw 的沙箱、凭证外置与 fork 生态'
date: '2026-09-13'
published_at: '2026-07-21'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/nanoclaw-and-the-rise-of-personal-ai-agents/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/07/SED1943-NanoClaw.txt'
summary: 'NanoClaw 创始人 Gavriel Cohen 讲清零信任 Agent 编排：Agent 不可信、凭证不进环境、沙箱边界强制约束，并用"fork 即定制"加 Skills 打造开源生态。'
tags: [AI Agent, 开发者工具, 开源]
---

# 零信任的个人 Agent：NanoClaw 的沙箱、凭证外置与 fork 生态

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-07-21 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 5167 字 · 阅读约 13 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/nanoclaw-and-the-rise-of-personal-ai-agents/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/07/SED1943-NanoClaw.txt)

## 速读

NanoClaw 创始人 Gavriel Cohen 接受 SED 访谈（本期主持人为 Kevin Ball），讲清为什么 OpenClaw 式的个人 Agent"价值巨大但危险"，以及他如何用零信任架构重建它。核心机制是三层：每个 Agent 独立 Docker 沙箱、凭证完全留在 Agent 环境之外、代理网关执行策略并强制人工审批。

最有价值的是具体的安全判断与工程数字：Agent 必须当恶意程序对待（"千万别删生产数据库"写在提示里本身就是它删过的证据）；一台 16 核/64GB 机器能跑约 200 个并行 Agent 容器；以及用"fork 即定制 + Skills"替代插件生态的思路。主持人 Kevin Ball 把 OpenClaw 形容为"即将发生的灾难，让人挪不开眼"——这句话是理解全期的引子。

## 主题正文

### 从 OpenClaw 到 NanoClaw：为什么必须零信任

Gavriel 的背景是从特拉维夫大学物理与计算机科学起步，在 Wix 做了约七年软件开发者，停写代码几年后约一年半前（正值 Claude Code 发布）回归编程。他把 OpenClaw 形容为"搁置安全与软件质量顾虑的疯狂实验"：把前沿编码 Agent 接到一切能拿到价值的地方，但伴随巨大安全问题——凭证暴露在 Agent 环境里、访问权限远超任务所需。他自己曾用 OpenClaw 搭 AI 原生营销代理公司，把 Agent 设为"销售经理"（挂载销售数据），它产出晨报、设提醒、更新文件，"很快开始像员工一样工作"，随后发现大量安全问题，于是自建 NanoClaw。（`00:02:09–00:04:36`）

零信任的出发点很直接：Agent 不可信。AI 是非确定性的，无论指令写得多强硬都不可靠；他调侃代码库里 claude.md 顶部写着"永远永远不要 drop production DB"——说明它删过、还会再删。只要 Agent 能接触未净化数据（邮件、PR 都可能含 prompt injection），就可能被注入并反向作恶，"必须把 Agent 当作恶意程序对待"。Kevin 呼应：Agent 一旦受外部影响，就等于处理用户生成内容，必须某种"消毒"，NanoClaw 的消毒就是隔离。（`00:04:36–00:07:48`）

### 三层安全机制与"一切皆消息"

NanoClaw 的三层机制：每个 Agent 独立沙箱（隔离宿主机与其他 Agent）；凭证/密钥/API key 不放 Agent 环境，外发请求经 Agent 旁的小型 vault 代理、在环境之外注入凭证；在代理网关执行策略与访问控制，并含人工审批。示例：Agent 可连邮箱但不持有凭证，可设策略"可自由读邮件，但发送/删除需我逐条审批"。（`00:04:36–00:07:13`）

实现上，Agent 跑在 Docker 容器（另有新选项 Docker Sandboxes，Docker 专门为跑 Agent 开发、有额外加固），挂载一个文件夹作为文件系统；策略是"不在环境内逐条检查，而让 Agent 在环境里疯跑，在环境边界强制约束"。编排结构是一个 NanoClaw 实例可含多个 Agent，宿主进程（host process）负责编排、路由消息；关键设计是两个 SQLite 数据库（inbox 与 outbox）：宿主收到消息判定路由给某 Agent 后写入其 inbox，沙箱内小循环进程拉取并推给 Agent（默认 Anthropic Claude Agent SDK，也可用 Codex 或 OpenCode），Agent 完成后写 outbox，宿主拉取后路由到 Slack/WhatsApp 等。"一切皆消息"：除少量注入的环境变量外，进出 Agent 环境的全部是消息——定时任务、循环任务、审批请求与响应都是消息。（`00:07:48–00:12:58`）

为什么用外部进程管理消息？为了在边界强制"Agent 能发给谁、从哪收"。他举了 WhatsApp 的例子：普通 WhatsApp 大多用 Baileys 包（逆向 WhatsApp 桌面 API 的非官方社区连接），连接会绑到你的 WhatsApp 身份、可访问每个群与联系人。他调试日志时发现 OpenClaw 把每个 WhatsApp 群和联系人的每条消息都以明文存到本地文件（不只它被加入的那个群），由此断定"无法用于生产业务场景"；NanoClaw 默认只存所连群的消息。（`00:11:19–00:13:28`）

### 容器生命周期与上下文压缩

容器并非常驻：Agent 调 MCP 工具发"定时任务"消息给宿主，宿主写入 inbox（带 process-after 时间戳），容器空闲 30 分钟（默认）无活动即关闭，宿主到点拉起容器、循环进程启动即拉消息。压力测试数字：1 台 16 核/64GB 机器可并发运行约 200 个 Agent 容器，2 核/8GB 机器只能并行 8–10 个。他妻子的"Andy"例子展示了机制：要求"某条牛仔裤降价时提醒我"，Andy 自设每天早上 9 点的循环任务、用环境内浏览器访问商品页比价、降价则发 WhatsApp——但 Gavriel 明确表达对 Agent 自设任务"是否真的执行"的怀疑。（`00:16:25–00:22:43`）

上下文压缩刻意简单：直接用 Claude Code 默认压缩，只加少量指令规定保留消息进出顺序、发送者、时间戳，长消息总结内容但保留"包装"。Agent SDK 压缩阈值默认 200K，NanoClaw 设到 165K，因为模型接近上下文阈值时会有"上下文焦虑"、开始变笨、急于收尾走捷径。记忆采用"LLM wiki"模式：让 Agent 把内容存成文件、建索引、更新 claude.md、自建记忆系统。已知问题：Claude Code 会话 JSONL 会膨胀到 50、100、几百 MB 后开始崩坏，需要"轮换会话并拉取上下文"但尚未实现——他承认"是将来要加的东西"。（`00:23:05–00:26:34`）

### 多 Agent、审批门与隐私

Agent 可互聊、也可创建 Agent：MCP 工具 create agent 给出名字与指令定义，新 Agent 拥有独立容器/文件系统/环境/内存；消息走 outbox → 宿主 → 对方 inbox。Agent 间直连需把对方加入"已知且被批准的目的地"（既是权限也是发现机制）；另一种模式是把两个 Agent 放进同一 Slack 频道互聊（可见、你也在场）。明确缺失的功能：Agent 间直连通信的审批门尚未实现；跨人场景（我的 Agent 可向你的 Agent 要信息）中若涉及私密内容，应在响应发出前加审批门查看内容。（`00:26:54–00:32:22`）

隐私观点：多人共用一个 Agent 应放在群聊而非 DM，因为 DM 会产生虚假的隐私感——同一 Agent 可能在另一 DM 里把你告诉它的一切分享给别人；群聊让大家对齐"这是公开论坛"。若想共享部分"LLM wiki/知识图谱"，第一步是每条外发消息都经人审批，之后可考虑用分类器/LLM 自动放行明显安全的信息——他明确承认这是在牺牲安全换便利，敏感信息加匿名公众用户场景不应这样做。（`00:29:59–00:32:22`）

### 制品传递、Agent factory 与"fork 即定制"

内部自建 Agent factory 来评审 NanoClaw 开源项目的 PR：最有价值的部分是判断"是否与项目哲学一致"（这是品味与判断，Agent 即使有指令也不擅长）；另做安全/代码质量评审并产出测试计划。测试流程是给测试 Agent 一个已检出 PR 分支的 VM，实际运行 NanoClaw 实例、发消息做真实 QA；GitHub CLI 命令由 Agent 写成草稿在 Slack 展示，人批准后才以审批者自己的凭证执行——"是我们在行动，不是 Agent 自动合并"。制品传递也体现了安全边界：Agent 把制品写进特定位置并调用确定性工具，宿主只从该特定位置取文件，Agent 不能任意指定宿主读取位置。（`00:32:47–00:36:45`）

产品哲学是安全加极简主义：能跑 bash、写任意代码的自治 Agent 是"狂野西部"，人人都该紧张；"只有代码小、简单才可审计，用户才应自己验证而非因星多就信任"。合并规则只合入对 80–90% 用户相关的改动，数百行的小众代码一律不合并。定制即代码级定制（fork）：支持改代码是一等能力，要求模块化编码与极简集成点，fork 只保留所需（如去掉 WhatsApp 则代码与依赖都不含）；他承认文档没讲清 fork 与上游契约、用户拉更新有挫折，近几天正在定义"对 fork 维护者的契约"。（`00:38:01–00:44:39`）

商业模式：NanoClaw 开源（MIT 许可、免费），公司 NanoCo 已融资 1200 万美元，商用方向是把 Agent 带给不想自建平台的企业。Kevin 用 Shadcn 类比（拷贝组件即拥有），Gavriel 认同并称 Shadcn 是灵感之一，但差异在于组件库拷贝一次即可，而 coding agent 每天变多次、用户必须能持续拉取更新。他提到 Karpathy 关于 claws 的大帖点名 NanoClaw，"slightly blew his mind"（他称这是最高赞誉），Karpathy 惊叹的是用 skills 定制/回馈 fork 的做法。Skill 在此指"修改 NanoClaw 的说明"（如加 Spotify 集成），不是运行期技能，而是指导 coding agent 改代码的指令，可带脚本与用户指引；应用基本确定性但"并非完全确定性"，集成点会变、coding agent 靠意图描述补全。（`00:43:00–00:50:49`）

### Agent provider 抽象与给开发者的建议

NanoClaw 用注册表模式抽象 Agent provider，可插入其他 coding agent，已支持 Claude 系、Codex、OpenCode；ACP（Agent Client Protocol）的 PR 待合并。一个明确的分歧点：Gavriel 只在 coding agent 层面集成、不做跨 LLM 的 API 路由转发，断言"LLM 路由行不通且会越来越糟，因为模型是在各自 harness 内训练的"；Kevin 反驳 OpenCode 等本身可做多模型多路复用，Gavriel 回应 Claude 家族模型间或有兼容性，但 Claude/Codex/Gemini 之间指令、技能、工具定义差异很大，"迁移不像人们希望的那样顺畅"。记忆系统他也刻意不建复杂确定性方案，只给一组"存文件/建索引/更新 claude.md"的指令，相信模型越强、自管理记忆越好。（`00:51:21–00:57:48`）

给开发者的建议很务实：不要用 LangChain/LangGraph 从零造 Agent——他去年自建，须处理缓存、工具定义、压缩、会话管理，"数月数月的工作"才做出 Claude Code/Codex/OpenCode 的核心能力；应把 coding agent 当作构建块、在其上做产品。也别纠结选哪个模型或 Agent，前沿模型都够用；构建时用前沿模型、先别优化成本，除非使用场景天然对成本极度敏感，否则先做出高价值再考虑降本。（`00:57:56–01:00:19`）

## 来源与定位

- 原始节目：[NanoClaw and the Rise of Personal AI Agents](https://softwareengineeringdaily.com/podcasts/nanoclaw-and-the-rise-of-personal-ai-agents/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 背景与 NanoClaw 由来（00:02:09–00:04:36）
  - 零信任出发点与"Agent 不可信"（00:04:36–00:07:48）
  - 三层安全机制与"一切皆消息"（00:07:48–00:12:58）
  - WhatsApp 明文存储问题（00:11:19–00:13:28）
  - 容器生命周期、定时任务与压力测试数字（00:16:25–00:22:43）
  - 上下文压缩与"LLM wiki"记忆（00:23:05–00:26:34）
  - 多 Agent 交互与缺失的审批门（00:26:54–00:32:22）
  - 群聊隐私观与自动审批取舍（00:29:59–00:32:22）
  - Agent factory 与制品传递边界（00:32:47–00:36:45）
  - 极简主义、合并规则与 fork 定制（00:38:01–00:44:39）
  - 商业模式、Shadcn 类比与 Skills（00:43:00–00:50:49）
  - Agent provider 抽象与跨模型分歧（00:51:21–00:57:48）
  - 给开发者的建议（00:57:56–01:00:19）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 融资、性能数字与产品状态均为受访者口径，未作独立验证；本期主持人为 Kevin Ball。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
