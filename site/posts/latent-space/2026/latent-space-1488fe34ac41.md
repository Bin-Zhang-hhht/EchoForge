---
item_id: latent-space-1488fe34ac41
title: '英伟达的 AI 工程师：Dynamo、Brev 与"光速"文化'
date: '2026-09-14'
published_at: '2026-03-10'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://www.latent.space/p/nvidia-brev-dynamo'
source_name: 'Latent Space'
input_type: official_transcript
transcript_url: 'https://www.latent.space/p/nvidia-brev-dynamo'
summary: 'GTC 前夜专访英伟达的 Nader Khalil（Brev）与 Kyle Kranen（Dynamo）：数据中心级推理的扩展优于放大（NVLink 与 InfiniBand 差一个量级）、prefill/decode 分离、Kimi K2 的硬件协同设计、SOL"光速"文化、代理安全三选二法则，以及"给一切造 CLI"。'
tags: [AI Agent, AI 架构, 开发者工具]
---

# 英伟达的 AI 工程师：Dynamo、Brev 与"光速"文化

> 节目：[Latent Space](/podcasts/latent-space/)
>
> 节目发布：2026-03-10 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 6105 字 · 阅读约 16 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://www.latent.space/p/nvidia-brev-dynamo) · 📄 [查看官方逐字稿](https://www.latent.space/p/nvidia-brev-dynamo)

## 速读

GTC 大会前夜，Latent Space 迎来首批英伟达嘉宾：被英伟达收购的 GPU 云开发者工具 Brev 的 Nader Khalil，与数据中心级推理框架 Dynamo 的工程负责人 Kyle Kranen。这家 4.4 万亿美元的巨头"仍在像创业公司一样运转"，而两位嘉宾的工作分别回答了 AI 工程师最关心的两件事：怎么最快拿到一张 GPU，以及怎么在数据中心规模上把推理跑到又快又便宜。

最值得带走的三点：推理服务化的核心权衡是质量、成本、延迟三轴，而规模化时"扩展（scale out）胜过放大（scale up）"——单机 NVLink 约 500GB/s、跨机 InfiniBand 约 50GB/s，差一个量级，prefill/decode 分离正是为了绕开这个悬崖；Kimi K2 展示了模型-硬件-上下文三方协同设计的最新玩法——更多专家、更少注意力头加 MLA，把 128K 上下文的 KV 压进 8GB 内存；以及 agent 安全的"三选二法则"——访问文件、访问互联网、写代码执行，三者最多给两个。

## 主题正文

### Brev：把"我想要一张 A100"变成首页大字

Brev 的产品哲学简单到极致：开发者说"我要 GPU"时，真正的需求文本被埋在云控制台第三页表单的下拉框里。"为什么最大的字不是用户想要的东西？"于是 Brev 的首页就是一张张巨大的 GPU 芯片图形，点选即 SSH——那些"美丽的动画"其实只是 Figma 里画好再导出的 SVG 加一个慢速过渡函数，"手工匠代码"。公司的营销史同样随性：Logo 是个沙卡手势、扛冲浪板去 GTC 摆摊、棕榈树高过隔壁展板、投资人牵着狗招揽人气——swyx 作为 Brev 的小额投资人当年还嘀咕"为什么要为 GPU 搞这些噱头"，如今承认这体现了贯穿产品与公司的 care（`00:01:00–00:07:00`）。Brev 的价值主张一句话：让"SSH 进一张 GPU"变得毫不费力；被英伟达收购后升级为 brev.nvidia.com——"想要 GPU 就去这个 GPU 的首页"——并在内部快速扩张；Launchable 则把任意软件变成 GPU 上的"一键部署"，连 OpenClaw 这样的内部需求都由安全团队给出官方姿势："跑在 Brev 上——VM 在云端、隔离在公司网络之外"（`00:07:19–00:09:00`）。DGX Spark 的开发者体验也是同一路数：工程 VP 们讨论的第一用例是"买两台组 Kubernetes 集群"，而 Nader 进场的第一个决定是"先让你轻松 SSH 进去"——新的 NVIDIA Sync 工具与 Brev 的注册功能让你把家里的 Spark 变成"口袋大小的数据中心"，在星巴克里像用云节点一样用它（`00:11:00–00:13:00`）。

