---
item_id: practical-ai-651c4b57184e
title: 中西部 AI 峰会三讲（下）：AI 边界章程、CIO 四项决策与一线数据代理实战
date: '2026-11-16'
published_at: '2026-11-05'
transcribed_at: '2026-11-16'
model: 'GLM-5.3 Flash'
source_url: 'https://share.transistor.fm/s/1b301bdc'
source_name: 'Practical AI'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/1b301bdc/transcription'
summary: 'Midwest AI Summit Part 2：更多讲者片段——从企业落地、评估到组织实践，看一线团队如何在真实约束下把 AI 用起来。'
tags: [AI Agent, 企业 AI, 评估, 组织转型]
---

# 中西部 AI 峰会三讲（下）：AI 边界章程、CIO 四项决策与一线数据代理实战

> 节目：[Practical AI](/podcasts/practical-ai/)
>
> 节目发布：2026-11-05 · 逐字稿获取：2026-11-16 · 笔记整理：2026-11-16
>
> 全文共 19247 字 · 阅读约 49 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [评估](/tags/%E8%AF%84%E4%BC%B0/) [组织转型](/tags/%E7%BB%84%E7%BB%87%E8%BD%AC%E5%9E%8B/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/1b301bdc) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/1b301bdc/transcription)

## 速读

本篇是中西部 AI 峰会特辑的下篇：Practical AI 再放出峰会的三段演讲。Don Barger（International Mission Board 创新与人工智能总监）讲组织如何在写下第一行代码之前先立 AI 章程，用「不做什么」的清单一百八十一岁的保守组织里赢得变革信任；Noblis 副总裁兼 CIO Mark Lay 把「AI 需要像员工一样被管理」展开为 CIO 必答的四项决策——委派什么、谁担责、谁验证产出、正在欠下多少技术债；AeroCore Technologies 资深数据分析经理 Darren Taillie 分享两段一线落地：Text-to-SQL 代理进 Teams 实现自助取数，视觉模型每天早上核验夜班工单，让月末对账会议这个月直接取消。适合正在为组织划定 AI 边界、承担 AI 问责，或推动一线数据自助的负责人、工程师与企业 AI 团队。与上篇特辑（可靠工作流、一线共创与智能体自主度）互补，本篇更靠近组织与业务的落地端。

## 主题正文

### 特辑第二辑：峰会的另外三个切面

本期开场由联合主持 Chris Benson 交代特辑形态：本周继续放出中西部 AI 峰会的三位讲者——International Mission Board 的 Don Barger、Noblis 的 Mark Lay 与 AeroCore Technologies 的 Darren Taillie，下周节目恢复常规嘉宾格式。（原文锚点：`three more of our speakers from the Midwest AI Summit`；`Don Barger from the International Mission Board, Mark Lay from Nobelis, and Darren Taillie from Evercore Technologies`）峰会现场仍由 Daniel Whitenack 担任主持与串场，他给 Don 这场演讲拟的题目直指组织落地 AI 最早撞上的那道墙：「构建 AI 信任——我们说了什么可以、什么不可以」。（原文锚点：`building AI trust, what we said yes to and what we didn't`）

### Don Barger：先立章程，再写代码

Daniel 介绍 Don 是 International Mission Board（下称 IMB）的创新与人工智能总监，早年在拉美等地以口传与叙事策略开展工作，并一路陪伴他的组织推进 AI 旅程。（原文锚点：`director of innovation and artificial intelligence at the International Mission Board`；`deploying strategies rooted in orality and storytelling`）Don 开场自陈不是典型的 AI 讲者：本科读会计，还有两个神学学位；他想传达的恰恰是鼓励——普通人也许有史以来第一次可以做出令人惊叹的东西，他的组织这三年来对 AI 的拥抱超出他三年前的想象。（原文锚点：`I have an undergraduate degree in accounting and two degrees in theology`；`normal people can build incredible things`）

