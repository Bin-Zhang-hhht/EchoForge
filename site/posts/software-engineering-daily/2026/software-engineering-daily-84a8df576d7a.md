---
item_id: software-engineering-daily-84a8df576d7a
title: '确定性模拟测试：AI 编码时代的软件验证答案'
date: '2026-10-17'
published_at: '2026-10-15'
transcribed_at: '2026-10-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/software-verification-in-the-age-of-coding-agents/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1973-Transcript.txt'
summary: 'Antithesis 红队的 Carl Sverre 讲清确定性模拟测试如何探索"未知的未知"：全系统确定性化、时间线可分支回放，15 分钟复现潜伏 SQLite 十年的并发 bug，并主张 AI 编码时代应把精力从写测试转向规格与验证之网。'
tags: [开发者工具, AI Agent, 安全]
---

# 确定性模拟测试：AI 编码时代的软件验证答案

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-10-15 · 逐字稿获取：2026-10-17 · 笔记整理：2026-10-17
>
> 全文共 7966 字 · 阅读约 20 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [AI Agent](/tags/AI%20Agent/) [安全](/tags/%E5%AE%89%E5%85%A8/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/software-verification-in-the-age-of-coding-agents/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1973-Transcript.txt)

## 速读

Antithesis 是一家围绕"确定性模拟测试"（deterministic simulation testing，DST）构建的软件验证公司，本期主持人 Sean Falconer 对话红队（red team）成员、AI 战略负责人 Carl Sverre。核心问题：测试擅长确认团队预期的行为，而最致命的故障恰恰藏在没人想到的边界情况里——AI 大量生成未经人仔细审查的代码，让这些盲区越来越大。

最值得带走的三点：一是 DST 的两大要素——把被测系统确定性化、再对时间线任意分支做广度优先搜索；二是 15 分钟在通用负载下复现潜伏 SQLite 十年、仅 Tailscale 撞到过的并发 bug；三是他的核心主张——编码时间缩短时应把精力重平衡到"精确规格 + 验证之网"，因为 AI 做测试驱动开发会对测试过拟合，而针对通用属性的模拟测试"不可能被过拟合"。

## 主题正文

### 红队与"测不出未知"的结构性原因

Carl 的角色介于客户与产品之间：红队不是安全意义的红队，而是一群分布式系统专家深度掌握 Antithesis 后帮客户解决最难 bug 的团队；另有全职 FDE 团队日常驻场，红队负责制定战略并传导"乘数效应"。红队直接向产品负责人汇报而非销售线，为的是把经验沉淀回产品。Carl 本人负责 AI 方向，写了 Antithesis 的 AI skills 仓库和供 Agent 使用的 CLI 工具；同事 Lawrence 则专注属性测试库 Hegel 与 Bombadil。（原文锚点：`we named the red team after the idea that what if we hired a bunch of distributed systems experts`；`We actually report up to head of product and not in the sales org`）

为什么可靠性工具长期投入不足？Carl 用 SingleStore（旧名 MemSQL）十年的经历作答：那里的文化是每个开发者为自己写的代码写全部测试，内部测试集群 Psyduck 支持"过程化测试"——一个测试通过参数化输入空间扩展成许多测试。这让测试变成工程谜题，工程师反而愿意用。他的诊断是：大多数测试只做回归——"我实现了功能 X"然后把 X 固化为可接受行为；而真正难写、也最有乐趣的，是覆盖"未知的未知"的测试。把测试做得越像"程序化生成"，工程师就越愿意用。（原文锚点：`the more testing could feel like procedural generation, the more likely engineers would like to use it`；`we tend to write more tests in the regression space`）

### 分布式与有状态系统为什么难测

纯函数代码用单元测试就够了；但高阶软件几乎整个是有状态的——依赖此前的全部输入历史，测试时要问"如果 A 发生、接着 B、接着 C"，而 B 和 C 往往是故障。人们于是写集成测试，把一条已知事件时间线编码进去；要测不知道存在的东西，就得穷举树状的可能输入，这立刻变成组合爆炸。再加上现代软件尤其是分布式系统的状态空间大量非确定、无法被确定性模拟，SingleStore 时代的结局就是：集成测试只覆盖已知事件序列（基本是回归测试），偶尔注入故障，或做大规模随机时间线的压力测试。（原文锚点：`you end up with this sort of tree-shaped thing`；`the state space is non-deterministic`）

