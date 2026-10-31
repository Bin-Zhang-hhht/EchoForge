---
item_id: oxide-and-friends-2169e5e45598
title: Oxide 再融 4.45 亿美元：D 轮背后的融资、税与债
date: '2026-11-01'
published_at: '2026-10-18'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: 'https://share.transistor.fm/s/867a87b6'
source_name: 'Oxide and Friends'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/867a87b6/transcription'
summary: 'Oxide 时隔约半年再度融资：4.45 亿美元 D 轮 7 月交割、10 月官宣，Eclipse 领投，Atreides 与 AMD 新进。Steve Tuck 解释为什么「没主动找钱也要融」——更大的订单与供应链挤兑；CFO Scott Orn 拆解「为什么敢交税」：NOL 只能抵 80% 收入、研发税收抵免，以及「债是垫子不是地基」的用债哲学。'
tags: [开发者工具, 企业 AI, 硬件]
---

# Oxide 再融 4.45 亿美元：D 轮背后的融资、税与债

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-10-18 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 16153 字 · 阅读约 41 分钟
>
> 标签：[开发者工具](/tags/开发者工具/) [企业 AI](/tags/企业 AI/) [硬件](/tags/硬件/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/867a87b6) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/867a87b6/transcription)

## 速读

Oxide 时隔约半年再度融资：4.45 亿美元 D 轮 7 月交割、10 月官宣，Eclipse 领投，Atreides 与 AMD 新进（`Series D, 445 raise`）。联合创始人 Steve Tuck 解释为什么「没主动找钱也要融」——更大的订单、翻倍的在手 backlog 与五十年一遇的存储、芯片、被动元件供应链挤兑；CFO Scott Orn 则接住评论区「怎么敢交税」的质疑，从 NOL 只能抵 80% 收入、研发税收抵免，一路讲到「债是垫子、不是地基」的用债哲学。适合所有想看一家硬件公司如何把股权、债务与信用工具串成一套资本结构的读者。

## 主题正文

### 为什么「又要」融资：更大的订单与五十年一遇的供应链挤兑

开场就是自嘲：半年多前刚做过一期「一模一样的」节目（`Six, seven months ago`）——那时 Oxide 刚完成 2 亿美元 C 轮（`we raised $200,000,000 Series C`），叙事还是「预期盈利、资本充足」。为什么又融？Steve Tuck 说这轮「不是我们的主意」，公司并没有主动出去找钱（`we were not out seeking to fundraise`），而是订单变得大得多（`even bigger orders to go fill`），在手 backlog 大幅增加（`our backlog had increased substantially`），团队在拼命扩建产能、加码供应链承诺（`furiously building out manufacturing capacity`）。恰在此时，投资圈对 Oxide 兴趣浓厚（`very interested in oxide`），公司自己也在盘算接下来「非常可观的供应链需求」（`some very substantial supply chain needs`），希望把金融基础设施提前备好，让下一批更大的订单接得住。回头看，C 轮的逻辑一脉相承：向企业市场证明 Oxide 会长期在场、不会被收购（`we were not going to get acquired`）。

这轮融得很快：Eclipse 领投（`Got a great lead in Eclipse`），因为感兴趣的资本太多，最终比原计划多融了一点，而且在名单敲定前就已「相当深度的超额认购」（`pretty deeply oversubscribed`）。Bryan Cantrill 坦言分钱是个「好问题但也不好受」：团队明确想回报「从一开始就相信 Oxide 的人」（`reward those folks that had been early believers in Oxide`），给不出理想份额「挺难受的」（`can't give them the allocation that they want`）。

### 谁进了这一轮：领投 Eclipse，新进 Atreides 与 AMD

Steve Tuck 把这轮引入的新钱分成两类：跨界（crossover）投资人——「私募里也投、公开市场 IPO 时也一路投进去」的机构（`investors that invest in private but also invest at public`）——和战略投资人（`crossover investors and then strategic investors`）。筛选新股东的一条标准是「你有多了解这家公司」（`how well do you know the company`）：行情好时人人都爱财务回报，但公司要找的是对战略与技术判断「有更深信念」的投资方（`deeper sense of conviction than just the financial returns`）。按他的说法，这个阶段不了解公司、没花过时间的传统 VC，「能带来的新增价值更少」（`bringing less new value`）。