故事的起点在将近四年前：在与 Daniel 在伦敦酒店大堂画草图、「接下来我们已经在做很多疯狂的事」之前，他先和另一个团队坐下来，专门讨论「我们相信 AI 是什么」——团队里一位成员刚读完数字伦理与计算机伦理的博士；他们花几天时间、八个人敲定了一份章程，约定在写下任何一行代码之前先想清楚会做什么、不会做什么。（原文锚点：`almost four years ago, I'll tell you how we got started`；`we sketched out some stuff in a hotel in London in the lobby`；`Before we ever write one line of code`；`we hammered out this agreement`）他回顾这份章程影响了团队此后的一切：什么可行、什么该说不，不必每次重新纠结；多次有人提出的需求，团队得以直接回绝——「我们认为那不是 AI 该做的事」。（原文锚点：`what we're going to say no to without even having to think about it`）

他把「能做不等于该做」称为大多数组织跳过的那场对话，并把责任问题当作建立信任的问题：在一个一百八十一岁的组织里，展示出你在认真构建信任，人们对改变的开放度会高得多。（原文锚点：`Just because we can do something doesn't mean we should do something`；`The responsibility question is the one that builds trust`；`an organization that's 181 years old`）更根本的是本体论层面的追问：如果你没想过自己关于 AI 的信念、AI 的本体论（ontology of AI）、你如何对待 AI 并允许它做什么，他挑战你先停下代码、停下来想清楚——他不认为业界头部人物在花时间思考这个「该不该」的问题，而这层思考需要有人带头去做。（原文锚点：`the ontology of AI`；`I think we need to be leading out in helping do that`）

「做」清单与提速。「容易的那些」：起草与编辑、摘要与研究——所有人都在做的通用任务；翻译——翻译工具帮他们省下大量开支；培训材料、学习支持与内容；写代码，但永远人在环。结果是交付节奏的质变：过去发布新产品要花数年、靠并不真懂需求的外包承包商，如今可以一天出原型、几个月内发布像样的产品。（原文锚点：`drafting and editing, summarizing and research`；`we always have humans in the loop when we write code`；`prototype in a day and ship within months`）

「不做」的五条红线：AI 在事工中把自己呈现为人——任何时候有人以为自己在和真人对话，就不能让 AI 冒充人类发声；由 AI 独自对人做出最终决定；在当事人不知情时监控人——他提醒这正在我们周围到处发生，他们不愿参与；在高风险、高利害场景给 AI 自主行动权——他们有人分布在世界各地服务，不愿把那类决定交给 AI；以及被拒绝最多的一条——把「灵魂关怀」（soul care）交给算法。（原文锚点：`AI presenting itself as a human in ministry`；`Final decisions about people that would be made solely by AI`；`Monitoring people without their knowledge`；`Autonomous actions in high risk and high stakes context`；`handling what I would consider soul care over to an algorithm`）灵魂关怀的清单很具体：牧养、祷告、辅导、门徒训练、深度个人关系、危机陪伴。他不希望 AI 承担牧者职责、不希望它做心理咨询——人真的需要与人互动；AI 可以帮忙筛查、鼓励与准备支持材料，但替代不了那个人，而且在他看来 AI 是把自己解放出来做更多这样的工作，而非取代。（原文锚点：`I don't want AI to be taking on pastoral responsibilities`；`AI can prepare the support, but it can't really replace the person`）

边界先行的价值在一个具体请求里得到检验。某个团队来找他：有人急需辅导却没有咨询师，也想办法送人去咨询，能不能帮他们做一个「基本充当咨询师」的 AI 聊天机器人？他不需要纠结——答案在章程里早已写下：不做，并把章程解释给对方；对方仍坚持「需求太大，有总比没有好」，他的回应是：「如果做的是错的事，『有』可能比『没有』更糟。」他不知道那个团队后来是否仍那样做，但他本人不会帮忙实现；他坦承，按自己「上个飞机就能搭个方案」的习惯，当晚看着 Netflix 就能把原型跑出来、第二天发过去问大家觉得如何——正因为界限在代码之前就划好了，这个「不」才说得出来。（原文锚点：`Can you help us build an AI chatbot that would basically become their counselor`；`Something can be worse than nothing if you're doing the wrong things`；`we drew the boundaries before we wrote the code`）

### Faithbot：250 万用户产品上的边界决策

