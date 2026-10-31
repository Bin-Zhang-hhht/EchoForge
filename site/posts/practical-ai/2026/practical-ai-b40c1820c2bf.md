---
item_id: practical-ai-b40c1820c2bf
title: 'AI 进入漏洞研究后：可利用性缺口、过半可疑的 PoC 与防御者的时间窗'
date: '2026-11-01'
published_at: '2026-10-22'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: https://share.transistor.fm/s/9a42098b
source_name: 'Practical AI'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/9a42098b/transcription
summary: 'AI 已能较可靠地识别漏洞，但从验证到证明真实攻击效用仍有缺口。VulnCheck 利用开发总监 Spencer McIntyre 与主持人讨论代理化漏洞发现、开源社区过半 PoC 可疑的 2026 年转折点、守门限制与本地模型迁移，以及防御者为何要按攻击效用而非评分排定优先级。'
tags: [安全, LLM, AI Agent]
---

# AI 进入漏洞研究后：可利用性缺口、过半可疑的 PoC 与防御者的时间窗

> 节目：[Practical AI](/podcasts/practical-ai/)
>
> 节目发布：2026-10-22 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 10412 字 · 阅读约 27 分钟
>
> 标签：[安全](/tags/%E5%AE%89%E5%85%A8/) [LLM](/tags/LLM/) [AI Agent](/tags/AI%20Agent/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/9a42098b) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/9a42098b/transcription)

## 速读

AI 已经能把"找出漏洞"这一步做得越来越快，但从验证到证明真实攻击效用，缺口依然在那里。这期 Practical AI 录制于 2026 年 10 月 21 日——当天正有一条被广泛报道的安全新闻。主持人 Daniel Whitenack（Prediction Guard CEO）与 Chris Benson（AI 与自主系统研究工程师）请来 VulnCheck 漏洞利用开发总监 Spencer McIntyre，讨论 AI 如何改变漏洞发现、利用开发与 PoC 生态，以及防御者该如何消化这些信号。

最值得关注的几点：开源社区公开 PoC 里"看起来不可信"的比例在 2026 年越过一半（节目转述口径）；AI 的漏洞能力有清晰的类间边界——开源逻辑类缺陷强，闭源逆向类弱；守门规则趋严之下，研究团队正转向本地模型，并重新权衡"把哪些数据交给谁"。对安全工程师、AI 平台开发者与需要做补丁决策的团队来说，这是一期防御视角的工程讨论，不含攻击操作细节。

## 主题正文

### 先拆开标题：漏洞、利用与验证门槛

节目开场正撞上一条新闻。Daniel 说，录制当天他刚看到媒体报道里"AI 发现了影响大半个互联网的利用"的说法。Spencer 随即举起他的"纠偏牌"：在这门行业里，术语需要先拆开——漏洞是缺陷的抽象概念，是"某种坏事可能发生"的潜力；利用则是把这种潜力落地为具体实现。他补充，行业语境下的"验证"标准，几乎总是低于真实操作者（无论动机是合法测试还是别的）真正需要的可用性门槛，而行业宁可把风险估得更高、推动尽早修复，在他看来是件好事。

把这个区分套到当天的新闻上，讨论的焦点变成：AI 究竟做到了哪一步。Spencer 的观察是，多家 AI 模型在识别漏洞这一步已经做得不错——能看到代码里哪个字节被覆盖、哪个令牌在泄漏；但分析常常就停在这里。行业缺的，是从"验证过的缺陷"到"能证明真实攻击效用的可用利用"之间的那一环。没有这一环，评分的参考价值有限：他举例说，同一个周期里出现二十来条 9 分以上的漏洞时，CVSS 之类评分只能提供有限的区分度，优先级必须回到"攻击效用 × 自己的业务上下文"来判断。（原文锚点：`a vulnerability is basically the potential for something bad to happen`；`an exploit is a concrete implementation that leverages that to do so`；`This byte is overwritten`；`they seem to be doing a pretty decent job at identifying vulnerabilities`；`the actual functional exploit that proves attacker utility`；`CBSS is only gonna give you so far`）

### 突发漏洞当前：研究结论出来之前怎么决策

