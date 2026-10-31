---
item_id: practical-ai-2fb48cf99dc3
title: 中西部 AI 峰会三讲：可靠工作流、一线共创与智能体自主度选择
date: '2026-11-01'
published_at: '2026-10-29'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: 'https://share.transistor.fm/s/37a0c3e9'
source_name: 'Practical AI'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/37a0c3e9/transcription'
summary: 'Daniel Whitenack 精选中西部 AI 峰会三段演讲：Heidi Porter 讲用对的机制加护栏、评估与可观测性构建可靠 AI 工作流；Kevin Solorio 讲与一线蓝领工人共同构建而非替其构建以赢得采纳；SEP 的 Chris Shinkle 与 Andrew Dunlap 以六项约束与四种模式帮团队选择合适的智能体自主度。'
tags: [AI Agent, 企业 AI, 评估, 组织转型]
---

# 中西部 AI 峰会三讲：可靠工作流、一线共创与智能体自主度选择

> 节目：[Practical AI](/podcasts/practical-ai/)
>
> 节目发布：2026-10-29 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 14551 字 · 阅读约 37 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [评估](/tags/%E8%AF%84%E4%BC%B0/) [组织转型](/tags/%E7%BB%84%E7%BB%87%E8%BD%AC%E5%9E%8B/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/37a0c3e9) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/37a0c3e9/transcription)

## 速读

本期是 Practical AI 的特辑：主持人 Daniel Whitenack 担任第二届中西部 AI 峰会（Midwest AI Summit）的主持，并经大会组织方同意，精选了三段大会演讲。Heidi Porter（Moyer Group AI）讲如何构建持久可靠的 AI 增强工作流：把每个任务交给对的机制，再用护栏、评估与可观测性兜底；Kevin Solorio（Focus）讲为什么与一线蓝领工人「一起构建」而不是「替他们构建」，才换来采纳与信任；SEP 的 Chris Shinkle 与 Andrew Dunlap 用六项约束与四种模式帮软件团队选择合适的智能体自主度，而不是盲目奔向「黑暗工厂」。适合正在把 AI 与智能体推进生产的工程师、团队负责人与企业 AI 团队。

## 主题正文

### 特辑与讲者：一场峰会的三个切面

Daniel 在开场说明，他受邀担任本届峰会主持，峰会上大家围绕 AI 代理、决策模型与 AI 安全等主题做了非常务实的交流；经大会组织方同意，本期节目放出几位讲者的演讲节选，包括 Moyer Group AI 的 Heidi Porter、SEP 的 Chris Shinkle 与 Andrew Dunlap，以及 Focus 的 staff software engineer Kevin Solorio。（原文锚点：`the emcee at this year's second annual Midwest AI Summit`；`a selection of a few snippets from speakers at the Midwest AI Summit`）三段演讲分别覆盖工作流设计、一线采纳与团队协作方式，恰好构成「把 AI 用起来」的三个层面。

### Heidi Porter：失败的不是模型，是给 LLM 派错了任务

Heidi 开场先做举手调查：多少人的 AI 试点没能走过 demo 阶段、或在进入生产时停滞——台下举手不少。她的归因很直接：失败通常不是模型的问题，而是 LLM 被要求做得太多——让它持有数据、充当系统记录、做决定，还要检查自己的工作。她希望听众带走的问题是：审视工作流中的每个任务，为它选择对的机制，并想清楚如何评估正确答案、如何在出错时发现。（原文锚点：`It's because the LM was asked to do too much`；`be the system of record`）

谈工作流之前先谈数据。她的判断是：数据为你任务与工作流的可靠性设定上限；问题不是数据「好不好」，而是「对手头这个任务够不够好」。数据陈旧时系统可能不报错，只是安静地给出错误答案。当 LLM 参与流程时，需要在运行时用数据锚定它：通过查询数据库或知识图谱取回事实，让证据驱动答案，并附上可核查的引用来源；数据本身的质量会被下游全部继承，所以要优先修数据。（原文锚点：`It sets the ceiling on how reliable your tasks and workflows can be`；`you need to ground it in your data at runtime`；`letting the evidence drive the answer`）

