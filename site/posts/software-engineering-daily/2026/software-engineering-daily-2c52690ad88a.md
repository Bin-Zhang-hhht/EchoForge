---
item_id: software-engineering-daily-2c52690ad88a
title: 'OpenAI 内部的 Codex：每个 PR 都由 Agent 审查之后'
date: '2026-09-13'
published_at: '2026-01-29'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/openai-and-codex-with-thibault-sottiaux-and-ed-bayes/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/01/SED1898-OpenAI.txt'
summary: 'Codex 工程负责人与产品设计师谈模型与 harness 共同演化：内部每个 PR 由 Agent 审查、代码生成"几乎已解决"、瓶颈转向审查与验证。'
tags: [AI Agent, LLM, 开发者工具]
---

# OpenAI 内部的 Codex：每个 PR 都由 Agent 审查之后

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-01-29 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3320 字 · 阅读约 9 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [LLM](/tags/LLM/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/openai-and-codex-with-thibault-sottiaux-and-ed-bayes/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/01/SED1898-OpenAI.txt)

## 速读

OpenAI Codex 工程负责人 Thibault Sottiaux 与产品设计师 Ed Bayes 做客 SED（主持为 Kevin Ball），讲 Codex 的产品与模型如何共同演化。最有信息量的是 OpenAI 内部的真实用法：每一个 PR 都由 Codex 审查、作为"安全网"每天拦截大量缺陷——因为生成代码变便宜后，人工 review 的时间预算不变，而 Codex 可以更深入。以及关键判断："代码生成几乎已解决"，瓶颈正转向审查、部署、规划与用户反馈。

文中判断多为受访者口径；该集逐字稿存在多处明显的转写乱码（访谈方说明），涉及处按可读部分归纳。

## 主题正文

### 沙箱默认与模型-harness 共同演化

Codex 起源于 Web 版（Codex cloud），运行在完全隔离的虚拟机中（底层为 Kata Containers，逐字稿拼作 catacontainers），后经 CLI 与 VS Code 扩展带到本机、保持 safe by default。Thibault 的因果很直接：不用沙箱等于把机器控制权交给一个高能力智能体、使用你的凭据行动；存在不用沙箱的用例，官方不建议但支持。产品端的 UX 摩擦缓解包括：按命令细粒度批准并可存入 config、IDE 扩展区分 agent 模式与只读模式；风险来源包括 agent 无意伤害与 prompt injection。（`00:06:20–00:09:55`）

模型与 harness 的关系是"共同演化"（co-evolution）：harness 类比为"身体"，涉及"如何安全地作用于世界"；产品形态尚未找到与日益智能系统交互的"最终形态"——未来 agent"永不被打断、一直运行"时，产品界面将是"另一场游戏"。（`00:04:17–00:06:20`）

### OpenAI 内部：每个 PR 都由 Codex 审查

"everything is Codex"——Codex 模型、Web、CLI 被视为同一个编码 agent 出现在不同空间。企业内部的关键用法：OpenAI 内部每一个 PR 都由 Codex 审查、作为安全网，每天拦截大量关键缺陷；其审查深度超过人与人互相 review 所投入的时间——因果是生成代码变便宜后，人工 review 的时间预算不变而 Codex 可更深入。（`00:10:12–00:11:55`）

规模的例子：Sora 与最近的 Atlas 中，代码库的整块部分仅凭一个想法加少数几个人 steer 一系列 Codex agents 即可搭建；deep research 团队约 1 名 PM、1 名设计师、几名工程师与研究员，且刻意保持小规模。设计师的 Slack 群里作品从静态 Figma 演变为可交互原型——设计师自述"不会写代码，直到用了 Codex"，Codex 消解学科边界、是 "great equalizer"。（`00:14:17–00:15:53`，`00:12:45`）

### 瓶颈转移："代码生成几乎已解决"

Thibault 的核心判断：代码生成"几乎已解决"，瓶颈正转向代码审查、部署、规划与引入用户反馈；正因预判 review 会成为瓶颈，团队很早投资了 code review。部署与线上 on-call 若由 agent 驱动，动作本身携带高风险，"如何安全地做到这一点仍是非常开放的问题"。（`00:13:47–00:17:36`）

