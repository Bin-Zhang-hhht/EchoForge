---
item_id: software-engineering-daily-1a321f11ed1f
title: '给 Agent 组织上下文：Unblocked 的 context engine 与真相漂移难题'
date: '2026-09-13'
published_at: '2026-03-05'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/organizational-context-for-ai-coding-agents-with-dennis-pilarinos/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1913-Unblocked.txt'
summary: 'Unblocked 创始人 Dennis Pilarinos 谈 agent 时代的组织上下文：真相漂移与冲突消解、permissions-aware 问答、"大厂 6 个月制造了超历史的技术债"。'
tags: [AI Agent, 企业 AI, 开发者工具]
---

# 给 Agent 组织上下文：Unblocked 的 context engine 与真相漂移难题

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-03-05 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3192 字 · 阅读约 8 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/organizational-context-for-ai-coding-agents-with-dennis-pilarinos/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1913-Unblocked.txt)

## 速读

Unblocked 创始人 Dennis Pilarinos（约 20 年开发者工具经验，BuddyBuild 被 Apple 收购）接受 SED 访谈（主持为 Kevin Ball），讲 agent 时代最被低估的问题：组织上下文。核心难题有两个——找到上下文在哪（搜索问题），以及判定"什么才是真相"（源代码说一回事、Slack 会话说另一回事、Jira 又是另一回事）。

最有价值的三个观点：指望团队整理并持续维护文档是 "fool's errand"，所以要对 PR diff 做嵌入、为组织构建 background knowledge graph；权限必须在查询执行时判定、防止被用作权限提升；以及一个引语——"大厂过去 6 个月制造的技术债超过其整个历史"。

## 主题正文

### 上下文的定义与所在

Dennis 的术语澄清："上下文"从技术角度是 "decision grade context"（机器做出正确决定所需的全部信息）；对人是 tribal knowledge——隐性知识。新人第一天的 onboarding 就是"上下文加载"，人与机器的上下文问题高度相似。上下文的物理位置：Slack、Teams、源代码及其历史、PR、bug tracker、文档系统、运行时生产系统。（`00:00:00–00:05:35`）

两大难题：找到上下文在哪；判定"什么才是真相"。他的类比性断言：如果一个"人"总是对你撒谎，你不会信任他——缺乏冲突消解的 AI 系统同理。用户和 agent 通常问两类问题："今天是怎么工作的？"与"我们做了哪些决策才走到这里？"——问题有时间维度；LLM 开箱对时间处理很差，Unblocked 的机制是对所有 artifact 加权、得出"那个时点的真相"，还需知道提问者是谁、实际有权访问什么。（`00:05:35–00:13:34`）

### 权限与三层技术结构

访问控制必须在运行时、查询执行时判定：demo 中 "project cantaloupe" 的发布日期在有权限时能回答、撤销权限后再问就答"我不知道"——尽管数据仍在知识库里。最难的平衡是"既要给出答案，又不能被用作权限提升"。

技术结构三层。数据层前提：他从没见过一个团队说"我们的文档井井有条且保持最新"——指望团队维护文档是 "fool's errand"；所以 Unblocked 对历史 PR 做 diff 并嵌入，为组织构建 "background knowledge graph"。身份层：GitHub、Slack、Notion 的身份互不相同、必须绑定。底层是 hybrid RAG（lexical + semantic）加 agentic——RAG 正被用到极限，agentic 工具可以自己去取答案；引用 Paul Graham "software is eating the world"：一切都有 API，若工具能调用 API 且尊重权限模型，就能点亮大量场景。（`00:13:34–00:18:34`）

### 用户数据与"快 vs 准"

产品内置满意度调查：数万人回答、95% 说有帮助；剩余 5% 中约一半只是讨厌填问卷。两个趋势让人们对幻觉的敏感度下降：用户形成了识别 AI"过度自信"的直觉；技术自我核查能力大幅提升。"fast answers vs thorough answers"功能的内部争论结果是压倒性多数愿意为更高质量的答案等待——"事后看似显然"。（`00:18:34–00:21:22`）