被问到"遇到这类新闻该怎么决策"时，Spencer 说自己经历过很多次"大漏洞刚出、所有人都在现场拆解"的场面，团队第一件事是弄清利用的约束条件——这决定它会不会真的被野外使用。他给的经验法则带着保留：从他对 React2Shell、Log4j 这类历史事件的印象出发，一个漏洞披露后拖得越久、还没被证实"被夸大"，通常越不是好兆头。就当天的 PHP 漏洞而言，他的建议是在深度研究结论公布之前就把系统打上补丁；截至录制，它"看起来没有被夸大"，但大家仍处在灰色地带。

Daniel 补充企业视角：自家技术栈不用 PHP，判断的一部分是分清哪些在自己控制内、哪些在供应商手里——比如内容管理系统可能底层用 PHP。Spencer 认同，并指出真正的长尾变量在硬件、构建与操作系统：PHP 跑在物联网设备与各类 appliance 上、跨多种架构，且按他的说法这个漏洞"据称影响追溯到 PHP 5"，意味着存在不再收补丁、甚至厂商已经倒闭的老版本。这些变量既是风险评估的难点，也是噪音的来源。（原文锚点：`what are the constraints upon exploitation`；`the longer it's been out and it hasn't been confirmed to be overhyped`；`patch your systems`；`apparently affects back to like PHP five`）

### 把 AI 接进流程：框架与语料降低了起点

Chris 问团队实际怎样把模型用起来。Spencer 的答案从工程结构开始：VulnCheck 用自家的开源 Go Exploit 框架——一个现代利用开发框架，把检查漏洞、扫描、验证目标、运行利用这些环节之间的差异做了归一化。对 LLM 来说，这意味着不必从零搭建脚手架；再加上一个每天还在增长的历史利用语料库（他说上周新增约 50 个、本周有望新增约 60 个），模型产出更好，人机之间的交互接口也更统一。框架的另一头是使用者：接口统一之后，不必再关心每个利用的细节差异。（原文锚点：`our open source Go Exploit framework`；`It normalizes how you would go through and handle the variances`；`we added, I think it was like 50 last week`）

### 类间差异：擅长开源逻辑类，吃力闭源逆向类

能力并非均匀分布。Spencer 说，LLM 在不少漏洞类别上表现"相当好"，尤其是开源 Web 应用里的逻辑类缺陷——令牌处理逻辑、表达式语言注入、文件泄露等；而一旦对象是闭源，需要先做逆向工程的固件或专有 x86 软件、要做补丁对比（patch diffing）的场景，模型就明显吃力得多。他强调"不是全部，但很多都落在这两个桶里"。

Daniel 追问：AI 发现的漏洞是否已经被更高比例、更大影响地利用？Spencer 的回答是：今天这样讲是安全的——AI 在利用的可靠性与影响上仍不及人类。人类研究者带着动机与上下文工作：他们通常清楚"攻击者能不能进来"这类问题，目标几乎总是拿到代码执行，因此人工打磨的利用对真实使用者的效用更成熟；AI 产出的很多东西停步于"一个理论上可利用的崩溃"，甚至会在推进中偏向对人类操作者没什么用的方向。（原文锚点：`LLMs seem to be pretty darn good at exploiting multiple vulnerability classes`；`it has to do like patch diffing`；`AI is not as reliable at exploiting them with the same impact as humans`；`This is a crash that's theoretically exploitable`）

### 守门规则下的研究日常：验证计划、降级建议与本地模型

谈到团队遇到的现实约束，Spencer 直言守门是真实存在的问题。团队首先走正式流程，申请进入各家供应商的网络安全验证计划，但结果不理想——并没有真正改变他们能做的事。Daniel 补充了一个他了解到的案例：OpenAI 与 Hugging Face 的一次事件里，Hugging Face 团队因为守门规则不在自己的主权控制范围内而无法处理相关日志，最终选择自托管一个 GLM 版本来做分析。