Sean 问 Netflix 的混沌工程是不是对"未知未知"的回应，Carl 给了肯定回答，并把它定性为"把压力测试放大到生产环境"：让系统持续经历坏天气，逼可靠性以更快速度提升——这与"把测试系统变成持续的坏天气压力测试"是同一种心智模型。他也补充 Meta、Google Cloud 等也有类似实践。（原文锚点：`They're essentially scaling up stress testing to production`）

关于 mock 保真度的常见疑问（依赖 Stripe 之类的服务无法放进模拟环境），Carl 的框架是：不必做完美模拟，只要让 mock "比真实更坏"——它的行为是生产行为的超集且全部更差，就足以用来验证软件；做一个覆盖更宽故障面的"更差 mock"往往比高保真 mock 更容易。（原文锚点：`you just need to make sure that the mock is worse than what can happen`）

### LLM 让状态空间更爆炸，DST 顺势更重要

对"被测系统开始依赖 LLM 这种非确定过程"的问题，Carl 认为这不改变测试方法论，但显著扩大了需要测试的状态空间：业务逻辑在多步流程中问 LLM 下一步做什么，后续可能性可能瞬间爆炸；极端情况是让 LLM Agent 在 Linux 沙箱里几乎为所欲为。此时下游软件必须能应对宽得多的新输入，"探索所有可能的下一步"的过程化测试——即 Antithesis 所说的确定性模拟测试——就更加重要。（原文锚点：`the potential next steps you might be able to go from that point may have just exploded`）

### DST 的两个要素：确定性 + 分支模拟

DST 的第一个要素是确定性：把被测系统放进完全受控环境。Antithesis 为 Linux 软件提供自动方案——像部署到一个 EC2 服务器一样把软件原样部署进来（Docker 容器切分也行），整个系统只会遭受 Antithesis 注入的非确定性；软件仍"看到"随机数、时间、乱序事件，但这些都能精确复现。另一条路是自己重写软件，把所有非确定性来源（时间、随机数、调度）改为注入控制；Carl 说，这种自建 DST 会给软件开发带来很高的成本。（原文锚点：`It will only suffer non-determinism that we inject`；`rolling your own DST`）

第二个要素是模拟（分支）。Antithesis 控制系统级随机数（例如 `/dev/urandom` 的读取），并建议客户不要在软件里混合熵源初始化 PRNG，而是每次都直接读系统随机——因为 DST 要在历史任意点"分支"出一条新的蝴蝶效应时间线；若用 PRNG，新分支会看到同样的随机数序列，除非重新播种。有了分支能力，就能做这样的实验：三节点分布式系统等一个节点崩溃（Raft 类系统本应能容忍），然后在崩溃后分支出一堆时间线，问"如果那个节点恰好在选主中途恢复会怎样"——从任意点分支、尝试不同事件顺序，等于对软件状态空间做广度优先搜索。（原文锚点：`we can branch at a much more fine-grained point`；`breadth-first search the state space of your software`）

### 借鉴 fuzzing：覆盖引导的自主探索与 SQLite 案例

如何决定往哪里探索？Carl 说这借鉴了 fuzzing 研究里的覆盖引导策略：监控被测代码走了哪些分支，随机输入触发新分支序列就记入地图，在紧循环里反复迭代，从而在不读源码内部逻辑的情况下积累对系统的认知。Antithesis 把这套策略用于 DST，并加上时间线分支：当发现某区域分支路径变化很快（典型是多线程锁与共享内存交互），会自动派出大量自主搜索者从那段高竞争代码的起点展开。（原文锚点：`we're going to monitor all of the branches that the coder under test is taking`）

今年 SQLite 的 WAL 重置 bug 是完美例证：该 bug 潜伏十年、自最早的 write-ahead log 代码起就存在，窗口极窄——一个线程读共享内存后睡眠，另一线程改了数据，它醒来却没做正确的再校验。据 Carl 所说只有 Tailscale 这一个大客户撞上过，Tailscale 今年做了大量研究、发布结论后才修复。Carl 把修复前的最后一个版本放进 Antithesis，用一个只跑插入和 WAL checkpoint 循环的简单负载，15 分钟就找到了这个 bug，并收窄到确切的操作顺序；随后他又写了一个对所有 SQLite 操作等概率的通用负载，同样 15 分钟复现。他坦承第一步的负载确实带了"先验"（他知道 bug 在哪、刻意锻炼相关代码），但通用负载的结果说明这并非必要。（原文锚点：`it happened to be Tailscale`；`And that still found the bug in like 15 minutes`）