第二个案例是意外走红的产品 Faithbot：可以在 faithbot.tools 访问，那里还有多个为教会构建的工具；上线约一年半、约 250 万用户，没花一分钱广告，全靠口碑。（原文锚点：`You can find it at faithbot.tools`；`we have several tools that we've built for the church on this website`；`It's got around 2,500,000 users in about a year and a half`；`We've not had any paid advertising for it, it's just word-of-mouth`）定位是一个永远从信仰视角回答问题的聊天机器人，扎根于对基督教信仰重要的东西。（原文锚点：`answer your questions from a faith perspective`）架构上有两点值得注意：其一，产品覆盖 50 种语言，他另一处具体说 51 种，且每种语言使用不同的 LLM、各自的 markdown 与世界观，按用户入口地区自动加载——用他的话说，这不是一个被翻译出来的工具，而是「51 个工具合成一个」；其二，第三版是他从丹佛飞成田的航班上写的，落地前就已发布上线，老用户整体切换完成。（原文锚点：`It's in 50 languages`；`there's 51 languages, and each of them use a different LLM`；`before I landed, it was live`）

在这款增长失控的产品上，边界决策同样先行。第一个决策：不让 Faithbot 为人祷告。新版在飞机上第一次试玩就主动提出「为你祷告」，他先觉得酷、随即觉得不对劲——「AI 不能祷告」，于是花了下一个小时把祷告能力「反编程」掉；他的解释很清醒：AI 并不是真的在祷告，只是在模仿训练数据。（原文锚点：`I don't want Faithbot to pray for people`；`AI can't pray`；`mimicking the training data`）第二个决策：不让人把全部需要都定义给一个算法，要把人指向人。他们早期就发现，用户中有挣扎中的人、正在被虐待的人、自残以及有自杀念头的人；被标记的对话他会回看、确认 AI 回应得当——他并不知道对方是谁，只为质量核查取用数据。（原文锚点：`I don't know who they are, but I get the data to make sure the AI is responding well`）系统因此被设计成：遇到危机就尝试把用户连接到真人，推荐服务机构与危机中心；关键事件会通知他本人，必要时他可以跳进对话接管——他也如实交代这条的现实约束：5000 用户时可行，250 万用户时已不可能，只能靠大量抽查。（原文锚点：`it's going to try to connect you to help`；`I can hop into the conversation and take over for the AI`；`It is not possible when you have 2,500,000 users`）

Faithbot 还有一组明确的「不越界」：所有产品都被告知某些事不能做，不能成为仇恨、胁迫或伤害性的工具，要做造就人、帮助人的工具；不给医疗诊断；不给财务建议——他惊讶于部分地区用户把它当理财顾问，产品被设定为「回到你擅长的事上来，别做你不能做、不该做的事」；甚至明确拒绝替牧师写讲章，还会顺势「教育」用户不该这么做。（原文锚点：`It's not going to give you a medical diagnosis`；`we don't give financial advice`；`if your pastor is going to AI to help you write a sermon`）商业与数据上同样有立场：产品不出售、不收费，靠喜爱它的赞助人支持，这也倒逼团队不断重构、把运行成本做低；数据上最初「登出即消失」，后来因为用户习惯了回看旧对话，才做成登录可选——用户可以永远保持匿名。（原文锚点：`it's not for sale`；`It was gone once you log out`；`You can always be anonymous`）

他的收尾把整场演讲压成几条可带走的判断：选择做什么时，评估标准要包含信任而不只是可行性——一百八十一岁、保守而厌恶风险的组织之所以向他打开门，是因为团队一次次证明了能做出可信的决定；无论在自己组织内推进还是向外出售 AI 产品，与人建立信任都不可省略。起步永远从「我们如何能」（how might we）出发——世上有人专给 50 个「不能」的理由，他宁可做那个给出 52 个「能」的理由的人，哪怕 52 个里 49 个不成立；并且尽早决定「我们永远不做什么」——无论 ChatGPT 还是 Grok 上线了什么新功能都不为所动；而这些清晰的边界最终让他能做远比以前更多、更自由的事。（原文锚点：`you should evaluate against trust, not just feasibility`；`we've proven time and time again to make really good, trustworthy decisions`；`Always start with how might we`；`what will we never do`；`these clear limits are actually freeing me up to be able to do way more`）

### Mark Lay：CIO 的四项决策——像管人一样管 AI

