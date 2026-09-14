---
item_id: talk-python-dccdbce49654
title: '从模型循环到 Agent Harness：LangChain Deep Agents 的 Python 组件'
date: '2026-09-14'
published_at: '2026-04-01'
transcribed_at: '2026-09-14'
model: GPT-5.6
source_url: https://talkpython.fm/episodes/show/543/deep-agents-langchains-sdk-for-agents-that-plan-and-delegate
source_name: Talk Python To Me
input_type: official_transcript
transcript_url: https://talkpython.fm/episodes/show/543/deep-agents-langchains-sdk-for-agents-that-plan-and-delegate.vtt
summary: 'Deep Agents 把长任务 Agent 的规划、文件系统、子 Agent、记忆与 middleware 组合成可扩展的 Python harness，同时把模型选择、工具权限和人工审批留给开发者。'
tags: [AI Agent, 开发者工具, 开源]
---

# 从模型循环到 Agent Harness：LangChain Deep Agents 的 Python 组件

> 节目：[Talk Python To Me](/podcasts/talk-python/)
>
> 节目发布：2026-04-01 · 逐字稿获取：2026-09-14 · 笔记整理：2026-09-14
>
> 全文共 4725 字 · 阅读约 12 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://talkpython.fm/episodes/show/543/deep-agents-langchains-sdk-for-agents-that-plan-and-delegate) · 📄 [查看官方逐字稿](https://talkpython.fm/episodes/show/543/deep-agents-langchains-sdk-for-agents-that-plan-and-delegate.vtt)

## 速读

Deep Agents 不是一个替你选定模型的聊天机器人，而是 LangChain 为长时间、多步骤任务提供的 Agent harness：在基本的模型—工具循环外，加入规划、文件系统、子 Agent、记忆、上下文压缩和可插拔 middleware。LangChain 的 Sydney Runkle 在这期节目中说明，这些组件让开发者可以用几行 Python 组装类似 Claude Code 的专用 Agent，同时保留自定义工具、模型和部署方式。（`00:18:57–00:20:03`，`00:32:13–00:33:02`）

这期适合正在做研究、数据分析、代码自动化或内部助手的 Python 开发者。最值得关注的边界是：节目讨论的是录制时已公开的开源库与 CLI 能力，不是“一个 prompt 就能得到可靠结果”的承诺；工具权限仍要在边界处约束，敏感操作可以接入人工审批，远程文件系统、沙箱和最终 `1.0` 则属于正在推进或即将细化的方向。（`00:55:31–00:58:46`，`00:59:47–01:01:06`）

## 主题正文

### Deep Agent 的差别在于 harness，而不只是模型

嘉宾把传统的“浅层 Agent”描述为模型根据提示，在工具调用循环中完成几步操作，例如调用航班或酒店工具；Deep Agent 面向的是上下文更多、过程更长、需要持续组织的复杂任务。这里的“深”不是某个特定模型的名称，而是 Agent 能否在更长的工作跨度中保持行动能力。（`00:05:45–00:06:43`）

Sydney 将 Agent harness 定义为围绕核心模型与工具调用循环添加的支持层：基础 Agent 是“给模型提示词和工具，然后循环直到产出结果”，harness 则加入让复杂任务更有效的额外能力。她以 Claude Code 为编码场景的例子，归纳出充足上下文、自主组织任务、子 Agent、待办事项以及面向用户的记忆等特征；这说明 Deep Agents 的目标是抽象出一类构建方法，而不是复刻一个只面向编码的成品。（`00:19:33–00:20:03`，`00:11:34–00:12:11`）

主持人把“能检查并重新验证”作为 Claude Code、Codex 一类工具与一次性问答的差异：先读代码、写改动，再运行 Ruff 或单元测试，根据结果继续修改。Sydney 同意迭代和更强的工具能力会增加实用潜力，但同时保留了基本前提：使用者仍应对 AI 输出提出追问并要求它检查工作；节目没有给出错误率或质量基准。（`00:07:30–00:08:17`，`00:10:32–00:11:17`）

### 四类内置能力管理长任务的上下文