### 计划生成、写回与源代码即真相

计划生成解决两个问题：确保人与 agent 之间的契约被充分理解；给 agent 的计划做上下文增强后"计划质量显著更好"——原本会在 PR 评审中卡住的问题被"左移"消化。是否让 agent 写回各系统"取决于公司对写回的舒适度"。核心主张：冲突消解中 Unblocked 对源代码本身权重很高——"source is the truth of what's actually happening at that point in time"。他提出一个思想实验：一家只靠面对面沟通、直接 `git push -f` 到 main 的公司，agent 长期表现会如何？greenfield 应用表现好，因为它不需要理解历史系统故障沉淀出的"坏模式"。（`00:21:22–00:27:19`）

### 瓶颈转移到 code review 与"6 个月 vs 全历史"

SDLC 瓶颈正在转移到 code review。他引述："大厂过去 6 个月制造的技术债超过其整个历史"（逐字稿转写存疑，按上下文理解）；开源社区的 backlash——维护者不想要 AI 生成代码，因为它给接受者带来维护负担。具体案例：他用 Claude Code 做内部工具时，Claude 建议"把 API key 放进环境变量"——他认为这会"把我们搞进大麻烦"；Unblocked code review 指出正确做法是加密存入 vault。他的行为变化：不是自己改，而是让 Claude 去读这条 review 意见并实现。开放性疑问：PR 的初衷是围绕代码库演化建立共享知识——bot 写码加上下文层评审加自动改，这个回路会被"短路"吗？"两年后 PR 还在不在，我非常好奇"。（`00:30:44–00:34:08`）

### 演进路线与不变的 BXT

变化速度：亲历的浪潮序列是 on-premise → 云 → 移动 → 这一波；去年 11-12 月（"Claude 成了人们在假期里拿来 hack 的好玩东西"）是阶梯式跃迁。产品演进路径：Q&A 平台（服务人）→ 把 Q&A 提供给工具/agent → 意识到核心资产是 context engine → 在引擎上构建 code review 产品 → 现在把引擎暴露给组织（SDK/MCP/CLI）。未解的前沿问题他坦言"一时没有答案"：agent 拿走所需知识后，人如何保持更新？每个 on-call 工程师的噩梦是"支持一个自己不知道它如何工作的东西"；"你到底需要理解系统的多少？我猜一年内、甚至更短，我们就会知道"。（`00:34:08–00:38:44`）

不变的答案是他早年接触的 BXT 模型（Business-Experience-Technology）：业务问题 → 最佳用户体验 → 支撑技术。做 Unblocked 的"几乎就是 BuddyBuild 的同一批 10 个人"；公司现名 Unblocked，代码库里最早的名称是 "Bother"。他的类比断言：人写代码需要多少上下文，agent 写出"能解决业务问题的代码"就需要同样多的上下文。（`00:44:38–00:47:29`）

## 来源与定位

- 原始节目：[Organizational Context for AI Coding Agents with Dennis Pilarinos](https://softwareengineeringdaily.com/podcasts/organizational-context-for-ai-coding-agents-with-dennis-pilarinos/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 上下文定义与两大难题（00:03:00–00:07:27）
  - 时间性与冲突消解（00:10:41–00:13:34）
  - 权限执行与防权限提升（00:13:34–00:15:06）
  - 三层技术结构与 background knowledge graph（00:15:06–00:18:34）
  - 满意度数据与"快 vs 准"（00:18:34–00:21:22）
  - 计划生成与源代码即真相（00:21:22–00:27:19）
  - 瓶颈转移到 code review 与"6 个月 vs 全历史"（00:30:44–00:34:08）
  - 演进路线、BXT 与收尾（00:34:08–00:47:29）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。逐字稿个别转写存疑处（big bangs、REPL time 等）已按上下文理解并标注。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 满意度数字与技术债引语均为受访者口径，未独立验证；"运动队"式匿名案例不涉及本篇。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
