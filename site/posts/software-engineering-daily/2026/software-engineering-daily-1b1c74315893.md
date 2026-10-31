---
item_id: software-engineering-daily-1b1c74315893
title: '管住失控的 AI 编程账单：Databricks 的模型路由、网关控制面与知识层'
date: '2026-11-01'
published_at: '2026-10-27'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/managing-ai-coding-costs-at-scale/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1968-Databricks-2026.txt'
summary: 'Databricks 联合创始人 Patrick Wendell 对话 Kevin Ball：AI 编程工具改按量计费后企业账单为何指数式膨胀；最大杠杆为何是价格曲线下移、把请求路由到最便宜够用的模型；网关与开发工具两侧的成本旋钮；以及成本管住后，缺上下文的企业知识层为何是下一个前沿。'
tags: [企业 AI, LLM, 组织转型]
---

# 管住失控的 AI 编程账单：Databricks 的模型路由、网关控制面与知识层

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-10-27 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 16305 字 · 阅读约 41 分钟
>
> 标签：[企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [LLM](/tags/LLM/) [组织转型](/tags/%E7%BB%84%E7%BB%87%E8%BD%AC%E5%9E%8B/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/managing-ai-coding-costs-at-scale/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1968-Databricks-2026.txt)

## 速读

Databricks 联合创始人 Patrick Wendell 本期对话主持人 Kevin Ball：AI 编程工具改按量计费后企业账单为何指数式膨胀；最大杠杆为何是价格曲线下移、把请求路由到最便宜够用的模型；网关与开发工具两侧的成本旋钮；以及成本管住后，缺上下文的企业知识层为何是下一个前沿。适合正在为企业内 AI 工具做成本与安全治理的工程负责人，以及关心模型选型与路由架构的工程师。

最值得带走的三点：一是成本为何失控——模型能力跃迁（Opus 4.5 前后加上 Codex、Claude Code、Cursor 这类高质量 harness）撞上按量计费，Databricks 内部一度出现"两个月翻倍"的成本曲线，而最大的对策不是限制使用，而是搭上模型价格曲线的整体下移；二是路由与控制面的分工——把"哪个模型够用"本身做成可训练的分类问题，网关侧负责强制成本管控与熔断，开发工具侧保留上下文优势、还能在多个 harness 之间派发（开源项目 Omnigent）；三是下一个前沿是企业知识层——模型推理已经足够强，卡住它们的是拿不到公司上下文，代码库因为自描述、无 ACL 而 AI 先赢，公司其余知识则需要一个"学会这家公司如何运转"的知识层。

## 主题正文

### 嘉宾与博客缘起：同行在撞同一堵墙

Patrick Wendell 是 Databricks 联合创始人，用他自己的话说，职业生涯简单到只有一份工作：2013 年在 UC Berkeley 读博期间研究大规模数据与机器学习，随后与同伴创办 Databricks；如今他的日常是支持多个工程团队。（原文锚点：`My career history is pretty simple`）这期节目的背景是：Databricks 有数千名工程师，要给每个人配上 AI 工具，同时兼顾安全、成本与自己的知识产权。（原文锚点：`we have thousands of engineers`）

促使他写那篇博客的，是太多客户——其中不少本身就是科技公司——来问"你们试过什么、什么有效、什么没用"；他还与 Stripe、Uber、Ramp（他自己也用了"我记得好像是"的口吻）等同行公司交换笔记。（原文锚点：`I had talked to so many of our own customers`；`We had talked to Stripe, Uber, I think Ramp`）这篇登上 Hacker News 首页的文章，按他的说法是"把脑子里的东西全部倒出来"，给面对同样问题的人一个可参照的数据点。（原文锚点：`reached the top of Hacker News`；`I wrote that post to dump everything out of my brain`）

### 成本如何失控：能力跃迁撞上按量计费

Patrick 把行业心态的转变讲得很具体：2023 到 2024 年（甚至 2025 年初），公司担心的还是"员工用 AI 用得不够多"；转折发生在他印象中的 Opus 4.5 前后——模型开始真正擅长写代码，又配上 Codex、Claude Code、Cursor 这类高质量 harness，问题从"推着大家用"变成"大家用得太猛"。（原文锚点：`Something changed roughly, I think, around Opus 4.5`；`like Codex or Claude Code, or Cursor`）几乎同时，基础模型厂商从按席位收费（他举的例子是"每个开发者每月 100 美元"）转向按量消费计费。（原文锚点：`switched to consumption prices`；`pay $100 per month for developer`）

两件事叠加，Databricks 内部出现了"看起来像指数增长"的成本曲线。按他的口径，成本建模时发现两个月里翻了一番，而公司有数千名开发者，这种速度累积起来非常快。（原文锚点：`what looked like exponential growth in costs`；`doubling in this two-month period`）他的判断带着"物理定律"式的口吻：任何一家不处理这件事的公司，最终都会被它拖垮。（原文锚点：`it will eventually bankrupt that company`）

他也不认为厂商转向按量计费是单纯收割：固定价套餐下，重度用户会让基础实验室"亏很多钱"，他自己就承认是让厂商吃亏的那类用户；消费计费把 ROI 的判断责任交还给买家——而这就要求企业自己学会做成本管理。（原文锚点：`the foundation lab was losing a lot of money`；`puts the onus on you`）

### 最大杠杆：模型价格曲线整体下移

谈到短期可用的缓解手段，Patrick 说他们看过四件事，而节目重点展开的第一件也是他眼中最大的杠杆：模型价格的持续下降。（原文锚点：`we looked at four things`）任一时点都存在一条质量对成本的帕累托曲线，而新一代模型会让整条曲线向好的方向移动——固定任务变便宜，或者固定预算干更多事。（原文锚点：`constant price reductions in models`；`continuous tradeoff of quality versus cost`）对 token 量巨大的团队，即便整体只便宜 20%，也是一个非常有意义的数字。（原文锚点：`getting 20% off a huge cost`）

为什么性价比能持续改善？他的解读是：软件工程是高度可验证的领域，可以上强化学习、进入自我改进循环；再叠加更多算力、推理与训练栈的持续优化，"每美元买到的质量"像有一条摩尔定律式的曲线在起作用。（原文锚点：`software engineering is a highly verifiable domain`；`quality cost ratio just seems to keep improving`）

需求为何迟迟不饱和？Patrick 的观察是开发者不断把更复杂的任务交给模型——旧任务上模型早就"够好"，只是人们又想出了新任务。（原文锚点：`hand off more and more complex tasks`）主持人 Kevin Ball 回忆，Sonnet 3.5 是他第一个觉得"能可靠写出像样代码"的模型，当时他就判断这足以改变软件工程。（原文锚点：`Sonnet 3.5 was the first model I played with that could write solid code reliably`）Patrick 补充了一个对照：个人聊天场景的需求确实饱和了（多数问题像"附近哪里能买到热狗"），但编程与企业工作流远未到顶。（原文锚点：`the set of things people want is saturated`）因此在他看来，能敏捷地在模型之间切换，本身就是吃到价格红利的前提。

### 把模型配到问题上：默认降档与修剪模型清单

价格曲线之下还有第二层收益：把模型配到问题上。Patrick 的判断是，对常规编码任务，上一代模型的表现与非常昂贵的前沿模型几乎相同。（原文锚点：`for routine coding tasks`；`perform identically to a very, very expensive frontier model`）但靠用户自觉降档行不通：大公司里没人自己付账单，个体开发者的激励就是把旋钮拧到 10、别挡着我干活。（原文锚点：`no one is themselves paying the bill`；`turn the dial to 10`）

Databricks 的做法有两层。一是默认模型可以不是最贵的，想升档的人可以自己升；（原文锚点：`the default model maybe could be not the most expensive model`）二是修剪模型清单——前沿实验室的新版本并不总是比旧版好。（原文锚点：`We also prune the set of models`）他举了一个他自己也不确定具体版本号的例子：某个 Opus 新版本发布后，他们在自家基准上发现它"更贵而且更差"，于是决定直接跳过、不开放给用户；下一版已经改善。（原文锚点：`Opus 4.7 came out`；`I don't know if exactly 4.7`；`more expensive and lower quality`；`we're going to skip that one`；`since got better with the next model`）

### 动态路由：任务级、请求级与"够用"分类器

Databricks 越来越依赖动态路由来决定用哪个模型。Patrick 区分了几种粒度：可以按任务或会话把某人在一段时间放到某个模型上；对提交式（非交互）的工单，按提交内容决定；也有请求级的细粒度路由——"看起来就像服务器系统里的传统负载均衡"。（原文锚点：`what we're using is dynamic routing`；`This looks like traditional load balancing`）请求级路由更难做对：推理虽然可以建模成无状态问题，服务器端其实有状态（Kevin Ball 接话点出 key-value cache）。（原文锚点：`there actually is some state in the server`）

缓存直接影响经济性。按他的口径，缓存读取大约比非缓存读取便宜一个数量级——他自己也补了一句"大概 10 倍吧，我也不确定"。（原文锚点：`10 times less or something than non-cache reads`）何时值得为某类问题专门建缓存，要同时权衡能省多少、性能会降多少、损失多少缓存收益，他认为这是非常值得研究的问题。

"哪个模型对这个问题够用"本身就是难题——连人都判不好，这也是大家倾向于一直用最贵模型的原因。Databricks 的答案是训练分类器来做这件事：这是一个 AI 问题，可以用 LLM 类的分类模型解决；不需要 100% 准确，命中率高到一定程度就可用。（原文锚点：`we build models to do that classification`；`a high enough hit rate`）验证可以部分客观化——看测试通过率，或让更聪明的模型来评估解答——但仍有一部分靠人眼判断。（原文锚点：`the pass rate on some tests`；`we ask a much smarter model to evaluate the solution`；`a little bit of eyeballing`）

他的立场是：Databricks 不自己做基础模型，但把"擅长路由的模型"当作重要研究方向；并且建议多数公司把 AI 的选择权握在自己手里，保持多模型、多供应商。（原文锚点：`most companies should take AI into their own hands`）

### 网关侧还是开发工具侧：成本与控制力的两个支点

路由逻辑放在哪里，是这期节目最"工程治理"的部分。网关（代理）侧的好处是客户端完全不用感知：代理对客户端说同一个推理 API，老客户端也能直接换装。（原文锚点：`your client is out of the loop`）强制性的成本控制放在服务端也更容易——避免"有创意的员工"改客户端设置绕过规则，比如把低效模型整体下线，不希望它们出现在可选集合里。（原文锚点：`avoids creative employees`）针对意外失控的花费，他们有一个熔断机制：有人（比如夜间忘关的循环任务）意外跑出失控花费时自动掐断，事后确认是有意为之可以重置。（原文锚点：`accidentally run runaway spend`；`We have a thing that will torpedo that`）

客户端侧的价值则是信息更多：它看得到整个会话历史、知道任务背景，Patrick 预计客户端侧也会出现很多智能。（原文锚点：`the client knows much more`）他同时提醒，真正要评估的往往是"模型加 harness 的配对"——同一模型在不同 harness 里可能一个很贵、一个很便宜。（原文锚点：`model harness pairs are really what you need to look at`）

客户端还有一个服务端做不到的能力：在 harness 之间派发。Databricks 开源了多 harness 派发器 Omnigent——你对着统一接口写代码，背后可以调用不同 harness，甚至让 harness 之间保持对抗关系：比如一个写代码、一个审代码。（原文锚点：`dispatch between different harnesses`；`called Omnigent at Databricks`；`adversarial relationship between your harnesses`）理由是模型评审自己的输出时会打虚高分数，跨模型评审的反馈要好得多。（原文锚点：`Models are very bad at reviewing their own output`）再往上一层还有"在 harness 之间路由的元 harness"；这套逻辑最终会落在哪一层，他坦承不知道——现在这三层都在用。

### 用自家代码库做评测：一小时内筛掉大多数新模型

模型好不好，以前 Databricks 靠灰度发布"用抱怨当信号"：把模型推给数千开发者，等抱怨多到信号噪声比够高，才确认这个模型真的有问题；期间可能已经在差模型上浪费数周。（原文锚点：`the complaints would start to come in`；`we would waste weeks with a crappy model`）成本有 AB 测试很快能看出来，质量却始终难以衡量。（原文锚点：`AB test that's pretty quick`）

解法是自建评测：他们基于自己代码库的时点快照做了一套基准，就是让模型去给 Databricks 代码库贡献代码，再离线评测。（原文锚点：`good evaluations you yourselves can run`；`go contribute code to Databricks`）目标是新模型发布一小时内就能判断值不值得内部试用；这套离线基准会筛掉"多得惊人"的候选，现在每周要跑多次，开源与闭源模型都在测。（原文锚点：`within an hour of a new model coming out`；`rules out a surprisingly large number`；`we're running that multiple times`）他们想把在用模型收敛到三到五个、构成帕累托前沿；评测结果虽然定期公开，但他提醒不要过度外推——基于自家代码库，可能存在过拟合。（原文锚点：`define that Pareto frontier`；`there could be some fitting going on`）

一个实测教训：必须把"模型加 harness 配对"作为整体来测，结果会截然不同。（原文锚点：`the model plus harness pair needs to be benchmarked`）主持人 Kevin Ball 补充，像 Pi 这种可定制性极强的工具还会进一步放大组合维度——模型加 harness 之外还有扩展与技能。（原文锚点：`Pi is incredibly hackable`）

### 语言与代码结构：流行语言与可验证接口（直觉而非结论）

Kevin Ball 问了一个好问题：代码组织与风格是否影响 LLM 的效率与成本？Patrick 明确说他们没有系统性的研究基准，只能给直觉。语言层面，互联网上各语言的代码量近似幂律分布，最大、最流行的语言效果最好，因为训练数据最多；Databricks 有相当比例的 Scala，"LLM 写 Scala 不算厉害"，他们在逐步把这些代码移到 Java。（原文锚点：`LLMs are not amazing at Scala`；`the biggest and most popular languages just tend to be the best`）他甚至怀疑，最终起决定作用的就是"互联网上这个语言有多少行代码"。（原文锚点：`how many lines of code on the Internet are in this language`）

他给了一个内部佐证：同一产品的内部功能有 Python 和 SQL 两个前端、背后是同一表示，把生成侧从 SQL 换成 Python 后，代码质量"一切都好多了"——因为 AI 更会写 Python。（原文锚点：`everything got way better`）结构层面，能重起炉灶的团队更注重接口设计，把 LLM 改动的范围做得更小、更可验证——这本来就是对人类也有益的模块化设计，只是"为 LLM 而做的 ROI 高得多"。（原文锚点：`make the scope of their changes smaller and more verifiable`）他强调以上都属于直觉判断，这个领域没有可靠的研究结论。（原文锚点：`We don't have robust research findings in this area`）

### 三条"宗教"与 AI 网关：企业级控制平面

组织落地层面，Databricks 从一开始就坚持做多模型、多工具的公司（至少在研发领域）：提供一组主流工具让工程师"用脚投票"，因为"什么是最好"每个月都在变。（原文锚点：`we wanted to be a multi-model, multi-tool company`）

坚持统一的是一道"窄腰"：公司内部自建的 AI 网关。所有 token 都过网关，公司里任何工具发起的每次推理都可见；对内部系统的数据访问也走这道网关——实际就是一个 MCP 代理，访问 Google Drive、Salesforce 之类都在上面做授权与全量留痕；对模型供应商则坚持零保留。（原文锚点：`narrow waist in the company`；`all tokens go through that gateway`；`an MCP proxy effectively`；`we insisted on zero retention for the people providing us the models`）这套能力后来产品化为 Unity AI Gateway；他的判断是，规模够大的公司需要这样一个中心控制面——哪怕不用 Databricks 的——这也是快速换用更便宜、更好模型的前提。（原文锚点：`We ended up productizing ours, called Unity AI Gateway`；`quickly adopt cheaper and better models`）

他每周都看帕累托曲线：上面通常有一个开源模型、一个 Anthropic 模型、一个 OpenAI 模型，供给越来越多，"基本经济理论告诉我们，要保持对供应商的选择权"。（原文锚点：`On there is probably one open-source model`；`maintain option and suppliers`）归纳起来，他的"宗教"只有三条：工具可选（在主流集合内）、访问必须过网关、对模型供应商零保留；其余一切——代码怎么组织、团队怎么搭——都是持续实验。（原文锚点：`that's my religion`）

### 网关之上：OAuth 不够，还要行为风险评分与沙箱

数据访问授权的老问题是"让软件代表我行动"，主导方案是 OAuth 的委托模型；但 OAuth 的 scope 粗粒度且静态，对"代理（agent）代表我行动"的新场景是必要而不充分。（原文锚点：`the approach that dominated was OAuth`；`OAuth scopes tend to be fairly coarse`；`it's necessary, but not sufficient`）他借用信用卡行业的类比：发卡机构对每笔交易做风险评分，风险高的警告、更高的直接拦截或动态降额——代理也应该这样被行为建模，协议本身不支持这种基于动态风险评分的细粒度授权，所以他们在网关层来实现。（原文锚点：`risk score every transaction`；`dynamic risk scoring-based approach`）

他给了一个假想例：如果部署的代理突然开始全盘扫描公司 Google Drive、成批下载文档，这就是值得干预的风险行为——掐断该代理，并邮件询问部署者是否有意为之，就像信用卡公司短信核实"内华达的那笔加油是不是你"。（原文锚点：`scanning our entire Google Drive`；`cut off that agent`）他观察到代理确实会做"中度不对齐"的事——不至于发动网络攻击，但可能用最省事的方式把公司内容搬到公开端点。（原文锚点：`medium unaligned behaviors`）

为此他们做网络沙箱等隔离：开发环境不光访问企业系统要走代理，也不能随便访问外网。（原文锚点：`network sandboxing`）Databricks 主要用云端开发机（少量本地开发则随工具带本地沙箱），据他们所知，至今没有代理逃出过自家的开发沙箱。（原文锚点：`we primarily have cloud dev boxes at Databricks`；`none have escaped our own development sandboxes`）

### 下一个前沿：企业知识层

先说结果：按 Patrick 的口径，AI 在 Databricks 的落地是成功——发布更多代码与功能，收入增长在"AI 后时代"甚至加速了（他说这是他们公开谈过的）；而基于这套成本手段，账单"感觉可控多了"，当然这始终是演进中的状态。（原文锚点：`We're shipping more code`；`revenue growth has actually accelerated`；`the costs are feeling much more under control`）

现在他更关心的是：为什么生产力没有随模型能力线性兑现。模型已是惊人的推理者，他甚至认为在许多情况下"它们比我聪明"（他自嘲说那就当他处于员工中位数吧）；理论上公司可以一夜之间多出 10 倍员工，但 10 倍代理换不来 10 倍产出——头号问题是模型拿不到完成工作所需的上下文。（原文锚点：`smarter than me in many cases`；`10 times more employees than overnight`；`the models not having the context`）

为什么编程反而是 AI 先赢的领域？他的解释是：代码库是自描述的、为密封性而设计；Git 时代之后代码库没有 ACL——"你要么在仓库里，要么不在"，可见性问题天然不存在。（原文锚点：`A code base is self-describing`；`The only ACL git has, you're either in or out of the repo`）模型拿到的是密封、可搜索、带可验证测试的环境，自然如鱼得水。而公司数据不是：不是每条数据人人可见，不能让 CEO 的信息泄露给刚来的实习生，数据侧因此有 ACL 难题。（原文锚点：`not every piece of data in a company can be seen by every person`）

他的新重心是给公司建"知识层"（有人叫本体，Databricks 的产品就叫 ontology）：公司信息散在 Slack、数仓、文档、人的活动与"似乎只能靠对话传播的隐性知识"里，而这一层必须既尊重访问控制、又不让人感到被监听。（原文锚点：`There's also, I think, a knowledge layer`；`Someone call it an ontology`；`There's data in Slack`；`implicit knowledge that seems to only diffuse through conversations`；`respects access control and it's not creepy`）连 Databricks 自己的计价单位 DBU 都是这样的难题——财务和产品团队对其衍生指标的定义"甚至不完全一致"。（原文锚点：`called a DBU`；`don't even totally agree on the definitions`）

对当下流行的技能（skills）文件，他的判断是：确实比没有强，但由人手工创建就会过时，一万人的公司靠互相共享技能文件并不扩展；而且 AI 有上下文预算，技能的渐进式披露只是权宜。（原文锚点：`They go stale`；`10,000 people, that doesn't really scale`；`there's a context budget in these AIs`）他把终局描述成一个学习问题——"学会这家公司如何运转"，就像新员工第一年在找电灯开关，AI 原则上也能学；这需要搜索式的信号：偏好更新的、偏好来自权威来源的。（原文锚点：`learn how this company works`；`prefer things that are more recent`）技能文件之于企业知识，就像 Yahoo 目录之于万维网——到某个规模就不行了；主持人 Kevin Ball 总结为"企业 LLM 正处在 Yahoo 目录时代"。（原文锚点：`you remember the Yahoo directory`）

### 尾声：都在摸索，靠实验前进

节目最后 Patrick 顺带"打了个广告"：Databricks 的 AI 网关已有数千客户在使用，本体产品也完全开放、可配合其他工具；但他同样提醒存在大量 DIY 方案，不硬性推销。（原文锚点：`thousands of customers using it`；`tons of DIY versions of these things`）他给同行的收尾建议是：所有人都在摸索，包括他自己；唯一的学习方式是实验——试不同的东西、看什么有效，并和其他公司交换笔记。（原文锚点：`everyone is just figuring all this stuff out`；`The only way that we've been able to learn is through experimentation`）

## 来源与定位

- 原始节目：[Managing AI Coding Costs at Scale](https://softwareengineeringdaily.com/podcasts/managing-ai-coding-costs-at-scale/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 嘉宾履历与数千工程师的内部推广（原文锚点：`My career history is pretty simple`；`we have thousands of engineers`）
  - 登顶 Hacker News 的博客与同行交流（原文锚点：`reached the top of Hacker News`；`I had talked to so many of our own customers`；`We had talked to Stripe, Uber, I think Ramp`；`I wrote that post to dump everything out of my brain`）
  - 转折点：Opus 4.5 前后与高质量 harness（原文锚点：`Something changed roughly, I think, around Opus 4.5`；`like Codex or Claude Code, or Cursor`）
  - 从席位制转向按量计费（原文锚点：`switched to consumption prices`；`pay $100 per month for developer`）
  - 指数式增长与两个月翻倍（原文锚点：`what looked like exponential growth in costs`；`doubling in this two-month period`）
  - 不处理终将拖垮公司（原文锚点：`it will eventually bankrupt that company`）
  - 固定价让实验室亏钱、责任转移给买家（原文锚点：`the foundation lab was losing a lot of money`；`puts the onus on you`）
  - 四类短期手段与最大杠杆：价格曲线下移（原文锚点：`we looked at four things`；`constant price reductions in models`；`continuous tradeoff of quality versus cost`）
  - 大盘便宜 20% 已很有意义（原文锚点：`getting 20% off a huge cost`）
  - 性价比持续改善的机制（原文锚点：`software engineering is a highly verifiable domain`；`quality cost ratio just seems to keep improving`）
  - 需求未饱和与聊天场景的饱和对照（原文锚点：`hand off more and more complex tasks`；`the set of things people want is saturated`）
  - Kevin Ball 的 Sonnet 3.5 回忆（原文锚点：`Sonnet 3.5 was the first model I played with that could write solid code reliably`）
  - 常规任务上一代模型一样好（原文锚点：`for routine coding tasks`；`perform identically to a very, very expensive frontier model`）
  - 个体激励与默认降档（原文锚点：`no one is themselves paying the bill`；`turn the dial to 10`；`the default model maybe could be not the most expensive model`）
  - 修剪模型清单（原文锚点：`We also prune the set of models`）
  - 跳过"更贵更差"的版本（原文锚点：`Opus 4.7 came out`；`I don't know if exactly 4.7`；`more expensive and lower quality`；`we're going to skip that one`；`since got better with the next model`）
  - 动态路由的粒度与请求级负载均衡（原文锚点：`what we're using is dynamic routing`；`This looks like traditional load balancing`；`there actually is some state in the server`）
  - 缓存读取约便宜 10 倍（原文锚点：`10 times less or something than non-cache reads`）
  - 训练"够用"分类器（原文锚点：`we build models to do that classification`；`a high enough hit rate`）
  - 路由效果的验证方式（原文锚点：`the pass rate on some tests`；`we ask a much smarter model to evaluate the solution`；`a little bit of eyeballing`）
  - 多模型多供应商主张（原文锚点：`most companies should take AI into their own hands`）
  - 网关侧路由与强制管控（原文锚点：`your client is out of the loop`；`avoids creative employees`）
  - 失控花费的熔断（原文锚点：`accidentally run runaway spend`；`We have a thing that will torpedo that`）
  - 客户端信息优势与模型-harness 配对（原文锚点：`the client knows much more`；`model harness pairs are really what you need to look at`）
  - harness 间派发与开源 Omnigent（原文锚点：`dispatch between different harnesses`；`called Omnigent at Databricks`）
  - 对抗式 harness 与模型自审盲区（原文锚点：`adversarial relationship between your harnesses`；`Models are very bad at reviewing their own output`）
  - 靠抱怨的灰度与数周浪费（原文锚点：`the complaints would start to come in`；`we would waste weeks with a crappy model`）
  - 成本易测、质量难测（原文锚点：`AB test that's pretty quick`）
  - 基于自家代码库的评测（原文锚点：`good evaluations you yourselves can run`；`go contribute code to Databricks`）
  - 一小时内出结论与筛掉大多数候选（原文锚点：`within an hour of a new model coming out`；`rules out a surprisingly large number`；`we're running that multiple times`）
  - 收敛到帕累托前沿与过拟合提醒（原文锚点：`define that Pareto frontier`；`there could be some fitting going on`）
  - 模型与 harness 必须一起测（原文锚点：`the model plus harness pair needs to be benchmarked`）
  - Pi 的可定制性放大组合维度（原文锚点：`Pi is incredibly hackable`）
  - Scala 不占优与流行语言最好（原文锚点：`LLMs are not amazing at Scala`；`the biggest and most popular languages just tend to be the best`）
  - 起决定作用的可能是互联网代码量（原文锚点：`how many lines of code on the Internet are in this language`）
  - SQL 换 Python 的内部佐证（原文锚点：`everything got way better`）
  - 小而可验证的接口设计（原文锚点：`make the scope of their changes smaller and more verifiable`；`We don't have robust research findings in this area`）
  - 多模型多工具原则（原文锚点：`we wanted to be a multi-model, multi-tool company`）
  - 窄腰：AI 网关与全量可见（原文锚点：`narrow waist in the company`；`all tokens go through that gateway`；`an MCP proxy effectively`）
  - 零保留与产品化网关（原文锚点：`we insisted on zero retention for the people providing us the models`；`We ended up productizing ours, called Unity AI Gateway`）
  - 快速换用更便宜更好模型的前提（原文锚点：`quickly adopt cheaper and better models`）
  - 每周的帕累托曲线与供应商选择权（原文锚点：`On there is probably one open-source model`；`maintain option and suppliers`）
  - 三条"宗教"、其余皆实验（原文锚点：`that's my religion`）
  - OAuth 的粗粒度与静态局限（原文锚点：`the approach that dominated was OAuth`；`OAuth scopes tend to be fairly coarse`；`it's necessary, but not sufficient`）
  - 信用卡式行为风险评分（原文锚点：`risk score every transaction`；`dynamic risk scoring-based approach`）
  - 全盘扫描 Google Drive 的假想例与熔断（原文锚点：`scanning our entire Google Drive`；`cut off that agent`）
  - 代理的中度不对齐行为（原文锚点：`medium unaligned behaviors`）
  - 网络沙箱与云端开发机（原文锚点：`network sandboxing`；`we primarily have cloud dev boxes at Databricks`；`none have escaped our own development sandboxes`）
  - 成本可控与业务加速（原文锚点：`We're shipping more code`；`revenue growth has actually accelerated`；`the costs are feeling much more under control`）
  - 模型聪明但缺上下文是头号问题（原文锚点：`smarter than me in many cases`；`10 times more employees than overnight`；`the models not having the context`）
  - 代码库自描述与 git 无 ACL（原文锚点：`A code base is self-describing`；`The only ACL git has, you're either in or out of the repo`）
  - 数据侧的可见性难题（原文锚点：`not every piece of data in a company can be seen by every person`）
  - 知识层与本体（原文锚点：`There's also, I think, a knowledge layer`；`Someone call it an ontology`）
  - 散落各处的知识与设计约束（原文锚点：`There's data in Slack`；`implicit knowledge that seems to only diffuse through conversations`；`respects access control and it's not creepy`）
  - DBU 口径分歧（原文锚点：`called a DBU`；`don't even totally agree on the definitions`）
  - 上下文预算与技能过时（原文锚点：`They go stale`；`10,000 people, that doesn't really scale`；`there's a context budget in these AIs`）
  - 学习型终局（原文锚点：`learn how this company works`；`prefer things that are more recent`）
  - Yahoo 目录类比（原文锚点：`you remember the Yahoo directory`）
  - 网关产品客户与 DIY 提醒（原文锚点：`thousands of customers using it`；`tons of DIY versions of these things`）
  - 靠实验前进（原文锚点：`everyone is just figuring all this stuff out`；`The only way that we've been able to learn is through experimentation`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语；归档逐字稿按无时间戳处理，正文不引用推算时间。
- 无法独立验证的数字与细节（成本两个月翻倍、整体便宜 20%、缓存读取约便宜 10 倍、帕累托前沿三到五个模型、新模型一小时内出评测结论、收入增长加速、AI 网关数千客户、Opus 具体版本号等）均按受访者口径呈现；同行公司名单中的 Ramp 为受访者记忆表述；本期主持人为 Kevin Ball，嘉宾为 Databricks 联合创始人 Patrick Wendell。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
