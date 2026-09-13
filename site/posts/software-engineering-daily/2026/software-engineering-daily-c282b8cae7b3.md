---
item_id: software-engineering-daily-c282b8cae7b3
title: 'AURA：用声明式 agent 框架把 SRE 从救火队员变成可靠性架构师'
date: '2026-09-13'
published_at: '2026-07-14'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/aura-and-open-source-agents-for-production-operations/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/07/SED1945-Andre-Elizondo.txt'
summary: 'Mezmo 产品负责人讲开源 AURA 框架：声明式定义 agent、Scratchpad 控上下文膨胀、分层记忆与"有治理的自治"，让 SRE 转向可靠性架构。'
tags: [AI Agent, 开源, 企业 AI]
---

# AURA：用声明式 agent 框架把 SRE 从救火队员变成可靠性架构师

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-07-14 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 4887 字 · 阅读约 13 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [开源](/tags/%E5%BC%80%E6%BA%90/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/aura-and-open-source-agents-for-production-operations/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/07/SED1945-Andre-Elizondo.txt)

## 速读

Mezmo 产品负责人 Andre Elizondo 接受 SED 访谈（主持人为 Kevin Ball），介绍 AURA——Mezmo 开源的声明式 agent 框架，面向 SRE 与平台工程。核心思路是把 Kubernetes 的"声明目标状态"哲学搬到 agent 编排：用简单 TOML 定义"让 agent 做什么"，而不是命令式地写"每一步怎么做"。对正在做生产运维 agent 化、或评估开源 agent 框架的团队，这是一份思路清晰的第一手设计文档。

最值得记的三点：SRE agent 与编码 agent 的三大差异（上下文工程、多 agent 编排、记忆与人在回路）；Scratchpad 用磁盘扁平文件做工具与模型之间的中间层以控制上下文膨胀；以及"有治理的自治"（governed autonomy）的渐进放权哲学。文中产品状态与数字均为受访者口径。

## 主题正文

### 背景：agent 时代的可观测性

Andre 的职业起点是运维系统（早年叫 sysadmin），现在负责 Mezmo 产品团队，目标是让运维人员获得编码 agent 过去几年已获得的收益。Mezmo 近 6–8 个月聚焦"agent 时代的可观测性"：因为 agent 更偏好原始数据、洞察与特定工具，而不是看 dashboard，可观测性系统本身要随之改变。公司目标在"软件工厂的后半段"——"运维的暗工厂"，不只把软件送进生产，还要改变健康维护、性能与成本优化的整个生命周期。（`00:03:08–00:05:17`）

Kevin 点出一个关键动机：可观测性因自动化而更重要——"agent 说没问题，但它真的按预期运行吗？"（`00:05:05`）

### AURA 的缘起与"冰山类比"

AURA 起初像多数厂商一样暴露 MCP server 供 agent 消费，但为了不让上下文膨胀（例如让 agent 一次消费一小时甚至一周的 trace 会立刻撑爆上下文窗口），把可观测性做成"主要为 agent 消费"。Andre 的核心论点是：通用、无观点的 agent 框架做 SRE 场景（日志模式识别、trace/metrics 的 RCA）时，前期要自己搭可靠工具调用、多 agent 编排等，投入巨大、阻碍成功——他称之为"冰山类比"（同 Kubernetes、云）：水面之上是"模型 + 简单框架 + 提示词"，水面之下才是可靠性。AURA 的目标是"缩短到达结果的回路"，受 Kubernetes 启发：声明目标状态而非命令式步骤，让工具从第一天就近可用且工作流可靠。（`00:05:17–00:09:44`）

声明式定义的形态：开源、遵循 Linux 哲学的"合理默认"——"如果不需要调每个环节，就用内置默认"；可调 reasoning budget、quality score、自评/自纠循环。配置是简单的 TOML 文件：定义 agent（工具 + 简单系统提示词），无需定义推理循环与自纠循环。（`00:10:27–00:14:40`）

### Scratchpad：控制上下文膨胀的关键设计