Spencer 观察到守门的整体趋势在收紧，进攻性安全研究圈里流传的建议近乎一致：如果你用的是美国专有模型，就降级使用。他还提到一个时间点上的担忧：按逐字稿记载，他说到 Opus 4.6 或 4.8 这类"相当好用"的版本将在二月前后停用，此后可能出现一道可用性上的断崖，不少团队因此在提前转向本地模型。在他看来，这类守门讨论最难的一环是证明意图——这也是威胁情报行业多年的老问题：即便完成了归因，判断动机依然困难。（原文锚点：`the formal processes with the companies to get into the cyber verification programs`；`They weren't in sovereign control of the OpenAI guardrails`；`if you're using one of the American proprietary models, it's to downgrade it`；`after those versions are gonna be sunset in February`；`is proving intent`）

### 中毒权重还是数据共享：模型信任的两个问题

Chris 从国家安全背景提出另一组张力：西方安全语境里中国模型通常不被允许；而在更大的安全圈子里，围绕中国模型"中毒权重"的担忧——无论真实还是被夸大——也在流传。研究者该如何在更严的守门与开源世界的不确定性之间权衡？

Spencer 的回答与提问的预设保持了距离。他说，身边推荐 GLM、Qwen 等开源权重模型的人很多；据他转述，Anthropic 几周前公布了对 GLM 5.3 的基准结果——这个可本地运行的模型表现约为其某些前沿模型的九成，发布才三四个月。但就"中毒权重"而言，他说从业者里还没有谁真的在担心这件事；反而有人在讨论 "abliteration"——自行编辑权重以去掉拒绝行为。他据此推断：既然研究者在检查甚至修改权重，权重里若本就嵌着问题，更容易被人发现，这与审开源代码是一个道理。他认为更紧迫的问题在托管模型：使用托管服务意味着数据全部上行，你不知道对方内部怎么处理；而研究者在手头往往是尚未披露的新漏洞，真正要回答的是"你愿意把这些信息交给谁"。很多人的答案是不想费这个心，于是干脆自托管。（原文锚点：`generally not allowed in national security context`；`they benchmarked GLM 5.3`；`I haven't actually heard of anyone expressing concern around poisoned weights`；`they're editing the weights themselves`；`a much more immediate concern would be if you're using the hosted models`；`are you comfortable sharing this information with who you're trying to get help from`）

### PoC 泛滥：2026 年的转折点

Daniel 把话题引向 VulnCheck 发布过的"假 PoC"分析，请 Spencer 解释 PoC 在这个语境里指什么。Spencer 先给定义：漏洞是理论缺陷、利用是具体实现，PoC 介于两者之间，谱系很宽——有的 PoC 只需要触发一次崩溃就能验证漏洞，也有 PoC 被完全武器化、会投递对攻击者有用的载荷。他不猜发布者的动机，只描述光谱：有人为名声，有人为学习分享，也有人就是发现者本人，用 PoC 证明自己的概念。

VulnCheck 的 initial access intelligence 有一项日常工作：按 CVE 编号在 GitHub、GitLab 等来源里复审能找到的所有公开 PoC，每天过一遍。客户关心的不只是"我们有没有"，还有"别人有没有"——同一个漏洞，其他攻击者手里可能掌握什么。他也回顾了研究分发十年来的碎片化：PoC 大量涌向 GitHub，而不是 Exploit DB、PacketStorm 这类老牌集中地；他半开玩笑补了一句——除非微软封你的号，而那种事确实会发生。

信息量最大的是他转述同事最近一次分享的内容：团队给公开 PoC 内部标注两个维度——"是否疑似 AI 生成"与"是否可用"。把 AI 维度拿掉单看可用性：随着 PoC 总量上涨，2026 年出现了一个转折点，"看起来不可信"的 PoC 平均占比越过 50%，最常见的原因是它们是坏的、跑不通，或达不到"能证明点什么"的标准。Spencer 的结论是：今天你随手找到一个 PoC，它多半不是你希望的那个能真正证明攻击效用的东西。（原文锚点：`a POC is somewhere in between`；`we review all of the POCs that we can identify by CVEs across GitHub`；`dumped onto GitHub as opposed to going to the old school`；`unless Microsoft bans your account`；`we saw a tipping point in 2026`；`tipped to over 50%`）

### AI 栈自身：旧漏洞类别的新聚集地