### 机制、护栏、评估、可观测性

整场演讲浓缩为四个词。机制：实际执行某一步的东西——规则、经典机器学习、决策模型或 LLM；LLM 的用法范围很大，从直接查询、生成、调用工具，到 agentic 架构或配合人工评审，关键是按任务选择，而不是按项目一刀切。护栏：围绕每个输出的运行时控制，可以拦截问题、升级给人、约束答案，或在问题漏出后恢复。评估：可重复的测试，决定你拿到的答案是否正确；她特别提醒不要只看平均值，因为平均值会掩盖坏结果——你必须知道最坏有多坏才能修。可观测性：恢复、重放，在事故发生前捕捉漂移。（原文锚点：`four words we'll use for the rest of the talk`；`you pick that step per task, not per project`；`averages can hide a bad result`）

对每个任务有三个决策：什么来执行这一步；工作如何协调（步骤明确就用程序写死的固定工作流，决策点可以交给 LLM 或决策模型分支，或用受成本、时间约束的 agentic 架构）；什么被允许执行。第三个是一个刻度：后果重大且不确定的动作由人批准；高批量、置信度混杂的让系统超过置信阈值才行动、其余升级给人；时间敏感的先行动、给人一个否决或撤销的窗口；只有撤销起来足够廉价的动作才直接自动化。无论先选什么，都把它当假设来测试。（原文锚点：`automate outright only what is cheap to undo`）

她强调：写在提示词里的规则不会被确定性执行；护栏是真实的机器——一道门、一次检查、一个人、代码里的限制。护栏要随机制缩放：传统编程同样需要护栏（变更控制、别把 bug 推进代码）；人工评审也会失效——面对成千上万条待审项，评审者会出现盖章疲劳，这不再是有效的护栏。还有一栏常被忽略：恢复（recover）。总会有东西漏过去，恢复就是把它包住、回到安全状态：回滚、撤回输出、撤销写入；因此尽量让动作可逆，不可逆的动作要求事先批准，并当心人类疲劳。评估则守在所有这些之上：评估告诉你系统是否在工作，也是通往更多自主性的闸门——评估不工作就不要升级到生产。（原文锚点：`a rule written in a prompt is not deterministically enforced`；`rubber stamping fatigue`；`make actions reversible where you can`）

### 三个跑起来的工作流

第一个案例是一项发表过的同行评议研究（不是厂商营销）：橡胶软管产线。摄像头监视产线，一个改造过的 YOLO（you only look once）视觉模型负责找缺陷——这一步没有 LLM。检出缺陷后触发诊断：系统从知识图谱取证据，搜索相关 SOP 与维护历史；LLM 只拿到来自系统记录的证据（不是整个知识库），起草候选解释与纠正措施；随后用基于规则的检查验证草稿是否越出所引证据的范围，证据支持不足就送人工。两条护栏叠加之外，操作员可以对任何案例接受、否决或评论，而不只是被升级的那些。结果良好但不完美——锚定仍需检查；团队监控了 52 周以确认系统正常。她的总结：他们没有让 LLM 看着软管搞定一切——LLM 负责解释，检查与护栏在旁边。（原文锚点：`a peer reviewed study of a rubber hose production line`；`a modified you only look once vision model finds the defects`；`they monitored this for fifty two weeks`）