Scratchpad 是 AURA 的原生概念，配置文件一行开启：作为工具与模型之间的中间层，把工具输出落到磁盘上的简单文件供模型交互，并自行判断工具是否需重调、可复用上次工具调用（可跨 agent 共享）。它专门解决像 Prometheus MCP server 这类"把一切可能结果都塞回来"导致的上下文膨胀。Andre 还批评商业方案/嵌入现有运维工具的 agent 多为黑盒，而 AURA 的 day-one 原则是完全透明——可看、可交互、可调。（`00:11:45–00:14:40`）

### SRE agent 与编码 agent 的三大差异

面对"生产环境 SRE agent 与笔记本上的编码 agent 有何不同"，Andre 给出三大支柱。一是上下文工程：任何模型的限制都是上下文窗口；编码 agent 的上下文≈代码，SRE 的上下文是运行时数据加基础设施加可观测性（trace/metrics/log）。"把一周的 trace/log/metric 塞进窗口再指望模型不产生幻觉"不可行，且生产规模使该问题自动放大、不会在第一天暴露。二是多 agent 编排：让不同 agent 分工（安全审查者、集群调查、代码库调查）并行，更快且避免单一上下文窗口成为瓶颈；通用框架里这通常是"第三四天"才撞上的问题，AURA 从第一天内置。三是人在回路、记忆与面向任务的观点：事故调查的记忆应是"之前看过哪些事故、如何解决、发生了什么"，而非通用记忆。（`00:14:40–00:21:01`）

自治的主张是渐进梯度——Copilot → assistant → 完全自治（"暗工厂"/关灯），逐步授予而非"要么全自动要么全手动"。（`00:19:30–00:21:01`）

### 多 agent 编排与 token 经济性

实现上，TOML 中定义 orchestrator（顶层 agent，系统提示词 5–20 行）和多个 worker（名字/描述/preamble，可限制工具以控上下文膨胀）。orchestrator 自动完成规划、分发、执行、自评，置信度阈值可调，通常初始设 70%。对照 LangChain 等通用框架——要自己写推理循环、重试与韧性。（`00:21:37–00:24:02`）

当前是"单路进、单路出"（single path in/out），Andre 承认这会随 harness 发展而改变；多 agent 工作流"很容易快速变得非常复杂"，day-one 刻意保持简单。token 经济性是声明式的红利：orchestrator 可用大模型（如 Opus）做规划推理，worker 可声明不同小模型（如 Haiku、开源模型），"大小模型混用"从第一天可用，他称已看到"相当惊喜的结果"。交互大量用磁盘扁平文件——"每个 LLM/agent 都擅长跟文件交互"，机制简单可靠，"坏的时候你知道为什么坏，理想情况根本不坏"。（`00:24:22–00:26:51`）

### agent 自身的可观测性与透明性

AURA 原生用 OpenTelemetry 全量插桩（GA 之前的早期访问阶段即硬性要求），trace 的 span 中可见"下一步推理如何做、工具调用是否成功"；自带服务端事件流回客户端，实时展示调查过程；内置 CLI 支持 /stream、/expand 命令查看后台活动。trace 可发往任意支持 OpenTelemetry 的系统，得到交互的可审计性（做了什么、为什么、推理步骤）。Andre 的信任论点：生产场景下你必须确切知道 agent 背后在做什么才能信任它，否则你不会把它放进生产、不会分派更多任务；可观测性不限于 Mezmo 商业产品。（`00:27:42–00:30:09`）

### 分层记忆与制度性知识

Andre 批评通用记忆（如 ChatGPT memory）是"一大坨不分化的乱象、无可见性"。AURA 采用分层记忆：低层是 turn/session 级（最近几秒、上次工具调用、上次运行结论），类比 RAM vs 硬盘 vs 离线存储；长时程记忆时间窗是过去 6 个月、12 个月，把"服务劣化 + 某人推的 GitHub 变更 + 日志异常"拼成集体记忆/简单 briefing 交给 agent。长时程记忆在 Mezmo 平台内以异步后台进程提供（内联太 heavy、且不让 agent 为记忆浪费 token）。技术实现上目前取"最低公分母"——另一个工具：经 MCP server 暴露为 investigations，工具调用返回 briefing；实验做法是给 agent 提供虚拟文件系统注入记忆（免工具调用、不耗 token），处于 research preview。（`00:31:00–00:36:42`）