### 可观测性、属性与多宇宙调试

黑盒之外，平台给用户四样东西。一是严格串行化的日志：因为执行顺序完全受控，日志里看到的事件顺序就是模拟中的真实顺序，传统分布式系统"两个事件谁先谁后"的猜测不再需要。二是属性（properties）：用户声明系统应满足的性质，Carl 测 SQLite 用的就是一条——在模拟中随机时点运行 `PRAGMA integrity_check`，一旦发现损坏就自动向该区域集中 fuzzing 精力。三是多宇宙调试（multiverse debugging）：可以 SSH 进模拟的任意时刻，比如损坏在 30 秒时被发现，就回到此前对时间线做二分搜索，用 GDB 定位。四是因果分析（causality analysis）：平台替你自动做这件事——回溯、扰动环境、重放，找出 bug 是在哪一刻被"锁定"进模拟的。（原文锚点：`the logs are strictly serialized with the exact order of operations`；`The fourth tool that we have is called causality analysis`）

### 与编译期验证、形式化方法的关系

Sean 提到 AWS 的 Hydro 项目（Joe Hellerstein 曾来节目）想用类型系统在编译期阻止某些分布式 bug。Carl 表示自己不深入了解 Hydro、无法评价其取舍，但给出一般性判断：这类方法与 DST 并不对立——纯 Rust 已能靠类型系统消除整类内存 bug，防线越多越好；不过此类系统常要求按特定方式写代码，更像静态验证的高级形态，可能更适合可以从零设计代码结构的 greenfield 项目。自建 DST 和这类编译期手段一样，长期给软件开发带来很高的"税"。他的结论：值得搞清楚 Hydro 能检查哪些类别、哪些仍是未知未知，而"在之上再放一层 Antithesis"仍然有价值。形式化方法则是另一套取舍：为系统建一个抽象模型并证明其正确性。（原文锚点：`it may not be that intuitive how to express like your problem in that way`；`involves a very high tax on the software development effort`）

### 测试栈怎么摆：贴近集成与压力测试一端

在整体测试栈里，DST 更靠近集成测试与压力测试的世界。单元测试仍然该用——验证小块独立代码最快；"能负担得起的测试类型都用上"总体上会带来更好的代码质量。DST 的独特价值在未知未知空间：一个测试写一次，就能覆盖软件几乎整个状态空间——理论上可达每一种可能发生的坏事件顺序。这对分布式系统适用，甚至一个"数据库 + 水平扩展的 Web 服务器 + 缓存 + 客户端"的普通 CRUD 应用也算分布式系统：客户端写到 A 节点、因故缓存未刷库、再从 B 节点读到旧值然后失败——这类故障的所有变体和顺序很难在普通集成测试里表达，用模拟测试反而更自然。Sean 补充：今天几乎所有系统都是分布式的，不只在规模化时。（原文锚点：`you can basically write that test once, and you can test almost the entire state space of your software`）

### ADD：为什么模拟测试不会被 AI 过拟合

Carl 正在教 AI 为任意软件编写运行在 Antithesis 上的负载，由此发现一个关键差异：AI 做测试驱动开发（TDD）会过度聚焦于给定的目标——Sean 一语点破"你基本上是对测试过拟合了"。而如果换成"Antithesis 驱动开发"（ADD），则不可能过拟合：Antithesis 的设计就是找反例，你写的不是具体路径上的测试，而是"数据库永不损坏"这类通用属性——要满足它只能用最通用、最正确的方式实现代码。（原文锚点：`Because Antithesis is designed to find counter-examples to whatever you give it`）

成本与迭代速度是现实问题。答案是一条"置信度传播波"：单个 PR 上跑 15 分钟（默认并行度 48，且模拟会快进代码里的 sleep——工作流引擎、作业系统类代码加速可达千倍，常见至少 48 倍，15 分钟能测数小时甚至更久的模拟时间）；主集成分支跑指数级更长的测试——"昨天发布的代码已跑完 12 小时过夜压力测试，模拟了三个月的系统时间"。他们也刚开放了让 Agent 启动运行并订阅特定失败属性的能力：运行前五分钟内属性失败，Agent 立即收到通知开始调试，无需等整个运行结束。（原文锚点：`which simulated three months worth of time in Antithesis`）