Daniel 问：代理 harness、模型服务框架、工作流工具这些 AI 栈新组件，有没有带来全新的漏洞类型？Spencer 先确认了问题的方向（问的是 AI 栈里的漏洞，而不是用 AI 栈做研究），然后给出的判断是：大体还是那些老问题。这些项目几乎都是解释型语言写的——它们太新；真正带远程攻击面的往往是 Web 界面、分发框架这类组件，而不是底层的 C/C++/Rust 组件。因此看到的仍是老类别：逻辑缺陷、文件读取、反序列化、账号注册与访问控制里的逻辑问题，与过去十年 OWASP Top 10 一类的历史清单高度重叠。变化不在类别，在数量：同样的问题开始成批出现。（原文锚点：`they're almost always interpreted languages`；`a lot of the same kind of vulnerability classes`；`deserialization flaws`；`we're just starting to see them more in bulk`）

### 代理化发现：模糊农场的类比与自建 harness

Chris 提到 agent swarm——按他的理解，OpenAI 那次事件在一定程度上就是用 agent 群实时找漏洞、再实时利用。Spencer 的心智模型借用自更早的"模糊测试农场"：一百个节点同时 fuzz Chrome，理论上就多找到相应数量的 bug。相似之处还有研究团队的反应：大家都在自建 harness 和提示词，逻辑与当年一样——用和别人相同的现成工具、相同的模型去测同一个热门目标，大概率找到同一批 bug，于是增加差异成了自然选择。

与 fuzzing 的相似性到此为止。Spencer 说，AI 最大的改变是拿掉了"首轮分诊"：漏洞一旦被识别，模型能直接给出一份初步分析——这是否可利用、属于什么缺陷类别、如何走到这一步——质量因你的控制与所选模型而异。（原文锚点：`find vulnerabilities in real time that are then exploited in real time`；`with fuzz farms from a long time ago`；`home brewing their own harness and their own prompts`；`it's kind of removing that first line of triage`）

### 离"全域自动利用"还有多远

对最关键的问题——大范围真实利用是否已经在发生——Spencer 的当下判断是：没有看到证据。但他紧接着给了两个限定：其一，如果三到六个月后答案不同，他一点都不会惊讶，此刻的任何判断几个月内都可能过期；其二，确定在发生的部分已经很有分量——agent 能构建 PoC 回去复现缺陷，在某些类别上能一路产出达到他们质量门槛的 PoC 乃至完全武器化的利用，但在另一些类别上还谈不上可靠。

Daniel 把讨论收拢成一种可行的分工：让 agentic 研究者做宽撒网与初筛，把候选交给人类专家去提升利用效用、验证 PoC 是否可用。Spencer 认同这个理解：把信息一路蒸馏到"已知如何触发、且大致知道它能做什么"，再与"攻击者想要什么"求交集——恰恰是某些类别卡在这最后一步。（原文锚点：`I haven't seen evidence that full on wide scale exploitation is where we're currently at`；`I would be shocked if the answer isn't different in three to six months`；`they can even build the POCs to be able to go back and re trigger the flaw`；`it will create a POC or a fully weaponized exploit that we would consider to meet our bar for quality`；`it's not quite reliably there for certain classes`；`It's boiling that information down`）

### 收尾：防御者的时间窗与等待判例的问题

被请去畅想未来时，Spencer 说自己相当乐观，理由落在速度上：攻击者不按规则行事，原本可以用不确定的时长去开发利用、再通过实际使用释放伤害，而防守方理解它的过程总是更慢；如今防守方跑完"识别—理解—产出可用信息"的速度快了很多，等于在削减攻击者从这些投入中获得的收益，新漏洞出现时的反应也更快。

他真正好奇的还有一个非技术问题。新闻里已经出现过"有人让 Claude 去办某件事，它利用了一个 SQL 注入漏洞把自己顶到健身课程队列最前面"这类报道；他想看到的是责任判例最终如何在法庭上形成——这类越界行为的责任归属，大家都有直觉，但他想看真实的裁决。（原文锚点：`attackers don't play by the rules`；`we are reducing the value that they're getting out of all that effort`；`Claude exploited a SQL injection vulnerability to bump him to the top of the queue`；`shakes out in the courts`）