投资人 Pierre 的午餐忠告值得单独记一笔。他问 Steve：「你知道跨界投资人擅长什么吗」（`do you know what crossover investors are good at`）？答案是「擅长说你爱听的话」（`good at telling you what you want to hear`），以及「任何投资人都会在他们认为价格永远不会再高的时候卖出」（`the price is the highest it will ever be`）。Steve 当场表示这话有点绝对，「这里面确实有细微差别」（`I think there is nuance there for sure`）——这处分歧原样留在节目里。

新的大型跨界投资方是 Atreides。Bryan 原话被转写记成了「a tradies as a big new investor」（`a tradies as a big new investor`），并提到这家机构「我们几年前就见过」（`we met years ago was, Atreides`）；牵线人是老朋友 Alex（`introduced to them by Alex Bienaek`）——一位在种子轮错过了 Oxide 的投资人（转写把「Atreides 的人」记作 `the attorneys folks`，亦为转写噪声）。节目顺势给出一条经验：被拒绝不等于关系结束，「总有理由赴每一次会」（`a good reason to always take the meeting`）。

战略新股东是 AMD。Bryan 自嘲 AMD 对 Oxide「永远是伴娘、从没当上新娘」（`always a bridesmaid, never a bride with us`）——「差一点成为 Oxide 投资人」已经不是一次两次（`Almost an Oxide investor many times over`）。这次趁 Steve 进山断联，AMD 动作飞快，投的钱还超过了原本的意向（`invest more than they originally wanted to invest`）。Bryan 总结：很高兴 AMD 进了股东名册（`happy to have AMD on the cap table`）。

关于稀释：Adam Leventhal 说这轮「稀释非常有限」（`very minimally dilutive`）。Bryan 解释机制——理想状态是估值一轮比一轮高，卖给新投资人的比例越来越小，但「只要融资就有稀释」（`whenever you raise, it's dilutive`），关键看公司价值增长能否跑赢稀释；「公司也可能遇到 down rounds」（`companies can have down rounds`）。他觉得员工们对这轮「挺高兴」（`employees are pretty happy about this one`）。公司目标也顺带重申：做「一家世代级公司，那就意味着上市」（`a generational company, and that means a public one`），Steve 说「最终我们预期成为公众公司」（`we anticipate being a public company`）——但都强调「不是可预见的近期」（`not in the foreseeable future or the immediate future`），目前只是航向。

### 官宣的分寸：7 月交割、8 月 Form D、10 月官宣与「敢说盈利」

时间线本身就有戏：Steve 请网友自己查——「我们 7 月就 close 了」（`we closed in, like, July`），「Form D 是 8 月报的」（`Our form d was filed in August`），那为什么 10 月才官宣（`why was this announced in October`）？节目没有正面展开，只说明这次配合了一位想写报道的记者的时间线（`made sense to accommodate going through the timeline`）。真正成为公告钩子的是「盈利与交税」。Bryan 特别感谢 Eclipse 的 Seth Winteroth（`huge shout out to Seth, Seth Winteroth`）建议「你们应该谈谈自己盈利了」（`talk about the fact that you're profitable`）——因为 Oxide 一直刻意避开客户与收入边缘的话题（`customer related or sort of revenue related`），这次若非提醒未必会主动说。于是有了那张「交税照片」（`Did take a photo of us paying taxes`），也顺势确认了 `we had hit profitability`。

Hacker News 评论区则跑题跑得欢：至少三分之一的评论在讨论与这轮融资无关的 Oxide 招聘流程（`about the Oxide hiring process`），「九小时现场对话」（`nine hours of live conversations`）成了当天的引爆点。本文按主题聚焦融资与财税，招聘流程的争论仅在此作背景交代。

### 税务第一课：别为省税做蠢决定

Scott Orn 开场先报师承：Kellogg 的 Mitchell Peterson 教授——「我在 Kellogg 最喜欢的课就是税务策略」（`My favorite class at Kellogg was tax strategy`），此外他还「曾帮着经营过一家税务与会计事务所」（`I used to help run a tax and accounting firm`）。他的第一课反直觉：「税务优化的第一法则，是别为优化税务浪费钱」（`don't waste money trying to optimize your taxes`）。Oxide 的「桌面筹码」是往技术和团队里猛投钱（`investing super heavily in our technology and our team`），2026 年看到的盈利是盖过这些投入之后的部分（`the profitability that we're seeing here in 2026 is in excess of all that`）；而且节俭本来就是 Oxide 的核心价值观（`one of our core values is thrifty`），公司还在继续扩编（`our headcount has grown quite a bit`）、投建测试设施（`we're investing in test facilities`）。