第二段演讲来自 Noblis（一家服务联邦政府的科学与技术组织）副总裁兼 CIO Mark Lay，他负责 IT 战略与交付，并保障基础设施的安全与韧性；Daniel 说他曾在白板前问出一连串了不起的问题。（原文锚点：`vice president and CIO at Noblis`）Mark 开场先呼应此前演讲里的「leash（牵引绳）」概念，并把它升到 CIO 层面，展开成他认为是组织层面看待 AI 的四项决策（四个问题）。（原文锚点：`I really love the leash concept`；`four questions or decisions`）他描绘的处境是所有 CIO 的共同体感：AI 以光速前进，这个月见完厂商，下个月对方的功能与话术就全变了——都更好，但都不同。更深层的变化在于：过去组织先有业务问题、把流程固化进系统；如今是把一个「目标」交给技术，围上护栏或拴上绳子，让它自己去产出结果——这「挺吓人」，也彻底改变了看问题的方式。（原文锚点：`AI is moving at the speed of light`；`turning over to technology an objective`）

第一项决策：该把什么委派给 AI。他的前提很朴素：把活动交给自动化系统，与多年来「把任务委派给员工」是同一件事——当你坐在 ChatGPT 或某个工具面前、或决定要建一个系统时，你要决定委派什么、给它多长的「绳子」。（原文锚点：`very similar to what we've done for many, many years, and that is manage people`）衡量有两个维度：回报与风险。回报是要么做得更好、要么更有效率，两者都占不到就不该上 AI；风险则问出错的概率有多高、出错的后果有多重。（原文锚点：`There's what reward you're gonna get out of it and what risk`；`is there a risk of an error`；`if you don't get either of those, you really shouldn't put it in AI`）两维交叉成四象限：结果更好、负担更小是明确的收益；没有风险的探索（比如他自己上网探索）尽管去做；高风险区域则要把护栏上得很紧。他还呼应了同场早些时候 Heidi Porter（即上篇特辑的第一讲）关于护栏的观点：确定性护栏正该用在出错后果严重的象限。（原文锚点：`if there's better outcomes and less burden to do it, that's a clear gain`；`deterministic guardrails`）他的总结是：把一切都当作委派来看待，像对待员工一样接受它会犯错，但要控制错误、保持平衡——决定把绳子拴多长，也就决定了 AI 该放在哪、价值从哪来。

第二项决策：AI 行动时，谁负责。他的判断是很多组织把这件事过度简化了：问责不可被委派——人可以把问责交给人，但对 AI 不行；RACI 表上 A（Accountable）那一栏，链条上溯最终必须是一个人。（原文锚点：`accountability can't be delegated`；`in the RACI chart for the A, there always needs to be a person`）他把落地展开为四个覆盖全局的领域。

一是保护数据。Noblis 因面对大量联邦各机构的合规与安全要求，过去一年先识别出上千个相关数据集（他承认未必找全，但至少开始了），再收敛到约一百一二十个对业务运营真正关键的数据集——不是零散数据文件，而是表格或报告层面的信息资产——并配约 30 名数据管家（data steward），负责弄清数据的内容、质量、时效、保护要求与可见范围。（原文锚点：`identifying over a thousand datasets that we thought were relevant`；`we had about 30 data stewards of those`）这次梳理暴露了旧习惯：HR、财务这类「明知自己拥有数据」的部门，传统上总回答「数据在 HR 系统里、在账务系统里，系统会保护它」；走向 agentic AI 之后这套说法行不通了，必须有人拥有数据、懂得数据。（原文锚点：`You have to have somebody who owns the data and knows the data`）

二是验证输出。护栏之外，按你委派了什么、出错风险多大，存在一整块「输出数据质量」的工作：工具铺开之后，谁来检查数据质量？（原文锚点：`validating the output`）他再次用 Excel 作类比：Excel 是铺给全体员工与财务团队的平台，在他看来就是 AI 的等价物——正如 Lotus 1-2-3 与 Excel 出现之前，没有工具能那样操作数字，它改变了世界；但财务拿到 Excel 可以写宏、跑只有本团队才懂的流程，谁来控制、谁来管理产出？去中心化的资源无法集中管理。（原文锚点：`Excel is a platform that's been deployed to all our employees`；`You can't centrally manage that decentralized resource`）

三是监控代理行为。盯着代理是全新的概念，但类比管理员工的工作，组织早已知道怎么做，问题是如何把这个用了多年的原则套到自动化场景、判断它适用于哪里。（原文锚点：`monitor the behavior of the agents`）

