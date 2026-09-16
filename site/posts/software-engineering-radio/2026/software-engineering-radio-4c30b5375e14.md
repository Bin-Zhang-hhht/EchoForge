---
item_id: software-engineering-radio-4c30b5375e14
title: 用 Agent 做 SRE：iLert 的 AI 值班工程师，四分钟根因分析与"把上下文握在自己手里"
date: '2026-09-17'
published_at: '2026-05-06'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/05/se-radio-719-birol-yildiz-on-building-an-agentic-ai-sre/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/05/se-radio-719-birol-yildiz-on-building-an-agentic-ai-sre/'
summary: 'iLert CEO Birol Yildiz 讲述 AI SRE 的构建：四分钟根因分析目标、agentic search 取代向量库、三 agent 分工与语义测试，以及两条铁律——拥有你的上下文，并以 Claude Code 为基准。'
tags: [AI Agent, 软件工程, 可观测性]
---

# 用 Agent 做 SRE：iLert 的 AI 值班工程师，四分钟根因分析与"把上下文握在自己手里"

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-05-06 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 7574 字 · 阅读约 19 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) [可观测性](/tags/%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/05/se-radio-719-birol-yildiz-on-building-an-agentic-ai-sre/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/05/se-radio-719-birol-yildiz-on-building-an-agentic-ai-sre/)

## 速读

iLert 联合创始人兼 CEO Birol Yildiz 与主持人 Kanchan Shringi 复盘他们构建"AI SRE"——一个处理生产事故的 AI 值班工程师——的全过程:从 2024 年底"让 AI 开浏览器看仪表盘"的最初构想,到推理模型与 MCP 双双成熟后的今天,架构信条变成了"从推理模型的路上让开,只定义 what,不规定 how"。

最值得带走的三点:根因分析的目标是四分钟内完成(2 分钟确认事故+2 分钟凌晨三点坐到电脑前);agentic search 用 grep、jq 这类"老派命令行管道"替代向量库,大数据永远不进上下文;而给 Agent 建设者的两条铁律是——永远拥有你的上下文(连 MCP server 都要 fork 后自己调优),以及拿 Claude Code 当基准:做不出超越它的理由,就别做。

## 主题正文

### Agent 的定义,与一个"赌对了推理模型"的起源

Yildiz 对 agent 的定义聚焦在自主性上:一个运行在推理循环里、自行决定求解轨迹的 LLM——与"每小时检查邮件并起草回复"的工作流(那只是"有一点代理性")划清界限。AI SRE 从第一天起就瞄准 agentic:传统解法是把每种事故写进 runbook 再自动化执行,但他们想要处理"没有 runbook 的新颖事故"。起点在 2024 年底,最初构想很具象:模拟一个人类响应者——打开一堆标签页,看图表、仪表盘、日志,靠截图拼出全局。他们下注的两个前提当时都还是赌注:推理模型会成为现实,以及 MCP(Model Context Protocol,最初由 Anthropic 发布、随后被包括 Google 与 OpenAI 在内的前沿实验室采纳的 agent 访问外部系统的标准协议)会流行起来——两者都在几个月内兑现。而第一版实现走了弯路:尽管已经用上推理模型,系统提示却写了一千多行,把"通常的成功路径"逐条规定给模型;经过多次迭代,今天的信条是"尽可能从推理模型的路上让开,只定义 what,把 how 留给它"。（原文锚点：`a large language model running in a reasoning loop and deciding its own trajectory`；`the model context protocol took off`；`more than a thousand lines`；`get as much as possible out of the way of the reasoning model`）

### 四分钟 RCA 与 agentic search

AI SRE 的内部目标是四分钟内完成根因分析(RCA):2 分钟是成熟客户确认事故的典型耗时,再加 2 分钟——凌晨三点被电话叫醒、走到电脑前的时间。人工 RCA 的经验值是 10 到 45 分钟,复杂事故二三十人的 war room 能拖到一小时。诚实的部分他也讲了:RCA 完成时间可以精确测量(搜索空间大时偶尔超时到十分钟以上),但"RCA 是否准确"测不准——给用户装了点赞/点踩按钮,"他们就是不点"。他定义的 agentic search 也令人耳目一新:agent 手握命令行时代就广为人知的工具,读文件、grep、把输出用管道喂给 jq 再筛字段——底层数据再大也永远不会进入上下文;与之相对的方案是维护向量库和同步管线。他的自嘲很到位:"agentic search 就是用老派终端命令的花哨说法。"（原文锚点：`we want our AI SRE to finish root cause analysis within four minutes`；`it can take up to an hour`；`agentic search is a fancy way of just using old school terminal commands`）