接着是记账常识：运营开支（OpEx）当年即可抵扣（`That's deductible right away`）；资本开支（CapEx）哪怕是买测试设备，也要按年折旧（`you have to depreciate it over time`），即便套用加速折旧时间表（`accelerated depreciation schedules`），钱已经花出去、抵扣不会立刻足额到账。在他看来，「招人是最好的抵税投资」（`hiring is the best way of investing to offset tax`）。一个具体例子来自两个月前的 Demo Friday：团队把一个 3D 打印件改成了注塑件（`that was three d printed that we made injection molded`）——Scott 复述时说反了方向，Bryan 当场纠正；模具不便宜（`the molds were not cheap`）、先要投入「大约几十万美元」（`it might cost a couple $100,000`），但换来的 COGS 节省「巨大」（`the COGS savings is enormous`），连机柜里没插 sled 时空位用的挡板（`a cubby that does not have a sled in it`）也从 3D 打印换成了注塑，兼顾风道（airflow）与观感。

### NOL、研发抵免与那张「交税照片」

评论区有人问：backlog 那么大，怎么还乖乖交税？Scott 给出第一块拼图：很多创始人甚至 CFO 都不知道，「净经营亏损（NOL）最多只能抵 80% 的收入」（`you can only offset 80% of your income with NOLs`）。Oxide 的特别之处在于硬件世界里「只花了 1 亿美元就做到盈利」（`we've only spent a $100,000,000 to get the profitability`），其 NOL 恰好约 1 亿美元（`our NOLs are a $100,000,000`）。他随即用假设数字演示，并强调这只是演算口径、「用大数字让算术好懂」（`just using these big numbers to make all the math really easy`）：若今年赚 2000 万美元，只能动用 1600 万 NOL（`We can only use $16,000,000 of our NOLs`），剩 400 万应税；NOL 可以逐年结转、但有技术细节（`you can use your NOLs year after year`）。

第二块拼图是税收抵免，用来压掉「剩余 20% 的营业收入」（`that remaining 20% of operating income`）——这是 Oxide 「一直在做而且做得不错」的事（`Oxide has historically done and done well`）。他们刚做完 2025 年度的研发税收抵免，又追溯 2024 年度补做了一份（`we went back into 2024 and are doing one in 2024`）。Scott 坦言 2025 年初「没人想到 Oxide 2026 年会盈利」（`Oxide was going to be profitable in 2026`），所以此前没做；研发抵免本可在公司头五年抵 payroll tax，但 Oxide 2019 年成立、窗口已用完（`Oxide was founded in 2019`；`run its course on the payroll tax offset`），只能用来抵真实利润。两笔抵免合计约 220 万–230 万美元（转写把数字连写成一串长数，按他随后的演算口径为 220 万），用于冲抵 2026 年利润（`tax credits that we are going to use against our profits this 2026`）：400 万再减 220 万，「剩下 180 万美元的应税收入」（`now you're down to $1,800,000 of taxable income`）。最终交多少，取决于今年「实际能发出多少机柜」（`how many racks we can actually ship this year`），「不是个大数字，但有意义」（`It's not gonna be a huge number, but it's meaningful`）。Bryan 补充，那张照片里就是真的在给 IRS 打款、避免罚息（`wire transfer to the IRS`）。

Scott 的自豪感顺带给了行业坐标：作为「一家盈利的风投系公司 CFO」（`CFO of a profitable venture capital backed company`），他预计本周投资者大会上 200 家公司里「盈利的大概只有五家」（`five out of 200 companies there that are profitable`）。面对「Amazon 不交税」的类比（`Amazon doesn't pay taxes`），Bryan 的回应分几层：Amazon 早年很多年也不盈利（`Amazon also was not profitable for the first many years of operation`）；而且「人家当时做的是服务，我们是在出货」（`they were operating a service`；`we are shipping a product`）；他同时提醒「有些避税操作确实可疑」（`tax avoidance stuff is kind of shady`），但立刻声明不是说 Amazon。节目的底线是：并不存在「拧几个会计旋钮就让税消失」的事（`turn arbitrary accounting knobs`）。

### 债是垫子，不是地基

评论区另一股「为什么拿 VC 的钱而不发债/贷款」的发言（`why did you take venture capital rather than debt`），被 Adam 归为「达克效应儿童」（`the Dunning Kruger child`），但认真回答是有的。Steve 的第一句是常识：「借钱是要还的」（`when you borrow money, you have to pay it back`）；用银行账户余额去想 runway 可能很危险，因为账户里可能躺着「已经提取的几百万美元债务」（`millions of dollars of debt one has drawn down`）。Oxide 四年前在用 venture debt（`we were leveraging venture debt`），如今行业里经典 venture debt 变少、更多是普通商业债务（`venture debt these days and much more just debt`）。