第二个案例来自种子公司 Syngenta 的 Cropwise AI：农民有时会为田地选错种子，销售或种植者把方案带到现场，基于当地条件做种子选择。LLM 解释自然语言提问（她认为是 LLM 的好用法例）；在任何处理之前，用户先由 AWS 的身份服务完成授权——这在应用代码里，不在 LLM 里；随后 Bedrock agent 把请求路由到知识库、API、Python 动作与数据代理，拉取天气、土壤、产品与农艺数据；当问题需要预测时，由 Syngenta 现有的种子与农艺模型产出——「LLM 不做农艺」。LLM 的第二个职责是用平实语言解释结果，最终由销售代表或种植者做决定。架构图上蓝色是 LLM 与代理工作的地方，灰色是规则与机器学习，黄色是护栏：LLM 是界面、路由器和解释者，不是农学家。这条架构还带来一个被验证的好处：换模型、甚至换知识库或其他数据源，系统都能存活——当然换完要重新评估。评估做法是从真实销售代表那里收集 100 对问答，由人工评审打分，并用 LLM 担任裁判（逐字稿作 “LMS judge”，疑为 LLM as judge 的转写误差）。她的 takeaway：把模型和知识库设计成系统里最容易替换的部分。（原文锚点：`the user is authorized by the identity service in AWS`；`The LLM does not do agronomy`；`the LM is the interface, the router, and the explainer, not the agronomist`；`a 100 question and answer pairs from actual sales rep`；`design so the model and knowledge bases are the easiest part of the system to replace`）

第三个来自医疗：斯坦福医疗（Stanford Health Care）的 Surgical Co Management Navigator，筛查次日择期手术患者中谁需要手术共管（co management，指临床医生在术前、术中、术后共同承担患者照护职责）。上线之前，常规人工分诊漏掉了一半符合条件的患者。新系统从电子病历拉取术前麻醉记录与用药清单；判定标准是机构自有的 rubric——从他们自己的文献与教师专长写成，固定在提示词里。提示词可读但不是执行，而这里 LLM 的唯一职责就是套用 rubric，回答 yes、maybe 或 no，没有发挥空间。与橡胶产线一样，每个病例无论是否被标记都出现在 EHR 列表里，医生可以确认、拒绝或否决：决定权留在临床医生手里。上线前他们把五个 LLM 与共识病历评审（consensus chart review）对标，选中了性能有竞争力、成本更低的一个（逐字稿作 “o three minutei”，疑为 o3-mini 的转写误差）——模型同样是系统里可替换的部分，而不是中心。对假阴性案例的分析（她强调是小样本）显示 LLM 自身错误极少，反而暴露了流程里其他环节的错误并得以修复，LLM 的错误也在同步排查。三条教训都关于谁拥有协议：机构拥有标准；比较候选模型；检查系统为何不同意。系统按设计倾向于过度标记（偏假阳性）；当系统给出否定答案时，医生 97% 表示同意；被标记的病例中医生拒绝约十分之四，理由是复杂度不够。（原文锚点：`routine human triage missed half of eligible patients`；`a rubric that the institution owns`；`benchmarked five different LMs against consensus chart review`；`it performed competitively at a lower cost`；`there were a minimal amount of LLM errors`；`the physicians agreed 97% of the time`；`physicians declined about four in 10 flagged patients`）

收束回四个词：每一步是否用了最简单可用的东西（Syngenta 用的是农艺模型）；护栏（橡胶产线在证据薄弱时扣下答案并升级给人）；评估（斯坦福对标五个模型、Syngenta 用 100 个真实问题测试）；可观测性（橡胶产线观察了 52 周）。四个问题都能回答「是」，你拥有的就是一个大概率能在 demo 之后继续工作的系统。（原文锚点：`a system that most likely keeps working after the demo`）

### Kevin Solorio：与一线工人一起构建，而不是替他们构建

Kevin Solorio 是 Focus 的 staff software engineer，主要用 LangChain 系工具为客户构建定制代理。他的分享来自一个近期客户项目：CEO 开场就说「采纳是关键」——无论做出什么，采纳必须最先发生；而这款应用的用户是蓝领工人，CEO 直言他们出了名地难以采纳新技术：不信任、不喜欢、看不见、不想要。（原文锚点：`adoption is key`；`notoriously slow to adopt new technology`）

回看工具失败的原因，症状有三类：「它不好用」（很含糊——拆开是慢、崩溃、不满足需求；工具可能做了它该做的，却没做用户需要的）；「帮不上他们」（技术由管理层几层之上采纳，解决别的问题或为了追踪指标，与日常工作无关，反而添活——人们只好下班前补录，重要信息已忘掉一半）；「繁琐」（要跨三四个系统取数再录入这个系统）。这些都是「替某人构建」（built for）的症状：需求研究不足、没深入用例、不是为他们而建。（原文锚点：`if the tool is cumbersome to use`；`It was not built for them`）