### SOL：先问物理极限，再把现实叠加回来

Nader 称在英伟达学到的最爱的一课是 Jensen 的 SOL（Speed of Light，光速）：创业时一切 existential，每个日期你都知道根因；组织变大后层级渐生，而 SOL 的做法是"先理解物理——理论极限是什么——然后告诉我为什么做不到"。买台电脑五天到货，SOL 是"我现在就去 Best Buy 拿回来"；超过 10 台才需要叠加现实。Kyle 补充了这个词的硬件出身：SOL 本指 GPU 满速无约束时程序能跑多快——训练里对应 SOL-MFU 与实际可达 MFU 的差距。它不是 Jensen 专属，一线工程师也在用；它也不是"什么都敢上"——稳定性与安全（如 Spark 注册功能的联网问题）会被作为细节层叠回讨论，CES 的结论是先上 early access 让人试用、网络加固随后补齐。Kyle 的总结很精辟：SOL 强调的是"进步是增量的"——先找到到达起跑线的最小路径，之后每个组件各有各的 SOL（`00:13:48–00:18:00`）。

### Dynamo：数据中心规模的推理引擎

Kyle 的路径从推荐系统（把 GPU 不擅长的表格/推荐负载搬上 GPU——Meta 的 DLRM、Google 的 Wide & Deep 因此受益于 HBM 的向量查找）到图神经网络，再到"Deep Learning Algorithms"组织——"怎么让与深度学习相关的东西跑得快"。他观察到英伟达的两个组织特质：一是 passion 索引——你可以直接给高层发邮件申请去做感兴趣的事（Nader：英伟达的邮件列表是"mosh pit"，60 个人随便回），动量是唯一的权威；二是"零十亿美元市场"——Jensen 愿意投资暂时没有收入的市场，只为理解它（`00:19:00–00:26:00`）。

Dynamo 的出发点是一个行业共识的破灭：vLLM、SGLang、TensorRT-LLM 这些推理引擎都以"单副本"思维设计，而规模化服务时你会撞上"放大的天花板"——单机内 NVLink 约 500GB/s（单向），跨机 InfiniBand 约 50GB/s，差一个数量级。所以必须 scale out：复制微服务、多机协同。Dynamo 是架在推理引擎之上的"数据中心级推理引擎"，把 KV 缓存的利用率、prefill/decode 分离（disaggregation）这些规模化技巧做成模块化框架（`00:26:39–00:28:00`）。三轴权衡贯穿始终：质量（够不够准）、成本（整个工作流——多轮代理——够不够便宜）、延迟（够不够快）；选型从"要什么模型、调多少次、输入序列多长、SLA 是多少"出发，在常见配置（张量并行大小等）里实验找最低成本的可行解——甚至可以选小模型加测试时扩展来逼近大模型质量（`00:33:00–00:35:00`）。

分离式推理（prefill/decode disaggregation）的原理被讲得非常清楚：传统引擎里 prefill（读入序列、生成 KV cache）与 decode（用 KV cache 逐 token 生成）在同一引擎里步进同步交替，长 prefill 会阻塞 decode 调度；而两者的资源画像完全不同——序列够长时 prefill 是计算受限（二次方量），decode 是内存受限（每步线性读取 KV）。把两个阶段拆到不同的池子里，各自独立扩缩，就同时解决了调度阻塞与异构资源的问题。极端演示：计算富余的 DGX Spark 做 prefill、Mac 做 decode；未来硬件甚至出现了 prefill 专用的加速器 Ruben CPX（`00:38:42–00:41:05`）。缩放编排由 Dynamo 的 Kubernetes 组件 Grove 承担：旧的 LeaderWorkerSet 难以表达"多机副本 + 随负载变化比例的双阶段（prefill/decode）"结构，而 prefill 与 decode 的配比本就该随工作负载漂移——查询变得超长时 prefill 压力二次方增长——Grove 既告诉你"该有几个 prefill worker、几个 decode worker"，也提供调度 API 让这个比例真实落在硬件上（`00:41:05–00:43:00`）。