制度性知识方面：团队 runbook 常存于 Confluence/GitHub，如果暴露了类似 vector database 的东西就很容易接入作为 agent 的 grounding。Andre 强调 agent 不只单向消费 runbook，还能在调查中反馈——开 PR 更新 runbook；Mezmo 内部用 AURA 跑自家 SRE 工作流，反馈机制效果积极。（`00:37:03–00:38:52`）

### 人在回路与"有治理的自治"

人在回路取决于多个维度：agent 背后的系统类型、对工作流本身的信心、对返回数据的信心。"单向门"（one-way door）工具（写/修复类）设硬屏障，agent 必须先求助再继续；或限制 agent 在流程中能走多远（只读，产出"给 SRE 去执行脚本/修复"的打包结果，之后完全交接）。完全自治则要求用可观测性数据随时间打分、验证足够次数后才给"全权放行"。他提出"有治理的自治"：配置驱动，MCP server 暴露 ask-for-help 工具，后台自动关联"谁是 on-call、Slack 通知、反馈"——agent 不必花上下文摸清求助渠道。（`00:39:35–00:44:16`）

### 开源边界与 SRE 角色演进

AURA 可脱离 Mezmo 使用；开源边界上，"如果你想要不同的人在回路流程，我们发布 spec，告诉你如何定义"，Mezmo MCP server 提供最省事的默认实现。当前主要贡献者来自 Mezmo（"小而强"），采用 Apache 2 license 降低贡献门槛，已是 AAIF（Linux Foundation 下属 agent 基金会）成员；未来可能移交基金会，CNCF"大概很挤"，AAIF 较新、是潜在选项，但"不想操之过急"。（`00:41:30–00:46:00`）

项目用 Rust 编写，Andre 的理由很妙："不是每个人都懂 Rust，但每个 agent 都懂 Rust"——有模型加 token 即可贡献，降低开源贡献门槛。他提出两个轴：production AI（agent 如何在生产中良好运作——多 agent、可靠调工具、记忆）与 AI for production（需要哪些任务/技能/工具让 agent 处理高价值难题），Mezmo 处于两者交汇。愿景是提升 SRE 角色——从"救火队员"转向"可靠性架构师"，以设计方式构建可靠性；内部实例中，所有工程师参与 on-call，SRE 构建护栏/系统/工作负载，使其他人更容易接 pager，原本困在 SRE 脑子里的部落知识借 agent 变成 as code、自动化、标准化。（`00:48:10–00:51:32`）

## 来源与定位

- 原始节目：[AURA and Open-Source Agents for Production Operations](https://softwareengineeringdaily.com/podcasts/aura-and-open-source-agents-for-production-operations/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 背景与 agent 时代可观测性（00:03:08–00:05:17）
  - AURA 缘起、上下文膨胀与冰山类比（00:05:17–00:09:44）
  - 声明式定义与合理默认（00:10:27–00:14:40）
  - Scratchpad 与黑盒批评（00:11:45–00:14:40）
  - SRE 与编码 agent 的三大差异（00:14:40–00:21:01）
  - 自治梯度主张（00:19:30–00:21:01）
  - orchestrator/worker 与置信度阈值（00:21:37–00:24:02）
  - 单路进出、token 经济性与磁盘文件（00:24:22–00:26:51）
  - OpenTelemetry 全量插桩与可审计性（00:27:42–00:30:09）
  - 分层记忆与长时程记忆（00:31:00–00:36:42）
  - runbook 反馈与制度性知识（00:37:03–00:38:52）
  - 人在回路与"有治理的自治"（00:39:35–00:44:16）
  - 开源边界、Apache 2 与基金会走向（00:41:30–00:46:00）
  - Rust、两个轴与 SRE 角色演进（00:48:10–00:51:32）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 产品能力、置信度与时间窗等数字均为受访者口径，未作独立验证；本期主持人为 Kevin Ball。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