### e-bike 类比与四层架构:知识用纯文本,不建向量库

AI 在公司的渗透程度:CTO 分享的数据是上个月 AI 生成的已提交代码占比突破了 95%,近三个月约 90%;从设计讨论到代码生成全线使用。但他对"AI 让工作更容易"的说法做了重要修正——那是个 e-bike 类比的误区:电助力车不会让你更快,只是更省力;AI 让"写代码"这个动作变容易,可"我们的工作不是写代码,而是为客户创造价值"——所以 AI 实际上让工作变得更难了,因为你必须掌握新技能。（原文锚点：`our AI generated committed code is, has passed in the last month I think 95%`；`AI makes our job harder because we need to master a new skill`）

AI SRE 的架构分四块。编排器(orchestrator)是所有 AI 服务的统一入口,负责 token 成本管理与请求路由;agent 服务封装了全部 agent 逻辑,客户可以为团队构建专属 agent,授予 GitHub、可观测性栈的访问权限并装配领域知识。知识层的设计最能体现"从路上让开"的哲学:没有索引企业知识库的 RAG 管线,agent 拥有自己的长期记忆,由专职的 discovery agent 在初始化阶段自动捕获——比如服务拓扑与服务间依赖(根因分析高度依赖这些),且尽量从遥测数据自动推断,而不是靠人工维护服务目录。存储上"完全不用向量数据库":结构化信息(服务目录)直接 enrich 进结构化对象,部落知识(比如"这个服务每天半夜因为有定时任务跑而崩溃")则以纯文本/markdown 形式存放,检索靠 agent 自己的 agentic search——向量库的最大代价是"原始知识一更新,向量也要同步"的维护负担,而 agent 搜索同等有效。他拿编码 agent 做了佐证:Cursor 早期给代码库建索引,Claude Code 什么都不建,只有少数几个工具加管道式搜索,"看它如何处理海量数据而完全不污染上下文,令人着迷"。（原文锚点：`we don’t have a rack pipeline that we index knowledge from a corporate repository`；`the equivalent of a clot.md file`；`it never makes it into the context`）

### 三个 agent、subagent 与 fork:把编排权逐步交给模型

生产中的 agent 分工清晰:discovery agent 负责初始化摸底,root cause agent 是主推理循环,verification agent 负责"验证 agent 自己提出的修复";另有独立的聊天入口,处理"没有告警、没有工单,人类直接描述疑似重大事故"的场景。大搜索量任务有两种隔离形态:subagent(全新上下文,只带问题描述,适合日志分析这类多步查询)与 fork(继承父上下文全部历史的子上下文,适合"需要完整背景才能判断查询是否相关"的场景)。指导原则是"预期大量输入输出时,用 fork 或 subagent,别把主上下文撑爆";而正在实验的第三种方案最激进——给 agent 提供创建 subagent、fork 会话的工具,让它自己决定在哪一层做。18 个月的演化轨迹被主持人一语道破:从大量自研编排代码,到"发现模型做决策可能比我们做得更好",于是不断放权。框架方面他们几乎不用——没用过 LangGraph 之类,CTO 手写了第一版编排;如今唯一依赖的"框架"是一个 Rust 写的代理层,用来统一对接 OpenAI、Anthropic、Mistral 各家不同的 API。（原文锚点：`a subagent has a fresh context`；`a fork in contrast is also another LLM context, but that receives the entire parent context`；`trying to give it more freedom in that sense`）

### 评测:语义测试、LLM judge 与嵌入分数