四是拥有结果。合同团队里一位早期职业合同管理员，把二三十年资历同事的知识收进来，做了个对合同做「第一遍预处理」的系统——这不是 IT 部门做的，是业务团队自己建的；它必须被管理和维护，业务要认领所有权并让它持续运转，就像财务部门明白宏归他们所有。（原文锚点：`built this system that would do a first pass on the contracts`；`they understand they own the macros`）

第三项决策：你正在制造什么技术债。他说这是 CIO 天天焦虑、却少有人谈论的话题，而且是全新类型的技术债。第一层来自集中式与分布式平台的选择，即前面讲的部门自建应用；第二层他有切肤之痛：放开让团队自建并共享应用后，厂商改了工具，升到下一版时，旧应用一个都没能迁移过来。技术栈在演化、所用数据在演化，要看住交付价值链上对数据、其他系统的依赖；然后问自己能不能撤销、撤销的实际成本与时间是多少。（原文锚点：`what technical debt are you creating`；`none of the old apps converted`；`What's the cost of reversing it`）最后一问每个组织都在撞上：有没有演化的容量——不只是 token 成本会不会吃掉价值，还包括技术更替时，中央 IT 或被借力的业务团队还有没有容量继续运维已部署的东西；他承认这些是快环境里最难回答的问题。（原文锚点：`do you have the capacity to evolve`）

收尾他化用 Drucker 的管理命题：AI 能干很多活、能产出大量东西，但产出值不值、成本几何，取决于你如何回答和处理这四项决策。（原文锚点：`adaptation of Drucker's management theme`）

### Darren Taillie：发动机清洗公司的一线落地

第三段演讲回到最「脏」的现场。Daniel 介绍 Darren 所在的 AeroCore Technologies 是一家本地公司，拥有在全球为喷气发动机做清洗的独特技术，组织里多数人并不开发代理，却能从代理汇总的清洗数据与工单洞察中受益。（原文锚点：`washes on jet engines all around the world`）Darren 自我介绍是 AeroCore 的资深数据分析经理；公司用专利的核化泡沫（nucleated foam）技术渗入清洗发动机内部的积碳与污垢，他分析洗前洗后的发动机性能数据、评估每次清洗的效果、追踪长期趋势与预测性维护，为机队找出「坏苹果」。（原文锚点：`senior data analytics manager for a company called AeroCore Technologies`；`We use a patented nucleated foam technology`）公司自嘲是「数字世界里的极度模拟公司」：清洗卡车上没有任何数字部件；业务覆盖美国主要机场约 11 个国内站点，并已落地日本、利雅得与巴西，逐年扩张；燃油涨价、机票跟着涨的时代里，他们正是在尽力帮大航空公司把这个趋势抵消回去。（原文锚点：`an incredibly analog company in a digital world`；`about 11 domestic sites at the major airports`；`sites in Japan, in Riyadh, and in Brazil`）

数据侧的挑战很典型。会天天写 SQL 的人寥寥，且多数人被有意挡在数据库之外——「如今删数据太容易了」；请求全部涌向分析师，形成他们口中的「分析师瓶颈」：接请求、取数、合并、分析、回发，每周干满 40 小时，长期增长、额外任务与研究一概没有，全在重复回答「亚特兰大昨晚洗了几台」这类问题，同样的内容要对不同员工答上 55 遍。还衍生出他称之为「workaround 蔓延」（workaround sprawl）的现象：非开发者用 pandas 的 read_csv 加 groupby 与位置过滤硬凑，Jupyter notebook 里堆满一周的随机取数，周末清一次，别人既看不到也复用不了。而整个数据分析组只有他和另外一名员工。（原文锚点：`that leads to the analyst bottleneck`；`Most people don't have access to the database intentionally`；`workaround sprawl`；`how many washes did we do in Atlanta last night`；`our data analysis group consists of me and one other employee`）