「为」构建总要经过代理：产品经理转述用户对话时会加入自己的解释，可能简化、遗漏关键用例；这还会发出「我知道什么对你最好」的信号，并把只在理论上成立的 SOP 固化下来。对比「与」构建（built with）：从目标出发，先讲清要解决什么问题；让用户进房间、跨竖井共享信息，建立尊重与信任。他的案例是为现场技师做应用——这些技师从修绞肉机到修 ATM 都干，今天派去修绞肉机的可能就是明天派去修 ATM 的同一个人，知识面之宽是工程师不具备的；AI 代理总会生成一个答案，但对不对他没底，必须依靠技师来纠正错误。（原文锚点：`field technicians that were repairing equipment from meat grinders to ATMs`；`lean on them to help correct me where I'm wrong`）

前 AI 时代这样做靠纸面原型与白板画图，定义什么信息在什么时间、以什么保真度呈现，以及有没有退路和下钻细节的通道。代理时代布局不再是重点（到处是聊天框），目标变成行为的正确：正确的时机调用正确的工具、用正确的护栏、尊重边界。评估正好提供这个场景。他给出一个自认大胆的说法：没有评估的代理只是概念验证（proof of concept）——这与部署在什么基础设施上无关；没有评估，就无法确认代理的行为符合预期。（原文锚点：`calling the right tools at the right time`；`an agent without evals is a proof of concept`）

与蓝领工人协作的特殊性在于：他们没有数字痕迹——没有邮件列表、没有 traces，白领协作里惯用的远程分析法行不通，必须把人拉进房间。他的做法是先合成一个数据集，把东西快速搭起来交到用户手里——第一版注定不对，还要主动展示错误：人们也许很难直接说出想要什么，但看到错误的东西时会飞快告诉你哪里不对。他导师的忠告是「与问题结合，而不是与方案结合」（逐字稿作 “Mary, the problem, not the solution”，疑为 Marry 的转写误差）——别因为方案是自己提的就放不下，收到反馈就迭代。（原文锚点：`with blue collar workers, there's not that trail`；`they are very quick to tell you where it is incorrect`；`Mary, the problem, not the solution`）

反馈要尽量便宜：要标注的数据集就给他们一个 Google spreadsheet，让他们按自己的时间标注；有时间就 vibe code 一个好玩的小应用，把它游戏化。之后扩大圈子——最初少数代表性用户看不到所有用例，要邀请更多人上平台。他强调建立数据飞轮：离线数据集用于开发与度量；部署后在线评估器持续对 trace 抽样打分，可以是确定性的代码评估器，也可以是 LLM 裁判（逐字稿作 “element as judge”）；未被覆盖的案例进入 annotation queue，复查发现哪里出错后回流到离线数据集——数据集随用例持续演化。准备好后发布，但保持循环运转：初始发现、首轮 beta、扩大范围都会冒出没预料到的案例。（原文锚点：`give them a Google spreadsheet`；`you create an offline dataset`；`added to an annotation queue`；`a constantly flowing dataset that is evolving with the use cases`；`keep the loop running`）

参与构建的人会成为拥护者：他借用 IKEA 效应——人们对自己亲手参与做出来的东西赋予更高价值，会觉得「这工具我参与了、我让它更好了」，进而成为工具的拥护者。蓝领工人尤其是手艺人（craftspeople），他们想看到你尊重他们、你自己也有手艺。评估数据集通常高度精选——不是百万级，而是足以覆盖用例、覆盖你期望代理做的一切；要深入细节，理解这个案例与那个案例为什么不同；花时间理解他们的流程，再回来展示系统理解了它；还要经常回访展示改进——「我听到了、我改了、继续」。这些累积成工程师与一线团队之间稳固的信任。（原文锚点：`if you've ever heard of that IKEA effect`；`they're craftspeople`；`These evaluation data sets are typically very curated`；`show it improving`）