### 模型-硬件-上下文协同设计与"解锁器"

当下最让 Kyle 兴奋的领域是模型/硬件/上下文的协同设计。案例是 Kimi K2（DeepSeek 风格的 MLA 架构）：他们在博客里详述了取舍——注意力计算量随头数线性增长（64 头比 32 头省一半），于是"更多专家、更少注意力头、略小的注意力维度"，用更高的专家稀疏度换注意力预算。更深一层是 KV 的负担：DeepSeek 的 MLA 把 128K 上下文的 KV 压到 8GB，而同精度的老式模型（Llama 4/5B 级）要 40–80GB（`00:43:20–00:51:00`）。Kyle 借 Leopold Aschenbrenner《Situational Awareness》的"unhobbler"（解锁器）概念统称这类发现：多 token 预测让 DeepSeek 训练更稳定，GQA/MLA 大幅削减 KV——它们不增加智能，却解锁了规模的下一阶。他自己的理论性"unhobbler"愿望清单是"局部 prefill、全局 decode"的模型：互不关联的文档各自小 chunks prefill（消解 prefill 的二次方问题），把跨文档的关联留给 decode 阶段的全局注意力。而 swyx 的反问也很现实：百万上下文两年未破，scaling 律的斜率"不太工作"，突破多半要靠新的解锁器（`00:48:00–00:52:00`）。harness 与模型的协同设计是延伸话题："harness 产出的上下文是模型的一部分"——在 harness 里训练（等价于一轮后训练）能换最好的质量，代价是通用性；Cognition 就在这么做，换工具就要" undo 别家的训练"。Bash 之所以成为"万能 harness"，正因为它是大家共用的那一个（`00:46:00–00:48:00`）。

### 代理安全三选二，与"给一切造 CLI"

Nader 开场的安全框架值得每个部署代理的团队贴在墙上：代理能做三件事——访问文件、访问互联网、写代码并执行——"你最多让它做其中两件"。文件加自定义代码就不要给互联网（那是全量漏洞面）；给了互联网与文件系统，你就必须清楚这个代理的完整能力边界，否则提示注入就是入口。这也是 Brev 对 OpenClaw 类需求的官方答案：跑在 Brev 的隔离 VM 里、在公司网络之外（`00:00:00–00:01:00`、`00:57:34–00:59:00`）。英伟达内部对 Codex 的全员推广则展示了另一面：工程 VP 下载 Cursor 问 Nader"你为什么用它"；有人写了 Outlook CLI，Nader 让 Codex 读完他全部邮件、标出升级事项、把待回邮件归档、其余归档——"如果你没收到我的回复，是因为它没归类"，他还在 500 人的邮件线程里安利了这个玩法；安全团队的姿态是"进步的"——英伟达工程师的笔记本本就少有锁死，"你被期待理解自己尝试的风险"（`00:55:00–00:58:00`）。

 Kyle 的一段历史让 build.nvidia.com 浮出水面：他当年负责模型侧的那个"试模型 + REST API"站点，一度是（现在可能仍是）英伟达最大的推理部署，新模型上线 SLA 是一天；对黑客它是免费限流的宝藏（`00:59:10–01:00:00`）。而本期最疯的预言是"给一切造 CLI"：Nader 正在重写 Brev CLI 让代理浏览并直接供应 GPU；团队在给 Slack、Workday 造 CLI 并打算开源，呼叮出现"open CLI foundation"——"编码代理之所以比通用代理有效，就是因为它有终端，终端背后是你装好的一切。现在轮到业务应用了。"Kyle 的回答则带一点考古学：CLI 与 MCP 占位相似，但预训练语料里有海量的命令行知识；"计算从终端与 shell 开始，后来我们嫌它对人类不共情，造了漂亮的 GUI——如今是 LLM 在操作这些 GUI，讽刺的是我们又对机器不共情了。把 shell 还给 LLM 吧。"（`01:05:00–01:08:00`）