第一段落地：Text-to-SQL 代理进 Teams。借助 AgentForge 与 MCP 服务器直连数据库查询，再放进 Teams——「没人喜欢多一次登录」；他说自己的手机当天已被使用代理的同事轰炸了三四次。典型问题如「返回这个机尾号的所有工单」，系统给出信息、实际查询与结果，方便团队追溯某架飞机的全部历史：飞机上所有工单、时间、执行人、地点以及每次清洗采集的技术数据。搬进 Teams 后采纳率非常高，分析数据里能看到持续的使用，重复问答的负担从分析团队身上卸了下来，也把他和同事解放出来做对公司更有益的事。（原文锚点：`No one likes an extra login`；`Return me all the work orders for this particular tail number`；`very high adoption`；`freeing up myself and freeing up my other analysts`）效率量级也变了：过去三十分钟、一小时、复杂问题一周的活，现在几分钟完成，他展示的一个复杂查询三秒返回；自助取数让领导层不必事事来 ping 他。对「安全与护栏怎么办」的疑虑，他们的选择恰恰是经由 AgentForge 与 MCP 服务器来建——既提供护栏，又给出必需的访问。（原文锚点：`things that used to take thirty minutes, an hour, a week for complex stuff, the system now does in a couple of minutes`；`building it through AgentForge with the MCP servers provides those guardrails`）

第二段落地更有趣：工单核验。发动机清洗多发生在深夜的机场：团队晚 7 点上班、凌晨 5 点收工，跨站点一晚做 15–30 台清洗，单个站点一晚约 6 台；通常一名技师独自在飞机旁作业——用手机采集需要的数据、记录要收集的信息，还要保证泵入发动机的清洗液量正确，现场没有人校验他的输入。「手滑」难免：深夜里 5087 看起来很像 5078。（原文锚点：`work shifts from about 7PM till about 5AM`；`fifteen to 30 washes in a night`；`In the middle of the night, 5087 looks a lot like 5078`）等到月底账对不上——清洗次数、机型、数量全可能出错。既有机制是技师每晚提交照片：写在机身侧白板上的伪表单、飞机照片、以及他们称作 effluent 的排出物照片，由其他站点的负责人与专业人员远程人工核验；但同样的错误反复出现——5078 被看错录成 5087，第二天真 5087 来了被当成重复工单删掉，月底才发现删错的那条才是真的，账已经乱了。（原文锚点：`a picture of a whiteboard that we've built on the side that acts as a pseudo form`）

解法是视觉模型。得益于此前在 AgentForge 上的使用，技师把照片上传到生成工单用的 Power App；每天早上 08:15，代理扫描全部照片，与 app 内录入的信息核对。视觉模型读机身侧的大号数字表现很好，连机尾顶部那个小号数字也能读出；对上就打勾，对不上就生成 flag 发给 Darren，由人去现场查看——有时是贴错照片，有时是云层、黑夜或画质问题。他特别感谢 Sharon 帮助把这个系统构建并部署起来。（原文锚点：`Every day at 08:15 in the morning`；`That flag gets sent to me`；`a human, go look at it`；`big thanks to Sharon who really helped me build this and deploy it`）提示词最终只有一句「Compare and flag」——他反复与模型拉锯，砍掉它「我觉得这架飞机大概是……」的发挥，强制它「只返回 N 和这些数字，别的一律不要」。（原文锚点：`Compare and flag`；`You need to return n and these numbers, and that's it`）

结果被他称作「wildly successful」，并已扩展到全部工单：每天中午向领导层发出摘要，覆盖过去 24 小时所有站点——商业与军方的全部工单；代理还扫描技师备注，标记烟雾事件（smoke fume events）与异常程序——「这次按烟雾排放处理」「这个周期没洗」「漏了一次清洗」等信息不再散失；还学会抓跨午夜工单——否则一张工单会显示 36 小时，实际只有约 4 小时。他们发现，人工 QC 反复漏掉的正是这几类问题。（原文锚点：`It goes out to leadership every day at noon`；`flags them anything related to abnormal procedures`；`we missed a cycle, or we missed a wash`；`work orders start taking thirty six hours`；`the same things were being missed over and over again by the human QC`）最大的成果在当月兑现：财务、数据、运营的三方月末对账会议被取消——这个月没有错误工单，也就没有逐条核对的理由；这类会议通常要花五到六个人小时，现在大家回去做开发、战略与面向未来的事。flag 目前只做记录与跟踪、团队按需处理，一个要求人工认领并了结的解决机制正在建设中。他把两段落地都归结为此前演讲讨论过的「AI 代理该放在哪」：工作量大减且结果更好。（原文锚点：`We canceled that meeting this month`；`talking about five, six person hours`；`Flags are currently just set and tracked`；`We are building in a resolution system as we speak`；`where your AI agents fit`）