### SEP：不是每个团队都需要黑暗工厂

第三段演讲来自 SEP 的 Chris Shinkle（创新总监）与 Andrew Dunlap（资深 AI 工程师）。Chris 开场描述了流行的「黑暗工厂」demo：手离开键盘，代理写代码、评审代码、评审代理、测试代码、发布代码——有些确实令人印象深刻，也适用于某些场景；但组织里总有人看过 demo 后来问：我们什么时候也这么干？（原文锚点：`agents writing all the code`；`when do we turn off the lights and kick up the dark factory`）

他们想留下两样东西：一个帮团队理解「该如何与 AI 协作」的 sense-making framework（心理模型），和一组上手原则。研究侧，他们引用三份较新的研究（最老的是 2025 年那份——逐字稿作 “2025 door report”，疑为 DORA 报告的转写误差），结论一致：AI 不会修复你的团队，它放大已有的东西。SEP 为「错不起」的公司造软件——医疗、制药、航空航天等受监管行业；他们不认为每个团队都需要黑暗工厂，也不必走到那一步才能获得显著的生产力收益；相反，在错误的模式下强行推进，最好的团队也会觉得处处别扭。错配的信号听起来很熟悉：「我们发布的都是 AI slop，没人知道对的什么样」；「我们应该更多地用 AI」；「快乐全没了，整天就是评审代码」。工作方式与情境不匹配时，更多的 AI 解决不了——more AI won't fix the AI fit。（原文锚点：`a sense making framework`；`The 2025 door report is the oldest`；`It amplifies what's already there`；`every team needs a dark factory`；`shipping AI slop and nobody knows what right looks like`；`fix the AI fit`）

Andrew 用三个客户团队展开。第一个是一家输电运营商（transmission operator）：遗留系统里有一批做格式转换的仿真模型，一位工程师想到用手里的一堆代理逆向出中间的过程，两天后就有了能跑的原型；但要把它推上生产时，团队进场一周却没有交付任何软件——新的约束在起作用。他们总结了六个约束：token 预算（组织全面拥抱 AI，但一天 10 美元、100 美元、1000 美元还是 1 万美元的 token 开销会改变对话）；组织准备度（有没有愿意背书这项工作的人）；目标定义（是试验还是上线）；领域知识（多少写下来了、多少在人脑子里——对代理能走多远影响很大）；可验证性（能否自动化验证、是否需要领域专家）；代码监督（受监管行业的大头——需要人盯着代码就会改变与代理的交互方式）。（原文锚点：`Two days later, lo and behold, he has a working prototype`；`We haven't delivered any software yet`；`there's six constraints that we found`；`a big one for regulated industries`）

回到原型案例的约束解剖：组织层面有 token 预算约束；团队预算只够开发者几天就把 token 用完；产品层面太多领域知识只在人脑子里——不问人就得不到正确答案；验证上，原型一个人就能验证，扩到生产是百万级输入参数，没有办法扩展验证每个输出。这些约束是旋钮：有的（如 token 预算）团队说了不算，但指认约束会触发组织层面的对话；领域知识约束改变的是谁需要参与进来——需要领域专家补充信息到代理能自动化的程度。（原文锚点：`the devs ran out of tokens`；`millions of input parameters`）

约束决定模式。他们观察到四种模式，按代理自主度从左到右排布：最左是 individual（人在环、各干各的），最右是黑暗工厂（人走了、灯关了、机器人当家，完全自主）。原型团队处于 individual agentic coding mode——只为出原型、不必担心扩展、一个人就能验证；一旦扩展，这种模式就失配、产生摩擦。（原文锚点：`there's four modes that we commonly find our teams operating in`；`individual agentic coding mode`）