评测分两层。第一层是"vibe testing"的严格版:在自己的 staging 环境制造混沌——甚至用其他 agent 来制造故障场景——然后让 AI SRE 找根因;缺点是整套环境太贵,无法大规模跑。于是过去三个月他们建了"语义测试":把生产中真实调查的完整过程(每次工具调用、每个返回、最终的 RCA 文档)录制为测试集,在换模型或改提示后重放对比。判定方法有两个,仍在并行实验:一是 LLM-as-a-judge,比较录制版本与新版本并参考人工标注;二是基于嵌入的打分(嘉宾口称 bad score)——把预期输出与新输出各自向量化,比较向量距离,成本极低且因为自托管嵌入模型而可以无限次跑、不依赖外部 API。测试集还能来自客户的真实调查,"依赖不属于我们的数据"反而是优势。（原文锚点：`semantic tests`；`those semantic tests are recordings of actual investigations`；`an embedding model that creates a vector of your output`）

### 真实案例:一次渗透测试引发的自我故障,与四分钟内的根因

最好的案例来自自家基础设施。产品里的状态页允许客户配置来自 Datadog、Prometheus 的指标展示;外部渗透测试发现了一个盲 SSRF 漏洞——攻击者可以猜测内部 URL。修复方案是在 K8s 集群下发网络策略,禁止指标服务访问内部系统,但策略写得太宽:该服务连自己的数据库都够不着了,状态页的指标区域随即停更,事故发生。这个案例是 AI SRE 的完美试金石,原因有二:第一,"任何 runbook 都不会写这种事"——新颖事故没有 runbook;第二,"metrics"这个词歧义太大,内部有一堆与指标相关的服务(Prometheus 时序库等),搜索空间巨大。AI SRE 拿到的唯一输入就是"客户报告 metrics 不工作了":它先在 K8s 集群里找名字带 metrics 的 pod,做多步查询,在日志里发现"metrics store 尝试访问数据库失败"的症状,进而追查部署事件、GitHub 上合并的 PR,必要时直接看 diff——"我把它讲得像规定好的流程,其实不是;多步查询、推理、大海捞针,这就是 agent 的天性"。当然,数据源是预先提供给它的,但搜索空间大到必须靠 agent 自主探索。（原文锚点：`the vulnerability is, is a blind SSRF attack`；`that network policy was too broad`；`finding the needle in the haystack`）

自主权的推进则相当克制:当前永远有人在环。演示里 agent 可以全自动完成"根因分析→创建事故→更新客户→应用修复"的全链路,但每次演示都声明"别在家里这样做"。通往自主的路径从 observe-only 开始:只读 agent 也可以提出一键批准的动作(内存溢出时加倍 pod 内存、回滚到上一个部署这类低风险操作),人类只负责点批准;而走向更多自主的前提是足够多的数据证明它表现良好,机制上则是预批准的动作类别加上验证 agent 与硬规则("这是破坏性命令吗?它在尝试 drop table 吗?")的组合,LLM-as-a-judge 与朴素处理规则并用。错误的根因怎么办?他观察到 agent 走错方向后若发现反证,有能力自我纠正;团队正在研究让 AI SRE 同时追踪两到四个假设,而不是"拆栈重来"。staging 环境的表现近乎完美:工程师弄坏 staging,它总能精准指出"是最新部署弄坏的"。（原文锚点：`there’s a clear path to autonomy and it starts with an agent that is observe only`；`we want the AI SRE to follow like multiple hypothesis at the same time`）

### 合规问询、两条铁律与"新类型的事故"

作为德国公司,客户的合规问题从最基础的问起:用哪些端点(是否区域端点)?我的数据会被用于跨客户训练吗?他们的标准动作是永远退出模型训练,架构上的代理抽象层让模型可随时替换,欧盟客户使用区域端点;推理模型仍必须是前沿款(嘉宾口中的 Opus 与 GPT 系列新型号),客户自带 API key 加自有护栏的诉求也被支持。对"你们怎么测试"的诚实回答是"还不令人满意":录制回放式测试覆盖不了所有工具组合(录制时只用了 30 个工具中的 10 个,新版本可能用到别的),它擅长的是拦截换模型时的性能回退,理想态是在真实环境上常跑自动化测试。客服是已经落地的第二用例:当初基于向量库加应用内聊天的 RAG 方案被整体抛弃,新客服 agent 复用 AI SRE 的架构,还多了一层能力——能直接查看客户的实时配置给出针对性提示;多个 agent 组成他们所称的 workforce。（原文锚点：`we opt out of model training`；`the recording captures doesn’t capture everything`）