## 来源与定位

- 原始节目：[Exploit Development, Agentic Vulnerability Discovery, and Fake PoCs](https://share.transistor.fm/s/9a42098b)

- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。

  - 漏洞与利用的区分、AI 识别能力与攻击效用缺口（`a vulnerability is basically the potential for something bad to happen`；`an exploit is a concrete implementation that leverages that to do so`；`This byte is overwritten`；`they seem to be doing a pretty decent job at identifying vulnerabilities`；`the actual functional exploit that proves attacker utility`；`CBSS is only gonna give you so far`）

  - 突发漏洞的优先级判断与应对（`what are the constraints upon exploitation`；`the longer it's been out and it hasn't been confirmed to be overhyped`；`patch your systems`；`apparently affects back to like PHP five`）

  - 团队将 AI 接入利用开发：Go Exploit 框架与语料（`our open source Go Exploit framework`；`It normalizes how you would go through and handle the variances`；`we added, I think it was like 50 last week`）

  - 漏洞类别上的能力差异与人机成熟度差距（`LLMs seem to be pretty darn good at exploiting multiple vulnerability classes`；`it has to do like patch diffing`；`AI is not as reliable at exploiting them with the same impact as humans`；`This is a crash that's theoretically exploitable`）

  - 守门流程、降级建议与本地模型迁移（`the formal processes with the companies to get into the cyber verification programs`；`They weren't in sovereign control of the OpenAI guardrails`；`if you're using one of the American proprietary models, it's to downgrade it`；`after those versions are gonna be sunset in February`；`is proving intent`）

  - 中毒权重担忧与托管模型的数据边界（`generally not allowed in national security context`；`they benchmarked GLM 5.3`；`I haven't actually heard of anyone expressing concern around poisoned weights`；`they're editing the weights themselves`；`a much more immediate concern would be if you're using the hosted models`；`are you comfortable sharing this information with who you're trying to get help from`）

  - PoC 谱系、日常复审与 2026 年转折点（`a POC is somewhere in between`；`we review all of the POCs that we can identify by CVEs across GitHub`；`dumped onto GitHub as opposed to going to the old school`；`unless Microsoft bans your account`；`we saw a tipping point in 2026`；`tipped to over 50%`）

  - AI 栈自身的漏洞类别（`they're almost always interpreted languages`；`a lot of the same kind of vulnerability classes`；`deserialization flaws`；`we're just starting to see them more in bulk`）

  - 代理化发现与模糊农场类比（`find vulnerabilities in real time that are then exploited in real time`；`with fuzz farms from a long time ago`；`home brewing their own harness and their own prompts`；`it's kind of removing that first line of triage`）

  - 全域利用的证据边界与人机分工（`I haven't seen evidence that full on wide scale exploitation is where we're currently at`；`I would be shocked if the answer isn't different in three to six months`；`they can even build the POCs to be able to go back and re trigger the flaw`；`it will create a POC or a fully weaponized exploit that we would consider to meet our bar for quality`；`it's not quite reliably there for certain classes`；`It's boiling that information down`）

  - 防御者的时间窗与责任判例（`attackers don't play by the rules`；`we are reducing the value that they're getting out of all that effort`；`Claude exploited a SQL injection vulnerability to bump him to the top of the queue`；`shakes out in the courts`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。

- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。

- 无法独立验证的数字仅作为节目中的观点或案例呈现。

- 逐字稿为出版方机器转写且无时间戳：公司名 VulnCheck 在稿中转写为 "Vulnerability""Vulnerability Check""VulnerCheck" 等变体，CVSS 写作 "CBSS"，OWASP Top 10 写作 "OS top 10"，部分模型与人名（如 "Quinn"）可能亦有出入；正文按通用名称或节目描述表述，原文锚点保持逐字稿原样。

- 节目中提到的模型版本、评测数字（利用语料周新增量、GLM 5.3 基准表现、可疑 PoC 占比等）均为发言人转述或估计，本文未作独立验证。

- 本文为防御视角的工程讨论整理，保留讨论的分析性质，不包含可操作的攻击指引。

- 整理模型：GLM-5.3 Flash

- AI 编辑整理，请以原始节目为准。