第一类是规划工具。Sydney 以 Claude Code 的待办清单为例，说明 Agent 可把复杂问题拆成步骤并逐项完成；她也把这种思路与模型先进行更多推理后再回答的趋势联系起来。规划被介绍为提升困难任务轨迹的机制，而不是保证计划正确的验证器。（`00:20:51–00:22:16`）

第二类是文件系统。模型的上下文窗口有限，选择性地搜索、读取和写入文件，可以把长期工作材料放在模型之外，按需要重新取回。节目用“读教材后仍能回去查章节”来解释这种上下文管理；文件系统因此是记笔记和保留中间产物的工作空间，不代表文件内容本身就经过事实核验。（`00:22:31–00:23:53`）

第三类是子 Agent，重点是并行化和上下文隔离。研究任务可以沿多条路径并行推进，批量修改相似文件也可以同时分派；每个子任务只接收所需上下文，主 Agent 不必把所有历史都带入。这个机制可以提高复杂任务的组织效率，但节目没有承诺并行一定更快，也没有讨论并发成本和失败重试策略。（`00:24:06–00:25:53`）

第四类是系统提示词与记忆。Deep Agents 会通过系统提示词告诉模型如何使用文件系统、规划工具和子 Agent，并把可跨对话保留的记忆加载进去；Sydney 还说明，冗长的共享提示词可做 prompt caching，以免每次调用都重复承担同样的成本。主持人提到 Claude Code 的系统提示词约 16,000 字，这个数字是对 Claude Code 的节目现场观察，不是 Deep Agents 的提示词长度或效果指标。（`00:25:53–00:28:38`）

### Python API 把模型、工具与 MCP 分开组合

录制时，Deep Agents 的快速开始是导入 `create_deep_agent`、调用它，再按需要传入模型、工具和提示词等配置；返回的 Agent 可以被调用，也可以进一步部署。创建函数会在底层加入规划和文件系统能力，开发者仍能补充面向具体场景的日历、邮件等工具。节目提到项目从当年夏天开始、当时约有 10,000 个 GitHub stars；这两个数字都属于录制时的项目状态，不能当作当前版本或成熟度结论。（`00:31:39–00:32:02`，`00:32:13–00:34:07`）

自定义工具可以是普通 Python 函数。函数签名中的类型，以及描述参数用途的 docstring，会被转换成模型可使用的 schema；因此模型知道何时调用工具、要填哪些参数。工具不局限于返回文本，也可以处理多模态内容、图像和其他类型文件。这里的便利来自函数定义与文档，而不是模型自动理解任意未说明的业务规则。（`00:34:09–00:37:40`）

MCP 在本期被解释为让 Agent 从外部服务器取得工具的标准化接口：Deep Agents 可以消费 MCP server 提供的工具，不是被描述为替开发者搭建 MCP server。这样既可接入团队或社区已经实现的工具，也可让工具从 API 获取较新的或私有数据。Sydney 还明确表示可以使用不同供应商的模型、开源模型适配器，并让子 Agent 采用更便宜、更快的模型；“任何模型”仍取决于 LangChain 的具体适配器与相应凭据配置。（`00:39:08–00:41:48`，`00:42:34–00:43:18`）

在这套分层里，LangChain 提供模型和 Agent building blocks，LangGraph 被定位为负责模型—工具迭代、流式输出、持久性和部署能力的运行时，而 Deep Agents 是加入规划、文件系统等逻辑的 harness。录制时还展示了 Deep Agent CLI：这是构建在开源 harness 之上的编码 Agent，支持流式输出、模型切换和内置记忆，内部团队也在使用；它仍应理解为一个示例性产品入口，而不是 SDK 对所有工作流的默认界面。（`00:43:30–00:45:55`）

### Middleware 连接生命周期，也连接安全边界

长对话接近模型上下文限制时，工具需要压缩历史。Sydney 说 Deep Agents 会在底层持续跟踪并总结，从而保证不会遇到 context overflow error；这是嘉宾对库行为的强表述，节目没有提供不同模型、不同工具负载下的测试数据，因此不能把它扩大为所有部署条件下的容量保证。（`00:46:07–00:46:40`）