给 agent 建设者的建议收敛为两条。第一条:永远拥有你的上下文——"决定 agent 性能的唯一杠杆,就是什么东西进入了上下文";因此他们不用 LangChain 等框架抽象提示与角色,甚至不建议在专用 agent 里直接用现成 MCP server——"fork 它们",因为工具定义与作用域同样是上下文的一部分,必须按自己的用例调优。第二条:尽可能从推理模型的路上让开——就像雇一位资深专家,你告诉他最棘手的问题和前人踩过的坑,而不是手把手规定做法;这条甚至适用于"何时派 subagent、何时 fork、哪些工具并行"的编排决策本身(尚未百分百验证)。配套的基准测试非常实用:用同样的 MCP server 与工具复刻一个纯 Claude Code 环境,如果你的定制 agent 表现不出显著优势,"为什么要费这个劲呢?"——而且要周期性重跑。（原文锚点：`you should always own your context`；`I would recommend that you fork these MCP servers`；`benchmark it against Cloud Code`）

他最后留给同行的预警颇具远见:最难领悟的一点是,未来会出现"连人类都没经历过的新颖事故"——当大量 AI 生成的代码、其中相当部分未经人类评审就进入生产,事故的成因将是全新的类型,而非线性推理循环的不确定性又叠加其上。主持人的收束是"人工评审与测试仍然至关重要";Yildiz 同意测试与自动化的一半,对人工评审作为长期形态则持保留态:"关键路径上我们仍然重度依赖人工评审,但我相信未来会有别的方式,让我们不必那么在意生成的代码,而是用别的方法验证我们没有灾难性地破坏什么。"（原文锚点：`there will be incidents that are novel in the sense`；`we have different ways of verifying that we didn’t catastrophically break something`）

## 来源与定位

- 原始节目：[SE Radio 719: Birol Yildiz on Building an Agentic AI SRE](https://se-radio.net/2026/05/se-radio-719-birol-yildiz-on-building-an-agentic-ai-sre/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - Agent 定义与 runbook 之外的动机（`a large language model running in a reasoning loop and deciding its own trajectory`）
  - 赌注兑现：推理模型与 MCP 双双成熟、千行系统提示的弯路（`the model context protocol took off`；`more than a thousand lines`）
  - "从推理模型的路上让开"与向量库的抛弃（`get as much as possible out of the way of the reasoning model`；`the equivalent of a clot.md file`）
  - 四分钟 RCA 目标与准确性测量的困难（`we want our AI SRE to finish root cause analysis within four minutes`）
  - agentic search 的定义：老派命令行管道（`agentic search is a fancy way of just using old school terminal commands`）
  - 95% AI 生成代码与 e-bike 类比（`AI makes our job harder because we need to master a new skill`）
  - discovery/root-cause/verification 三 agent 与 subagent/fork 之辨（`a subagent has a fresh context`；`trying to give it more freedom in that sense`）
  - 语义测试：录制真实调查、LLM judge 与嵌入打分（`those semantic tests are recordings of actual investigations`）
  - 渗透测试引发的自我故障案例与大海捞针（`the vulnerability is, is a blind SSRF attack`；`finding the needle in the haystack`）
  - observe-only 起步的渐进自主与多假设并行（`there’s a clear path to autonomy and it starts with an agent that is observe only`）
  - 合规问询、区域端点与录制回放测试的边界（`we opt out of model training`；`the recording captures doesn’t capture everything`）
  - 两条铁律：拥有上下文、fork MCP server 与 Claude Code 基准（`you should always own your context`；`benchmark it against Cloud Code`）
  - AI 生成代码的新颖事故预警与收尾（`there will be incidents that are novel in the sense`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- "95% AI 生成代码""四分钟 RCA""1.85M 行/秒"类数字均为嘉宾口述的内部口径，本文未独立验证；逐字稿中提及的具体模型型号（Opus、GPT 系列）为录制时点口径。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