第二个团队是 Andrew 自己的：为一家建筑构件制造商写设计软件——失败成本高，「楼不能塌」。他们从 individual 走向 shared，办法是建一个共享信息体：领域元素、架构、工作流、实现规则、代码、计划，全在一个所有人都可访问的知识体里；开发者日常仍各自与代理结对，但共享同样的领域规则，于是可以给代理更多自主度。可验证性在这里权重很高——建筑不能倒，所以他们不舒服就不往前走：这是一个选择，也是好适配。（原文锚点：`we had to build a shared pile of information`；`buildings falling down`；`This was a good fit for us`）

第三个团队为本地信用合作社 Forum 的移动银行应用做 C# 到 iOS/Android 原生的迁移：要求齐备、组织背书、token 随便花。构建的形态里个体消失了：团队加代理工作流，代理开始分担角色、与编排器对话，团队提供意图与上下文；更高的自主度反映为项目工作量六倍的下降。（原文锚点：`Spend all the money you want`；`a six x reduction of effort for the project`）

那么目标是从 individual 一路走到黑暗工厂吗？Andrew 的回答是不必然：目标是 fit——约束导出模式，模式即适配；约束多的领域就待在更 individual 的模式（比如每行代码都要对、或根本没有网络），识别约束、选出最适合你的模式才是正事。（原文锚点：`the goal here is fit`；`picking the mode that best operates for you`）

Chris 从精益（Lean）给出理论收束：没有单一蓝图；Toyota 从未命令所有人挂 Andon 绳（产线边任何人都可拉停产线的绳子），这背后是「把质量内建」（build quality in）的原则——别等到最后检验，发现问题时立刻停下修好；但 Toyota 并没有在所有工厂每条线都装 Andon 绳——按约束来装；原则放之四海皆准，实践因约束而异。（原文锚点：`Toyota never told anyone to hang an Andon cord`；`are true everywhere. The practices aren't`）

最后是五条原则：共享基础设施（把知识拉进代码库让人人可访问）；有意的迭代（每周排一个专门时间段来谈，否则不会改善）；让它安全——先验证后提速（verification before velocity，规模与约束变了就先确认答案对了再快）；系统性追瓶颈（review 会成为卡点，把它做成不是瓶颈后瓶颈会转移到别处，继续追——放大效应会让瓶颈比以前更痛）；去除苦活（把重复发生的事脚本化，把思考留给人类、把分析过程留给 LLM——省 token、更快、团队更舒服）。五条原则，三个团队：同样的原则，不同的模式，不同的实践。（原文锚点：`we're gonna start with the foundation, shared infrastructure`；`Until you schedule a block of time in the week`；`verification before velocity`；`you need to make it not a bottleneck`；`Save the thinking for the humans`；`Five principles. Three teams, same principles, different modes, different practices`）

### 三段演讲的共同底线

三位讲者从不同层面给出同一判断：LLM 最稳的位置是解释、路由、起草与界面，而不是数据库、农学家或最终决定者；评估是把 demo 与工作系统分开的那条线——Heidi 警告平均值会掩盖坏结果，Kevin 说无评估即概念验证，SEP 把可验证性列为约束，说的是同一件事；而信任与适配不是宣传出来的，是靠尊重数据上限、尊重一线经验、尊重团队约束一点点换来的。（原文锚点：`It's not because the model was the problem`；`you cannot confirm for sure that the agent is behaving as expected`；`Do you need subject matter experts`）

## 来源与定位