### 规格与验证之网：AI 时代的工程重心

Sean 观察到，AI 生成代码的问题不在于代码天然更差，而在于人不再逐行理解它，责任因此转移到测试与验证，愿意投入的时间和算力也随之改变。Carl 完全同意，并给出方向：编码时间缩短时，应把精力重平衡到验证与规格——未来的工程角色是"非常非常精确地写规格"，Markdown 文档未必够用；验证则应与规格挂钩，不是聚焦单条路径，而是一张"所有可能路径都符合规格"的网。Antithesis 的故事线是：从规格导出代码应有的属性与不变量，编码进负载，负载就成了"任何路径都必然到达合法属性结果、永不出现反例"的网，Agent 只需在这张网内安全地写代码。（原文锚点：`we basically should be rebalancing that effort into verification and specification`）

收尾时他抛出一个更远的推想：如果 AI 生成代码的能力强到一定程度，软件工程可能从迭代过程变成类似图像扩散模型的过程——改规格，重新"扩散"整个代码库，只要通过那张巨大的状态空间验证网，就直接把全新代码库作为新版本发布。他表示很期待看到这一天的演进，并认为 Antithesis 是这个问题验证侧的一个好答案。（原文锚点：`from an iterative process to almost like a diffusion process`）

## 来源与定位

- 原始节目：[Software Verification in the Age of Coding Agents](https://softwareengineeringdaily.com/podcasts/software-verification-in-the-age-of-coding-agents/)
- 定位：归档官方逐字稿为无时间戳的纯文本（出版方原文含 [H:MM:SS] 标记，归档按无时间戳存储），以下为可在全文中搜索的原文短语。
  - 红队定位与 AI 战略职责（原文锚点：`we named the red team after the idea that what if we hired a bunch of distributed systems experts`）
  - 红队向产品线汇报（原文锚点：`we actually report up to head of product and not in the sales org`）
  - 过程化测试与回归测试之辨（原文锚点：`the more testing could feel like procedural generation, the more likely engineers would like to use it`）
  - 集成测试的组合爆炸（原文锚点：`you end up with this sort of tree-shaped thing`）
  - 混沌工程与持续坏天气（原文锚点：`They're essentially scaling up stress testing to production`）
  - mock 保真度："比真实更坏"原则（原文锚点：`you just need to make sure that the mock is worse than what can happen`）
  - LLM 扩大状态空间（原文锚点：`the potential next steps you might be able to go from that point may have just exploded`）
  - DST 确定性要素与注入式非确定性（原文锚点：`It will only suffer non-determinism that we inject`）
  - 分支模拟与 PRNG 建议（原文锚点：`we can branch at a much more fine-grained point`）
  - 广度优先搜索状态空间（原文锚点：`breadth-first search the state space of your software`）
  - 覆盖引导 fuzzing（原文锚点：`we're going to monitor all of the branches that the coder under test is taking`）
  - SQLite WAL bug 与 Tailscale（原文锚点：`it happened to be Tailscale`）
  - 通用负载 15 分钟复现（原文锚点：`And that still found the bug in like 15 minutes`）
  - 严格串行化日志（原文锚点：`the logs are strictly serialized with the exact order of operations`）
  - 多宇宙调试与因果分析（原文锚点：`The fourth tool that we have is called causality analysis`）
  - 编译期验证与自建 DST 的高成本（原文锚点：`involves a very high tax on the software development effort`）
  - 一次测试覆盖整个状态空间（原文锚点：`you can basically write that test once, and you can test almost the entire state space of your software`）
  - 单进程内的分布式系统（原文锚点：`Even inside a single process`）
  - ADD 与不可过拟合（原文锚点：`Because Antithesis is designed to find counter-examples to whatever you give it`）
  - 12 小时过夜测试模拟三个月（原文锚点：`which simulated three months worth of time in Antithesis`）
  - 重平衡到验证与规格（原文锚点：`we basically should be rebalancing that effort into verification and specification`）
  - 扩散式软件工程的推想（原文锚点：`from an iterative process to almost like a diffusion process`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语；出版方原文中的 [H:MM:SS] 标记未在归档中保留，正文不引用推算时间。
- 无法独立验证的数字与案例（SQLite bug 细节、加速倍数、并行度等）仅作为受访者口径呈现；本期主持人为 Sean Falconer。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