然后是 Steve 敲了一整个职业生涯的黑板：现金转换周期要尽量收紧（`cash conversion cycle as, as tight as possible`）。Dell 的绝活是「负的现金转换周期」（`Dell brilliantly had a negative cash flow conversion cycle`），Costco 同理（`Costco very much the same way`）——先收客户的钱、再付供应商的钱。多数硬件公司相反：先垫钱买料、造完卖掉、再等回款。债务的角色就是「借钱去买材料」（`borrow money to be able to buy materials`），抵掉中间那段垫资（`offset that middle period`）；前提是终端客户信用要好，「客户信用不行，你借不到钱」（`customers that are not creditworthy`）。而「有钱才借得到钱」（`you have to have money to borrow money`），资产负债表越强，债务条件越好（`much better debt deals with a stronger balance sheet`）。Bryan 点题：这一大笔股权融资，很大程度上就是「为了让我们在债务端处于更好的位置」（`to put us in a better position with respect to debt`）。

Scott 的职业生涯一直在和债打交道——他曾是债投基金 Lighthouse Capital 的合伙人，一干九年（`a partner at Lighthouse Capital`）。他的框架是：没有债的时候，董事会层面是「投资人与创始人/管理层两方，需要保持一致」（`two parties that need to stay aligned`）；他反复称赞 Oxide 董事会「几乎没有政治」（`there's very little politics`）。而债一进来就「多了第三方」（`you're adding a third party to that dynamic`）：顺风时放贷人「被动而友好」（`passive and collegial`），可一旦公司出麻烦，第三方只关心拿回自己的钱，「你可能非常快地失去对公司的控制」（`lose control of your own company really, really quickly`）。所以他的哲学是：股权按需要的上限去融，「垫子用债来做」（`the cushion comes from debt`）。

垫子哲学的好处是实打实的：有强股权垫底，Oxide 现在「以中个位数利率借钱」（`we are borrowing in the mid single digits`）；没有的话「借 10%、11%、12% 都很轻松」（`we'd be borrowing at like 10, 11, 12% easily`）。用处也具体：就在上周，Micron 通过合作伙伴「间接给了额外配额」（`Micron basically is giving us extra allocation indirectly`），公司想「hit the bid」吃下这批货，靠的正是 Western Alliance 信用额度里有富余（`a credit line with Western Alliance`）——Scott 顺带感谢 Western Alliance 「多年来一直是极好的放贷方」（`Western Alliance has been a fantastic lender for Oxide`）。背景是 Steve 说的「五十年一遇的存储、芯片、被动元件供应链挤兑」（`once in fifty year supply chain crunch`）：现在的问题不是价格，而是「能不能拿到足够的货」（`can you get enough supply`）；被动件与电源「最终都汇到 TSMC」（`all things kind of roll up to TSMC`），没有花钱买断产能的通道，必须「在还没有确定性需求时就下长注」（`long ahead of even having like guaranteed demand`）。此时「债成了竞争优势」（`the debt becomes a competitive advantage`）。反过来，Scott 警告「不要在刀刃上配置资本」（`capitalized on a knife's edge`）：若只靠应收款融资，就是「零容错」（`zero margin for error`），根本做不了机会型采购。

### 信用证、条款与失控风险

债务话题的深水区是信用证（letter of credit）。Oxide 资本效率高的一个原因是用代工厂（`we use contract manufacturers`）：对方垫库存、垫「半建成」的机柜，而且出货后还要 30 天才回款（`not getting paid for thirty days`），三笔现金敞口都压在薄利的代工厂身上——万一 Oxide 倒了，代工厂会蒙受巨大损失。公司的做法是给对方开信用证「把他们补足」（`give them a letter of credit to kind of make them whole`），而信用证由银行提供（`the letter of credit is funded by a bank`）。拆分信用额度开证后，额度不能重复占用——「不能超订你的 credit line」（转写作 `you don't get to overbook your deadlines`，deadline 为 credit line 的转写噪声）；比如要「今天提取约 2500 万美元」（`draw down like $25,000,000 today`），加上已占用的信用证，必须低于总额度。备选方案是现金质押开证（`cash collateralize your letter of credit`），但那会牺牲现金收益；Oxide 谈成了「直接收费、费用象征性」的安排（`a straight fee arrangement and it's a nominal fee`），让现金保持流动与收益——这是大约「九个月或六个月前」落地的事（`maybe nine months ago, six months ago`），前提正是账上先有了「更大的银行债务额度」（`this larger debt line with our bank in place`）。

