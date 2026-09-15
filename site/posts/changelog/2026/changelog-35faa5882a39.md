---
item_id: changelog-35faa5882a39
title: 把 MCP 用对了：Cloudflare Code Mode 如何用约 1000 tokens 装下 2500 个 API
date: '2026-09-15'
published_at: '2026-05-15'
transcribed_at: '2026-09-15'
model: GLM-5.3 Flash
source_url: https://changelog.com/podcast/681
source_name: The Changelog
input_type: video_agent_kit_asr
summary: Cloudflare 的 Matt Carey 访谈：服务端 Code Mode 用 search+execute 两个工具在约 1000 tokens 里装下 2500 个 Cloudflare API，Dynamic Worker Loader 沙箱执行模型代码，并谈工作流、三 agent 上限与 agent 记忆设计。
tags: [AI Agent, AI 架构, 开发者工具]
---

# 把 MCP 用对了：Cloudflare Code Mode 如何用约 1000 tokens 装下 2500 个 API

> 节目：[The Changelog](/podcasts/changelog/)
>
> 节目发布：2026-05-15 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 5386 字 · 阅读约 14 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://changelog.com/podcast/681)

## 速读

The Changelog 第 681 期（全长约 115 分钟，录制于 2026 年 3 月）：主持人 Adam Stacoviak 对话 Cloudflare 的 Matt Carey（负责 Agents SDK 与 MCP）。核心论点：MCP 协议本身设计良好，被用错了——大多数 MCP 服务器把「一个端点映射成一个工具」，于是工具定义塞满上下文；Cloudflare 的做法是把 Code Mode 移进 MCP 服务器，只暴露 search 与 execute 两个工具，让模型写代码去检索 OpenAPI 规范、组装 API 调用，约 1000 tokens 的上下文即可覆盖约 2500 个 Cloudflare API 端点。执行安全由 Dynamic Worker Loader 保证：模型写的代码在独立主机的 V8 isolate 里跑。后半段转入工作流与记忆设计，信息量同样密集。本文基于 ASR 转写整理，专名与归属以官方节目页核对为准。

## 主题正文

### 被工具定义吃掉的上下文

Matt 从 MCP 的源头讲起：2024 年 11 月由 Anthropic 的两位工程师发布，协议由 tools、prompts、resources 三部分组成，其中工具远超其他两者的使用量；如今几乎所有大型 SaaS 公司都发布了 MCP（`00:09:15`–`00:11:32`）。他对 MCP 相当乐观——「我不认为我们在修复 MCP，我们只是把 MCP 用到了它能力上限」，问题出在最初的用法（`00:08:29`–`00:08:44`）。传统路径是函数调用：GPT-4 之后普及，每个工具的 schema 都要在开场注入模型；GitHub 的 MCP 服务器最初约 1.5 万 tokens，而最好的模型在 50K tokens 左右就开始掉性能，Claude Code 因此要频繁触发压缩（`00:12:03`–`00:14:39`）。他给了一笔账：想做一个真正自动化你工作的个人 AI，需要的函数可能上百个——按 1 端点 1 工具的映射法，上下文先爆（`00:14:51`–`00:15:07`、`00:20:09`–`00:20:59`）。

### 服务端 Code Mode：search + execute 两个工具

Code Mode 的思路是回 到 codeact：模型见过海量代码，那就让它写代码而不是逐个调用工具。2025 年夏 Cloudflare 发布第一版 Code Mode（在 agent 侧做代码执行），但半年下来采用者寥寥——要求每个 agent 自带代码执行环境太难；于是 Matt 把它移进 MCP 服务器，几周前发布了服务端版（`00:07:20`–`00:08:02`、`00:15:14`–`00:15:43`、`00:18:02`–`00:19:31`）。设计极简：整个服务器只导出 search 和 execute 两个工具。search 不是搜索函数，而是让模型直接写代码遍历 Cloudflare OpenAPI 规范（`spec.paths` 加朴素过滤）；execute 则给模型一个 `cloudflare.request` 客户端随它调用（`00:21:21`–`00:22:31`）。结果是约 2500 个端点的整个 Cloudflare API 被装进约 1000 tokens 的 MCP 服务器里（`00:08:09`–`00:08:23`）。他的演示十分钟即可从零构建并部署一个 Next.js 站点，全程没有任何代码落在本机——只存在于对话上下文和云端（`00:22:31`–`00:23:24`）；Cloudflare 内部的周五 demo 上演完后当场决定发布（`00:23:39`–`00:24:25`）。