下一步两个方向仍在「模拟世界」里做文章：让视觉模型自己从卡车与照片等途径采集录入信息，减少技师在 app 里手工输入；以及对清洗卡车阀门温度压力设定的视觉核验——那台卡车上没有计算机，全靠机械球阀与开关，既要确认每晚设置正确，又不想把卡车复杂化。（原文锚点：`There's no computer on that truck`；`Vision of truck valve temperature pressure settings`）

### 三段演讲的共同底线

三段演讲处在完全不同的语境——信仰事工组织、联邦政府服务商、发动机清洗公司——但落在同一条底线上：边界与问责必须在构建之前想清楚，而不是出了事再补。Don 的章程写在第一行代码之前；Mark 把问责钉死在「RACI 的 A 栏必须是人」；Darren 的视觉核验对不上时，flag 最终仍交给人去现场。三人都把 AI 定位成把人解放出来做「只有人该做的事」：对 Don 是灵魂关怀要留给人，对 Mark 是像委派员工一样委派并持续盯着，对 Darren 是把两名分析师从重复取数里释放出来做研究。Daniel 收尾时说，Daniel 知道把一件事从想法推进到日常使用需要什么，而 Darren 做到了——在团队环境里真正被用起来、价值兑现；他打趣说，这正是「95% 的 AI 试点失败」那项常被引用的 MIT 研究的反面——「我们需要更多 Darren」。（原文锚点：`from idea into daily use`；`ninety five percent of, AI pilots fail`；`we just need more Darren's`）

## 来源与定位