条款是另一处暗礁：covenant 可以温和到「盈利或收入条款」（`profitability or revenue covenants`），也可能危险如「重大不利变化条款」（转写作 `material average change clause`）或「投资人放弃条款」（`investor abandonment clause`）——后者基本等于「你的投资人不再愿意投你了」。一旦违约，「银行就有救济手段」（`the bank has remedies`），包括「对你的负债行使抵销权」（`right of offset against your liability`）：银行管着你的现金，可以直接划走抵债。唯一的缓冲是，背靠顶级 VC 的公司一般不会被银行「先开枪再问话」（`do not shoot first and ask questions later`），但 VC 能做的也有限——因为走到那一步，VC 与放贷方的对话里「猜猜谁不在场」（`guess who's not in that conversation`）：创始团队。

收束回到哲学：债是让公司「跑得更快的额外弹药」，「不是公司的地基」（`It's not the foundation of the company`）；有时债甚至是「逃避艰难决策的藏身处」（`debt is like a hiding place`）——该做的取舍躲不掉。Bryan 的总结是：股权与债务「不是二选一」（`it's not either or`），是两件不同的工具，都要会用。

## 来源与定位

- 原始节目：[Oxide's $445M Series D](https://share.transistor.fm/s/867a87b6)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 半年多前的 C 轮专期与本期背景（`Six, seven months ago`；`we raised $200,000,000 Series C`；`we were not going to get acquired`）
  - 再融资的动因：更大的订单、backlog 与供应链需求（`we were not out seeking to fundraise`；`even bigger orders to go fill`；`our backlog had increased substantially`；`furiously building out manufacturing capacity`；`very interested in oxide`；`some very substantial supply chain needs`）
  - 融资速度、领投、超额认购与回报早期信仰者（`Got a great lead in Eclipse`；`pretty deeply oversubscribed`；`reward those folks that had been early believers in Oxide`；`can't give them the allocation that they want`）
  - 跨界与战略投资人的划分及上市目标（`investors that invest in private but also invest at public`；`crossover investors and then strategic investors`；`we anticipate being a public company`；`a generational company, and that means a public one`；`not in the foreseeable future or the immediate future`）
  - 选股东的标准与传统 VC 的局限（`how well do you know the company`；`deeper sense of conviction than just the financial returns`；`bringing less new value`）
  - Pierre 对跨界投资人的警告与 Steve 的保留意见（`do you know what crossover investors are good at`；`good at telling you what you want to hear`；`the price is the highest it will ever be`；`I think there is nuance there for sure`）
  - Atreides 的来历与「永远要赴约」（`a tradies as a big new investor`；`we met years ago was, Atreides`；`the attorneys folks`；`introduced to them by Alex Bienaek`；`a good reason to always take the meeting`）
  - AMD 作为新战略投资人（`always a bridesmaid, never a bride with us`；`Almost an Oxide investor many times over`；`invest more than they originally wanted to invest`；`happy to have AMD on the cap table`）
  - 稀释、估值与员工反应（`very minimally dilutive`；`whenever you raise, it's dilutive`；`companies can have down rounds`；`employees are pretty happy about this one`）
  - 交割与官宣的时间线（`Series D, 445 raise`；`we closed in, like, July`；`Our form d was filed in August`；`why was this announced in October`；`made sense to accommodate going through the timeline`）
  - 「盈利」作为公告钩子与交税照片（`huge shout out to Seth, Seth Winteroth`；`talk about the fact that you're profitable`；`customer related or sort of revenue related`；`Did take a photo of us paying taxes`；`we had hit profitability`）
  - 评论区跑题的招聘流程讨论（`about the Oxide hiring process`；`nine hours of live conversations`）
  - 税务第一课：不要过度优化、投资优先（`My favorite class at Kellogg was tax strategy`；`I used to help run a tax and accounting firm`；`don't waste money trying to optimize your taxes`；`investing super heavily in our technology and our team`；`the profitability that we're seeing here in 2026 is in excess of all that`；`one of our core values is thrifty`；`our headcount has grown quite a bit`；`we're investing in test facilities`）
  - OpEx/CapEx 常识与注塑改造案例（`That's deductible right away`；`you have to depreciate it over time`；`accelerated depreciation schedules`；`hiring is the best way of investing to offset tax`；`that was three d printed that we made injection molded`；`the molds were not cheap`；`it might cost a couple $100,000`；`the COGS savings is enormous`；`a cubby that does not have a sled in it`）
  - NOL 规则与演算示例（`you can only offset 80% of your income with NOLs`；`we've only spent a $100,000,000 to get the profitability`；`our NOLs are a $100,000,000`；`just using these big numbers to make all the math really easy`；`We can only use $16,000,000 of our NOLs`；`you can use your NOLs year after year`）
  - 研发税收抵免与追溯 2024（`that remaining 20% of operating income`；`Oxide has historically done and done well`；`we went back into 2024 and are doing one in 2024`；`Oxide was going to be profitable in 2026`；`Oxide was founded in 2019`；`run its course on the payroll tax offset`；`tax credits that we are going to use against our profits this 2026`；`now you're down to $1,800,000 of taxable income`）
  - 交税照片的真实性与盈利公司的稀缺（`how many racks we can actually ship this year`；`It's not gonna be a huge number, but it's meaningful`；`wire transfer to the IRS`；`CFO of a profitable venture capital backed company`；`five out of 200 companies there that are profitable`）
  - 「Amazon 不交税」类比的回应（`Amazon doesn't pay taxes`；`Amazon also was not profitable for the first many years of operation`；`they were operating a service`；`we are shipping a product`；`tax avoidance stuff is kind of shady`；`turn arbitrary accounting knobs`）
  - 债务常识与现金转换周期（`the Dunning Kruger child`；`why did you take venture capital rather than debt`；`when you borrow money, you have to pay it back`；`millions of dollars of debt one has drawn down`；`we were leveraging venture debt`；`venture debt these days and much more just debt`；`cash conversion cycle as, as tight as possible`；`Dell brilliantly had a negative cash flow conversion cycle`；`Costco very much the same way`；`borrow money to be able to buy materials`；`offset that middle period`；`customers that are not creditworthy`）
  - 强资产负债表与股权融资的目的（`you have to have money to borrow money`；`much better debt deals with a stronger balance sheet`；`to put us in a better position with respect to debt`）
  - 董事会一致性与债的第三方风险（`a partner at Lighthouse Capital`；`two parties that need to stay aligned`；`there's very little politics`；`you're adding a third party to that dynamic`；`passive and collegial`；`lose control of your own company really, really quickly`；`the cushion comes from debt`）
  - 借贷成本与机会型采购案例（`we are borrowing in the mid single digits`；`we'd be borrowing at like 10, 11, 12% easily`；`Micron basically is giving us extra allocation indirectly`；`a credit line with Western Alliance`；`Western Alliance has been a fantastic lender for Oxide`；`capitalized on a knife's edge`；`zero margin for error`）
  - 供应链挤兑背景（`once in fifty year supply chain crunch`；`can you get enough supply`；`all things kind of roll up to TSMC`；`long ahead of even having like guaranteed demand`；`the debt becomes a competitive advantage`）
  - 信用证与代工厂风险（`we use contract manufacturers`；`not getting paid for thirty days`；`give them a letter of credit to kind of make them whole`；`the letter of credit is funded by a bank`；`you don't get to overbook your deadlines`；`draw down like $25,000,000 today`；`cash collateralize your letter of credit`；`a straight fee arrangement and it's a nominal fee`；`maybe nine months ago, six months ago`；`this larger debt line with our bank in place`）
  - 条款、违约与抵销权（`profitability or revenue covenants`；`material average change clause`；`investor abandonment clause`；`the bank has remedies`；`right of offset against your liability`；`do not shoot first and ask questions later`；`guess who's not in that conversation`）
  - 债的哲学收束（`It's not the foundation of the company`；`debt is like a hiding place`；`it's not either or`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。文中税务与融资内容为嘉宾的经验分享与观点，不构成税务、法律或投资建议。
- 出场人物：主持人 Bryan Cantrill、Adam Leventhal；嘉宾 Oxide 联合创始人 Steve Tuck 与 CFO Scott Orn。官方转写页为机器转写且未标注时间戳，存在专名与数字噪声：投资方 Atreides 有时被转作 "a tradies" 或 "the attorneys folks"，信用额度（credit line）多处被转作 "deadline"，"material adverse change clause" 被转作 "material average change clause"，一笔约 220 万–230 万美元的税收抵免被连写成一串长数字（本文按其前后演算口径取约 220 万）；"Pierre Labonde"、"Alex Bienaek" 等人名以转写记音为准、未经独立核实。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