### 安全性：Dynamic Worker Loader 与沙箱权限

「把模型写的代码拿来执行」传统上人人色变，而 Dynamic Worker Loader 这个云原语改变了前提：把一段字符串代码放到独立主机的 V8 isolate 里全沙箱运行，可以近乎即时地扩到十亿级小脚本，还能用 global outbound 限制外连——代码即使被注入恶意指令也困在笼子里（`00:16:10`–`00:18:01`）。他在结尾建议：想让 agent 做安全的生产部署，别在终端里裸跑，看看沙箱解释器——比如 Monty（ASR 记为 pydantic 出品，为 code mode 打造的 Python 解释器）或 Dynamic Worker Loader（`01:45:12`–`01:47:01`）。他还比较了 bash 与 TypeScript SDK：bash 是 agent 时代的通用语，但 TS 能预生成类型、权限模型也更干净——沙箱解释器可以检查每一条试图离开 isolate 的 fetch，形成围住模型的 ACL/防腐层，比「yolo 进终端」好得多（`01:47:09`–`01:49:00`）。

### 缘起：一个周末的 Agents SDK 和一个周二

团队协作方式的两个细节值得记录：Agents SDK 是技术负责人 Sunil 一个周末写出第一版（agent 即 Durable Object，一行导出）、一周后上架的（`00:25:17`–`00:25:54`）；服务端 Code Mode 则是 Matt 拖了几周后，某周二坐下来和 Claude 聊清楚方案动手做的（`00:26:11`–`00:26:23`）。他拒绝给模型配搜索函数的核心理由：给了搜索就得建评测，而让模型写代码「保持在训练分布里」，模型越强这套东西自动越强（`00:26:46`–`00:27:39`）。这支团队同时支撑 Agents SDK、MCP（含对外发布的整套服务）和 Sandboxes 三条产品线，不久前还是 5 个人，录制时约 6 人、马上 7-8 人；他们担心的是变成过于狭窄的领域专家，因此互相跨域补位（`00:42:40`–`00:43:58`）。团队目标直白：跑在组织需求前面——组织还想要的，他们已经准备好（`00:47:38`–`00:48:11`）。

### Matt 的工作流：跳过权限、Zig git 护栏、三个 agent 上限

他 100% 的时间用 `--dangerously-skip-permissions` 跑 Claude Code，底气来自自建护栏：一个用 Zig + libgit2 写的 git 包装器 Zaggy（公开在 GitHub），从根上禁止任何 agent 强推或覆写远端仓库——「本地随便弄坏，外部不行」（`00:29:21`–`00:30:47`）。他的效率心法是坐下前先想清楚要什么：没有预设地跟模型闲聊「像在刷 Instagram，喂的是假多巴胺」；对话方式就是「问题、目标、现状、差距，开聊」，不做角色扮演（`00:30:51`–`00:32:39`）。自圣诞前后的 Opus 4.5/4.6 起，他把编码 agent 统统开在顶层 code 目录里，用 worktree 切换仓库，IDE 只用来 review（`00:33:14`–`00:34:12`）。并行度方面他很诚实：羡慕能同时开 6 个 agent 的人，自己上限是 3——「脑子里只能装 3 个问题还能保证每个的产出质量」，1 对 1 又太慢，2–3 是甜区（`00:53:14`–`00:55:06`）。1 对 1 时他反而会犯「抢跑」的毛病：脑子比模型打字快，忍不住中途纠偏，结果把执行轨迹搅乱——所以他更爱 2–3 个并行、plan 由另一个模型 review 的节奏（`00:55:57`–`00:56:36`）。

主持人的循环也很有代表性：写 PEP（project enhancement proposal，致敬 PEP）做计划，然后固定四连问——「review this plan for lack of clarity and blind spots」「what are your suggestions for each」「fix the plan」「do it」，并指出这本质是 reflection 加思维链提示的日常化；Opus 4.6 有时已会主动补上 suggestions 那步（`00:57:18`–`01:01:10`）。Matt 的总结自我减压：「这些都不聪明。聪明的部分是你坐下时知道自己要做什么」（`01:01:50`–`01:02:03`）。

### 记忆：全是问题，暂无答案