架构上，harness 刻意简单："一个 for 循环、一堆工具调用、为编码设计的工具"，全部开源、"没有那么多魔法"；用户意图 → 控制权交给模型 → 工具调用 → 观察结果 → 循环可达数百次。真正的难点在循环外围的产品：如何控制、引导、监督 agent，以及多 agent 协作的交互界面。Ed 的类比：ChatGPT 发布时极简（文本进文本出）；agent 交互更像人与人的协作——像请同事"搭建一套新基础设施"。产品哲学是 "delightfully open-ended"：主持人的"先写文档再出三方案互相论证"的工作流被评价为极其强大，但产品刻意不规定流程。（`00:28:59–00:32:59`，`00:36:21–00:38:16`）

### 多模型策略与 Codex 专用模型线

模型线：CLI 默认 GPT-5.1-Codex-Max，另有 5.1 Codex、5.1，新发布 GPT-5.2——在 GDPval（逐字稿误写 GDP file）基准上有超过 20% 的提升；主流基准多已饱和，故改用衡量"经济价值"的基准。GPT-5 Codex 系列是"在 Codex harness 内单独训练、在该 harness 中更有效"的版本。一个未调和的分歧：主持人在 Cursor 中使用裸 GPT-5.1 反而常比 Codex 版好用；Thibault 的回应是 agent = 模型 + 工具集 + 上下文处理的组合体，对模型与 harness 共同训练（co-train）可获得更好结果，未直接解释 Cursor 场景。延迟布局两条路径：compute 越靠近用户笔记本越好（减少往返）；Codex Web 则把 VM 搬到离 GPU 尽可能近的地方。（`00:17:36–00:28:59`）

### 超越代码生成：心智模型与缺失原语

一个前瞻判断：未来 agent 的更深角色是帮用户高效理解周围世界的状态（如每天告知代码库变化）；"代码生成最终可能只占 agent 所做工作的很小一部分"。案例：新工程师通过与 Codex 对话深入理解代码库、减少打扰同事；团队几乎不写"如何运作"的文档，更多写"为何存在"。非技术岗用法：写文档、创意构思、数据分析、处理 CSV。（`00:32:59–00:36:21`）

缺失原语从 GitHub issue 的最高票来：呼声最高的是 subagent，团队正积极研究 multi-agent networks；其余大量是 "product overhang"——如何让产品更适合大规模管理、引导、监督 agent。Ed 提出的设计问题：从"看 1 分钟的 rollout"到"10 小时的任务"，如何保持掌控感。hooks"最终会做"；最强用户（包括 OpenAI 内部最多产用户）维护自己的 Codex fork——开源的直接好处；CLI 用 Rust 编写、理由是健壮与性能。（`00:40:13–00:44:23`）

### 通用性张力与收尾

一个自认的张力：OpenAI 内外越来越多非技术人员在终端使用 Codex，存在"通用性的拉力"——最好的编码 agent 是能在代码之外推理的 general agent；但团队当前 "laser-focused 于让 Codex 成为专业软件工程的最佳工具"，认为两者最终结合得很好。收尾观点：现在是"有问题最幸福"的时代，应质疑两年前有效的工作方式；六个月前设计师展示静态 Figma，如今是功能完整的小产品，"比我们已上线的东西还好，最好尽快发布"。（`00:44:23–00:49:51`）

## 来源与定位

- 原始节目：[OpenAI and Codex with Thibault Sottiaux and Ed Bayes](https://softwareengineeringdaily.com/podcasts/openai-and-codex-with-thibault-sottiaux-and-ed-bayes/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 沙箱默认与 UX 摩擦缓解（00:06:20–00:09:55）
  - 内部每个 PR 由 Codex 审查（00:10:12–00:11:55）
  - 瓶颈转向审查、部署与规划（00:13:47–00:17:36）
  - 多模型策略与 co-train 主张（00:17:36–00:28:59）
  - harness 即 for 循环、难点在外围产品（00:28:59–00:32:59）
  - 心智模型更新与"代码生成占很小一部分"（00:32:59–00:36:21）
  - 缺失原语来自最高票 issue（00:40:13–00:44:23）
  - 通用性张力与收尾（00:44:23–00:49:51）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。该集逐字稿存在多处明显的 ASR 错乱（原方说明），涉及处按可读部分归纳、不补写内容。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 模型版本、基准提升、内部团队规模等均为受访者口径，未独立验证；主持人在 Cursor 中的相反经验与受访者 co-train 主张之间的张力如实保留。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