- 原始节目：[Abundant Intelligence at the Midwest AI Summit Part 2](https://share.transistor.fm/s/1b301bdc)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 特辑形态与讲者介绍（`three more of our speakers from the Midwest AI Summit`；`Don Barger from the International Mission Board, Mark Lay from Nobelis, and Darren Taillie from Evercore Technologies`；`building AI trust, what we said yes to and what we didn't`；`deploying strategies rooted in orality and storytelling`）
  - Don 的背景与「普通人也能构建」（`director of innovation and artificial intelligence at the International Mission Board`；`I have an undergraduate degree in accounting and two degrees in theology`；`normal people can build incredible things`）
  - 章程先于代码（`almost four years ago, I'll tell you how we got started`；`we sketched out some stuff in a hotel in London in the lobby`；`Before we ever write one line of code`；`we hammered out this agreement`；`what we're going to say no to without even having to think about it`）
  - 责任问题与信任（`Just because we can do something doesn't mean we should do something`；`The responsibility question is the one that builds trust`；`an organization that's 181 years old`；`the ontology of AI`；`I think we need to be leading out in helping do that`）
  - 「做」清单与交付提速（`drafting and editing, summarizing and research`；`we always have humans in the loop when we write code`；`prototype in a day and ship within months`）
  - 「不做」红线与灵魂关怀（`AI presenting itself as a human in ministry`；`Final decisions about people that would be made solely by AI`；`Monitoring people without their knowledge`；`Autonomous actions in high risk and high stakes context`；`handling what I would consider soul care over to an algorithm`；`I don't want AI to be taking on pastoral responsibilities`；`AI can prepare the support, but it can't really replace the person`）
  - 被拒绝的「AI 咨询师」请求（`Can you help us build an AI chatbot that would basically become their counselor`；`Something can be worse than nothing if you're doing the wrong things`；`we drew the boundaries before we wrote the code`）
  - Faithbot 规模、架构与上线（`You can find it at faithbot.tools`；`we have several tools that we've built for the church on this website`；`It's got around 2,500,000 users in about a year and a half`；`We've not had any paid advertising for it, it's just word-of-mouth`；`answer your questions from a faith perspective`；`It's in 50 languages`；`there's 51 languages, and each of them use a different LLM`；`before I landed, it was live`）
  - Faithbot 的边界决策（`I don't want Faithbot to pray for people`；`AI can't pray`；`mimicking the training data`；`I don't know who they are, but I get the data to make sure the AI is responding well`；`it's going to try to connect you to help`；`I can hop into the conversation and take over for the AI`；`It is not possible when you have 2,500,000 users`）
  - Faithbot 的「不越界」与数据立场（`It's not going to give you a medical diagnosis`；`we don't give financial advice`；`if your pastor is going to AI to help you write a sermon`；`it's not for sale`；`It was gone once you log out`；`You can always be anonymous`）
  - 以信任为评估标准与收尾两问（`you should evaluate against trust, not just feasibility`；`we've proven time and time again to make really good, trustworthy decisions`；`Always start with how might we`；`what will we never do`；`these clear limits are actually freeing me up to be able to do way more`）
  - Mark 的背景与 CIO 处境（`vice president and CIO at Noblis`；`I really love the leash concept`；`four questions or decisions`；`AI is moving at the speed of light`；`turning over to technology an objective`）
  - 决策一：委派什么给 AI（`very similar to what we've done for many, many years, and that is manage people`；`There's what reward you're gonna get out of it and what risk`；`is there a risk of an error`；`if you don't get either of those, you really shouldn't put it in AI`；`if there's better outcomes and less burden to do it, that's a clear gain`；`deterministic guardrails`）
  - 决策二：AI 行动时谁负责（`accountability can't be delegated`；`in the RACI chart for the A, there always needs to be a person`；`identifying over a thousand datasets that we thought were relevant`；`we had about 30 data stewards of those`；`You have to have somebody who owns the data and knows the data`；`validating the output`；`Excel is a platform that's been deployed to all our employees`；`You can't centrally manage that decentralized resource`；`monitor the behavior of the agents`；`built this system that would do a first pass on the contracts`；`they understand they own the macros`）
  - 决策三：新型技术债（`what technical debt are you creating`；`none of the old apps converted`；`What's the cost of reversing it`；`do you have the capacity to evolve`；`adaptation of Drucker's management theme`）
  - Darren 的公司与业务背景（`washes on jet engines all around the world`；`senior data analytics manager for a company called AeroCore Technologies`；`We use a patented nucleated foam technology`；`an incredibly analog company in a digital world`；`about 11 domestic sites at the major airports`；`sites in Japan, in Riyadh, and in Brazil`）
  - 分析师瓶颈与 workaround 蔓延（`that leads to the analyst bottleneck`；`Most people don't have access to the database intentionally`；`workaround sprawl`；`how many washes did we do in Atlanta last night`；`our data analysis group consists of me and one other employee`）
  - Text-to-SQL 代理进 Teams（`No one likes an extra login`；`Return me all the work orders for this particular tail number`；`very high adoption`；`freeing up myself and freeing up my other analysts`；`things that used to take thirty minutes, an hour, a week for complex stuff, the system now does in a couple of minutes`；`building it through AgentForge with the MCP servers provides those guardrails`）
  - 夜班工单的痛点（`work shifts from about 7PM till about 5AM`；`fifteen to 30 washes in a night`；`In the middle of the night, 5087 looks a lot like 5078`；`a picture of a whiteboard that we've built on the side that acts as a pseudo form`）
  - 视觉模型核验与提示词（`Every day at 08:15 in the morning`；`That flag gets sent to me`；`a human, go look at it`；`big thanks to Sharon who really helped me build this and deploy it`；`Compare and flag`；`You need to return n and these numbers, and that's it`）
  - 每日摘要、扩围与月末会议取消（`It goes out to leadership every day at noon`；`flags them anything related to abnormal procedures`；`we missed a cycle, or we missed a wash`；`work orders start taking thirty six hours`；`the same things were being missed over and over again by the human QC`；`We canceled that meeting this month`；`talking about five, six person hours`；`Flags are currently just set and tracked`；`We are building in a resolution system as we speak`；`where your AI agents fit`）
  - 下一步与主持人收尾（`There's no computer on that truck`；`Vision of truck valve temperature pressure settings`；`from idea into daily use`；`ninety five percent of, AI pilots fail`；`we just need more Darren's`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 归档逐字稿为出版方页面的自动转写，个别专名疑有转写误差，正文按上下文注明理解方式：如 “Evercore Technologies” 疑为 AeroCore Technologies、“Nobelis” 疑为 Noblis、“Norita” 疑为 Narita、“Lotus one, three” 疑为 Lotus 1-2-3、“I and B” 疑为 IMB（International Mission Board）。
- 节目中一段赞助商广告（SerpAPI）及开头结尾的节目运营信息属外围内容，未纳入正文。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