### 结语：mosh pit、零十亿美元市场与"动量即权威"

这期节目的底层其实是一幅英伟达组织文化的速写：邮件是 mosh pit（重要线程会被顶起、可以 fork、可以抄送 60 人），新工具被任何人发进邮件列表就会"像野火一样蔓延"，Jensen 拿到后会说"让它全公司跑起来"； passion 被制度性索引，"任务就是老板"；零十亿美元市场被坦然投资（自动驾驶做了十年，奔驰车队才刚开始被授权上路）。Kyle 的全圆形时刻是亚马逊广告团队来讲"用 Dynamo 做生成式推荐"——"我用 LLM 取代了我五年前的工作"。对 startups 的建议藏在 Nader 的一句话里："动量是唯一的权威。起步、做出一点进展、给人看东西——这是推进任何事最有效的方式，在英伟达如此，普遍亦然。"（`00:21:00–00:26:00`）

## 来源与定位

- 原始节目：[NVIDIA's AI Engineers: Agent Inference at Planetary Scale and "Speed of Light" — Nader Khalil (Brev), Kyle Kranen (Dynamo)](https://www.latent.space/p/nvidia-brev-dynamo)
- 定位：官方逐字稿自带节选时间戳与章节时间轴，以下定位取自归档逐字稿。
  - 代理安全"三选二"法则（00:00:00–00:01:00）
  - Brev 起源、GTC 冲浪板与 SVG 动画（00:01:00–00:07:00）
  - 收购体验与 Launchable 一键部署（00:07:19–00:09:00）
  - DGX Spark、NVIDIA Sync 与"口袋数据中心"（00:11:00–00:13:00）
  - SOL 文化：物理极限优先（00:13:48–00:18:00）
  - Kyle 路径：推荐系统、GNN 与 passion 索引（00:18:42–00:23:00）
  - 零十亿美元市场与"动量即权威"（00:23:00–00:26:00）
  - Dynamo：扩展优于放大与 NVLink/InfiniBand 量级差（00:26:39–00:30:00）
  - 三轴权衡与选型流程（00:33:00–00:35:00）
  - prefill/decode 分离与计算/内存受限（00:38:42–00:41:05）
  - Grove 与 prefill/decode 配比调度（00:41:05–00:43:00）
  - Kimi K2 的三方协同设计与 MLA（00:43:20–00:47:00）
  - harness 协同设计与"训练进模型"（00:46:00–00:48:00）
  - unhobbler、MLA 的 KV 压缩与"局部 prefill/全局 decode"设想（00:48:00–00:52:00）
  - GTC 场次预告：Dynamo 教程与代理生产推理（00:52:00–00:55:00）
  - Codex 全员推广、Outlook CLI 故事与安全团队姿态（00:55:00–00:59:00）
  - build.nvidia.com、NIM 与内部推理部署史（00:59:10–01:01:00）
  - "给一切造 CLI"与终端的轮回（01:05:00–01:08:00）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 逐字稿为自动转写，专名与词形按上下文校订（如 "Rev/Bread" 当为 Brev、"Netter" 当为 Nader、"Viu/Vibhu" 为客座主持 Vibhu Sapra、"shelan/tenor TLM" 当为 SGLang/TensorRT-LLM、"Kimmy" 当为 Kimi、"LAMA three" 当为 Llama 3、"Ruben CPX" 为 Rubin CPX 的转写）；NVLink 与 InfiniBand 的带宽数字（约 500GB/s 对 50GB/s）为受访者凭记忆给出的量级，其明确提示"取决于代际"。
- 内部使用数据（Brev 增长、Codex 部署规模）与 GTC 议程信息均为受访者口径，未经独立核实；"买两台 Spark 组 K8s 集群"等内部讨论为受访者转述的玩笑语境。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