Matt 目前聚焦 agent 记忆，但他自称「只有问题，没有答案，先攥着牌」（`01:18:56`–`01:21:17`）。需求清单很长：跨会话记住对话并可检索、支持 skills（按需加载进上下文的 markdown）、会话压缩、持续学习、会话向长期存储迁移；API 还必须可编程、足够灵活，新趋势来了不用破坏性升级（`01:19:45`–`01:24:41`）。设计约束同样具体：不能替用户选存储（有人要 Durable Objects + SQLite，有人要 PlanetScale/Neon），所以走 provider 模式，也要兼容 Vectorize 等向量方案；像系统提示那样的常驻指令与 agent 可改写的待办清单（工作上下文）则需要不同的加载路径（`01:22:12`–`01:23:48`）。它最初会落在 Agents SDK 里，但不该绑运行时——ECS、Lambda、Vercel 上的 Next.js 都该能用（`01:24:41`–`01:25:43`）。

### 台风眼外的火花

两条 high-signal 的支线：一是他对 AI 写作的定位——「AI 是给极有主见的人的解锁：你不必擅长写，只需擅长批评」。他讨厌摘要（「一个人的摘要是另一个人的糊渣」），Code Mode 博客初稿就是对着 Granola（他当医生的父亲用它彻底改变了问诊记录流程）口述再让 AI 挑要点而不是总结（`01:12:00`–`01:12:53`、`01:14:19`–`01:16:01`）。二是给 CLI 时代的实用建议：他给自家所有 CLI 加 `--agent` 标志，用 markdown 向 agent 解释「这是什么、怎么用」——agent 解析帮助的方式和人不同；而 Changesets 这类全交互式 CLI 对 agent 极不友好，他打算提 PR（`01:49:02`–`01:50:22`、`01:51:14`–`01:52:16`）。

## 来源与定位

- 原始节目：[MCP on Code Mode (Interview)](https://changelog.com/podcast/681)
- 定位：时间戳取自 ASR 逐字稿。
  - MCP 起源与三大原语（00:09:15–00:11:32）
  - 「不是修复 MCP，是用到上限」（00:08:29–00:08:44）
  - 工具 schema 撑爆上下文：GitHub MCP 约 1.5 万 tokens、50K 掉性能（00:12:03–00:14:39）
  - 1 端点 1 工具的映射上限与个人 AI 需要上百函数（00:14:51–00:15:07、00:20:09–00:20:59）
  - Code Mode 沿革：2025 夏首版到几周前服务端版（00:07:20–00:08:02、00:15:14–00:15:43、00:18:02–00:19:31）
  - search+execute 设计与 OpenAPI 规范直查（00:21:21–00:22:31）
  - 约 2500 端点 / 约 1000 tokens 与无落盘演示（00:08:09–00:08:23、00:22:31–00:23:24）
  - Dynamic Worker Loader、V8 isolate 与 outbound 限制（00:16:10–00:18:01）
  - Sunil 周末版 Agents SDK 与 Matt 的周二（00:25:17–00:26:23）
  - 拒绝搜索函数：保持在训练分布（00:26:46–00:27:39）
  - 三条产品线与 5→8 人团队（00:42:40–00:43:58、00:47:38–00:48:11）
  - 跳过权限 + Zaggy git 护栏（00:29:21–00:30:47）
  - 「假多巴胺」与不做角色扮演（00:30:51–00:32:39）
  - 三 agent 上限与抢跑毛病（00:53:14–00:56:36）
  - PEP 计划循环与 reflection+CoT（00:57:18–01:02:03）
  - 记忆设计的需求与 provider 模式（01:18:56–01:25:43）
  - Granola、「AI 是给有主见的人的解锁」（01:12:00–01:16:01）
  - `--agent` 标志与 Changesets 之痛（01:49:02–01:52:16）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 该期节目暂无官方逐字稿（节目页逐字稿区为 Coming Soon 占位、官方逐字稿仓库未收录），时间戳取自 ASR 逐字稿。
- ASR 转写的说话人标签不可靠，正文按官方节目页的参与人信息与上下文归属：嘉宾为 Matt Carey（Cloudflare，Agents SDK 与 MCP），主持人为 Adam Stacoviak；专名（Code Mode、Dynamic Worker Loader、Durable Objects、supermemory、Granola 等）按官方节目页与公开资料核对，ASR 无法可靠辨认的产品名（如若干记忆方案）在正文略去。
- 广告段落（Coder、Tailscale、RWX）未纳入正文。
- 无法独立验证的数字（如端点数、token 数）仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