Middleware 是 LangChain 1.0 在当年 10 月发布的机制，被描述为模型节点和工具节点之间的生命周期扩展点。它可以在模型调用前检查是否需要总结，在敏感工具执行前要求人在回路中审批，也可以提供模型 fallback、工具重试、个人信息检测和待办清单等预置能力；开发者还可以构建自己的 middleware。比如发送邮件或执行交易前先审批，正是把业务规则放到工具边界的例子。（`00:47:27–00:49:16`）

安全部分的核心不是让模型“自我约束”，而是让允许做什么的边界落在工具和运行时。Sydney 提醒，Agent 越自主越有用，但执行代码、使用沙箱或调用敏感 API 都需要开发者设计限制；LangGraph 提供人工审批和拒绝的支持。CLI 默认会要求工具调用经过人工确认，并可逐步把反复确认的操作加入白名单；具体策略仍由使用者决定。（`00:55:31–00:57:46`）

### 示例已能说明方向，路线图仍要单独看

项目示例包括 Deep Research、Content Builder、Text-to-SQL 和所谓 Ralph mode。Deep Research 使用 Tavily 做网页搜索，目标是处理更长、更彻底且需要当前信息的任务；Agent viewer 可以逐步展示摘要 middleware、模型步骤、工具调用和 trace，帮助开发者观察 Agent 到底做了什么。这里展示的是调试与理解工具，不是对研究结果正确性的证明。（`00:50:04–00:52:16`）

Text-to-SQL 示例让 Agent 依据数据库结构把自然语言问题转换为 SQL，再执行并回答；节目将它作为数据分析和业务逻辑的有力模式，但没有提供准确率、数据安全或错误查询的评估。Deep Research 还有 notebook 和 LangGraph 开发 UI；Sydney 说他们最近推出了由 Deep Agents 驱动的无代码 Agent Builder，能够以聊天界面呈现工具调用等信息。无代码入口是录制时已发布的产品描述，不应与更早的概念验证 UI 混为一谈。（`00:53:03–00:55:10`）

未来部分需要和当前能力分开。Sydney 说团队正在朝 `1.0` 推进，先巩固核心原语；远程文件系统，包括 S3 后端或数据库后端，已经被作为可用选项提到，但更详细的 roadmap 仍计划发布。她把沙箱、执行代码，以及让通用 Agent 通过写代码完成数据分析和其他自动化，视为很有前景的方向；这些是趋势判断或推进方向，不是本期给出的交付时间表。（`00:57:56–00:58:46`，`00:59:47–01:01:06`）

## 来源与定位

- 原始节目：[#543: Deep Agents: LangChain's SDK for Agents That Plan and Delegate](https://talkpython.fm/episodes/show/543/deep-agents-langchains-sdk-for-agents-that-plan-and-delegate)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Deep Agent 与浅层 Agent 的任务跨度、harness 定义及可靠性边界（00:05:45–00:12:11；00:18:57–00:20:03）
  - 规划、文件系统、子 Agent、系统提示词、记忆与 prompt caching（00:20:51–00:28:38）
  - Deep Agents 项目状态、快速开始与 Python 工具函数（00:31:39–00:37:40）
  - MCP、模型适配、子 Agent 模型选择、CLI 及 LangChain/LangGraph 分层（00:39:08–00:45:55）
  - 上下文总结和 middleware 的生命周期、审批、重试与自定义机制（00:46:07–00:49:16）
  - Deep Research、Agent viewer、Text-to-SQL 与 Agent Builder（00:50:04–00:55:10）
  - 工具边界、人工审批、白名单、沙箱与执行代码的风险（00:55:31–00:58:46）
  - `1.0` 方向、远程文件系统、路线图与 harness engineering（00:59:47–01:01:06）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 文中的项目 stars、提示词长度和功能状态均按录制时的节目语境呈现；嘉宾个人实验、主持人举例和路线图没有改写成产品保证，未提供的质量、成本和安全数据也未自行补充。
- 整理模型：GPT-5.6
- AI 编辑整理，请以原始节目为准。