- 原始节目：[Abundant Intelligence at the Midwest AI Summit](https://share.transistor.fm/s/37a0c3e9)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 节目形态与讲者介绍（`the emcee at this year's second annual Midwest AI Summit`；`a selection of a few snippets from speakers at the Midwest AI Summit`）
  - 试点失败归因与数据上限（`It's not because the model was the problem`；`It's because the LM was asked to do too much`；`be the system of record`；`It sets the ceiling on how reliable your tasks and workflows can be`；`you need to ground it in your data at runtime`；`letting the evidence drive the answer`）
  - 机制、护栏、评估、可观测性框架（`four words we'll use for the rest of the talk`；`you pick that step per task, not per project`；`averages can hide a bad result`；`a rule written in a prompt is not deterministically enforced`）
  - 执行刻度、评审疲劳与恢复（`automate outright only what is cheap to undo`；`rubber stamping fatigue`；`make actions reversible where you can`）
  - 橡胶软管产线同行评议案例（`a peer reviewed study of a rubber hose production line`；`a modified you only look once vision model finds the defects`；`they monitored this for fifty two weeks`）
  - Syngenta Cropwise AI 种子选择案例（`the user is authorized by the identity service in AWS`；`The LLM does not do agronomy`；`the LM is the interface, the router, and the explainer, not the agronomist`；`a 100 question and answer pairs from actual sales rep`；`design so the model and knowledge bases are the easiest part of the system to replace`）
  - 斯坦福手术共管筛查案例（`routine human triage missed half of eligible patients`；`a rubric that the institution owns`；`benchmarked five different LMs against consensus chart review`；`it performed competitively at a lower cost`；`there were a minimal amount of LLM errors`；`the physicians agreed 97% of the time`；`physicians declined about four in 10 flagged patients`）
  - 四问收束：能撑过 demo 的系统（`a system that most likely keeps working after the demo`）
  - Kevin：采纳优先与失败症状（`adoption is key`；`notoriously slow to adopt new technology`；`if the tool is cumbersome to use`；`It was not built for them`）
  - 「为」构建与「与」构建（`field technicians that were repairing equipment from meat grinders to ATMs`；`lean on them to help correct me where I'm wrong`；`Mary, the problem, not the solution`）
  - 行为正确、无评估即概念验证（`calling the right tools at the right time`；`an agent without evals is a proof of concept`；`you cannot confirm for sure that the agent is behaving as expected`）
  - 无痕迹用户、反馈与数据飞轮（`with blue collar workers, there's not that trail`；`they are very quick to tell you where it is incorrect`；`give them a Google spreadsheet`；`you create an offline dataset`；`added to an annotation queue`；`a constantly flowing dataset that is evolving with the use cases`；`keep the loop running`）
  - 信任、精选数据集与拥护者（`if you've ever heard of that IKEA effect`；`they're craftspeople`；`These evaluation data sets are typically very curated`；`show it improving`）
  - SEP：黑暗工厂之问与「放大器」研究（`agents writing all the code`；`when do we turn off the lights and kick up the dark factory`；`a sense making framework`；`The 2025 door report is the oldest`；`It amplifies what's already there`；`every team needs a dark factory`；`shipping AI slop and nobody knows what right looks like`；`fix the AI fit`）
  - 六项约束与原型受挫（`Two days later, lo and behold, he has a working prototype`；`We haven't delivered any software yet`；`there's six constraints that we found`；`Do you need subject matter experts`；`a big one for regulated industries`；`the devs ran out of tokens`；`millions of input parameters`）
  - 四种模式与三个团队（`there's four modes that we commonly find our teams operating in`；`individual agentic coding mode`；`we had to build a shared pile of information`；`buildings falling down`；`This was a good fit for us`；`Spend all the money you want`；`a six x reduction of effort for the project`）
  - 目标是适配而非黑暗工厂（`the goal here is fit`；`picking the mode that best operates for you`）
  - 精益与五条原则（`Toyota never told anyone to hang an Andon cord`；`are true everywhere. The practices aren't`；`we're gonna start with the foundation, shared infrastructure`；`Until you schedule a block of time in the week`；`verification before velocity`；`you need to make it not a bottleneck`；`Save the thinking for the humans`；`Five principles. Three teams, same principles, different modes, different practices`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 归档逐字稿为出版方页面的自动转写，个别专名疑有转写误差，正文按上下文注明理解方式：如 “o three minutei” 疑为 o3-mini、“LMS judge” 疑为 LLM as judge、“element as judge” 疑为 LLM as judge、“2025 door report” 疑为 DORA 报告、“Mary, the problem, not the solution” 疑为 “Marry the problem, not the solution”。
- 节目中两段赞助商广告（Framer、Prediction Guard）及开头结尾的节目运营信息属外围内容，未纳入正文。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
