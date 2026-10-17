---
item_id: software-engineering-daily-03d004c8f393
title: '被误读的流放岁月：NeXT 如何奠基 Mac OS X 与 iPhone'
date: '2026-10-17'
published_at: '2026-10-08'
transcribed_at: '2026-10-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/steve-jobs-in-exile/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/09/SED1971-Geoffrey-Cain-Danl-Lewin.txt'
summary: "《史蒂夫·乔布斯：流放岁月》作者 Geoffrey Cain 与 NeXT 联合创始人 Dan'l Lewin 对话主持人 Matt Merrill：流行叙事把 NeXT 讲成失败，本书以新访谈与未公开材料论证它才是隐形转折点——大学市场打法、技术押注与 IBM 一笔签了却未出货的授权，如何让 NeXTSTEP 奠基 Mac OS X 与 iPhone。"
tags: [开发者工具, 编程语言, 架构]
---

# 被误读的流放岁月：NeXT 如何奠基 Mac OS X 与 iPhone

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-10-08 · 逐字稿获取：2026-10-17 · 笔记整理：2026-10-17
>
> 全文共 24803 字 · 阅读约 63 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [编程语言](/tags/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80/) [架构](/tags/%E6%9E%B6%E6%9E%84/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/steve-jobs-in-exile/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/09/SED1971-Geoffrey-Cain-Danl-Lewin.txt)

## 速读

《史蒂夫·乔布斯：流放岁月》（Steve Jobs in Exile）作者 Geoffrey Cain 与 NeXT 联合创始人 Dan'l Lewin 本期对话主持人 Matt Merrill：流行叙事把 NeXT 讲成一场失败，这本书却以对 110 多位前 NeXT 高管与员工的访谈和未公开材料论证——NeXT 才是乔布斯生涯真正的隐形转折点。本期适合对苹果与 NeXT 技术史、面向对象编程的演化路径以及科技商业史感兴趣的读者。

最值得带走的三点：一是叙事修正——书中论证 Macintosh 当年并非商业成功，乔布斯因试图罢免自己请来的 CEO 而离开苹果，NeXT 的"失败"其实对应 NeXTSTEP 的成功：这套面向对象操作系统后来成为 Mac OS X 与 iPhone 的地基；二是技术押注——伯克利 Unix 发行版、Objective-C 与运行时动态绑定、Interface Builder 让 NeXTSTEP 领先业界 15 年以上，IBM 甚至真的授权了 NeXTSTEP，只是从未出货；三是商业教训——Cube 定价超过 1 万美元，而大学预算只有 3000 美元，不听客户导致硬件溃败，转向 OpenStep 与 WebObjects 的软件续命，最终促成 1996 年苹果对 NeXT 的收购。

## 主题正文

### 被颠覆的叙事：NeXT 不是失败，而是隐形转折点

Geoffrey 开门见山：人们对 NeXT 的集体记忆"不太对"，被流行文化和电影塑造走了形（原文锚点：`our memories have been warped by pop culture`）。流行版本是这样的：乔布斯与沃兹尼亚克在车库里创办苹果，做出了 Macintosh，乔布斯因为"太有创造力"被踢出公司，在外面流浪了十二年，办了一家失败的 NeXT，然后回归拯救了濒临破产的苹果。

而他在书中给出的"反转"版本是：乔布斯与沃兹确实创办了一家成功的公司，完成了 IPO、做出了 Macintosh，但乔布斯在公司内部并不讨某些派系喜欢——Macintosh 并非商业成功，公司持续失血、库存堆积；他最终试图罢免自己请来的 CEO John Sculley，两人被一起送上董事会，乔布斯被"流放"，去处正是 NeXT（原文锚点：`The real story is that the Macintosh computer was not a commercial success`；`he tried to oust his CEO, who he brought on`）。

NeXT 也因此不能按"失败"来读。Geoffrey 的核心论点是：NeXT 是成功的，因为它做出了基于面向对象编程的 NeXTSTEP 操作系统；苹果需要的正是一套新操作系统，而乔布斯在 NeXT 打磨近十年的这套系统，成了他回归苹果的筹码（原文锚点：`NeXT Computer was a success`；`this is the operating system that powers a lot of the Apple software today`）。他强调，乔布斯在 1987、1988 年间开发的东西，会出现在 2008 年的 iPhone 上（原文锚点：`He was developing things in the years, 1987 and '88, that would appear in 2008 with the iPhone`）。按他的说法，NeXT 岁月还是乔布斯"学会领导、学会信任与授权"的地方（原文锚点：`That's where he both learned to lead`）。

### 从 Lisa 到大学市场：救回 Macintosh 的打法

Dan'l 的讲述从苹果内部展开。他从 Lisa 项目早期就在苹果——Lisa 是 Macintosh 的前身，没有 Lisa 就没有 Macintosh（原文锚点：`the beginning of the Lisa computing project`）。他当时穿西装打领带，做面向财富 500 强的市场开拓，带过八九十家公司来看这项技术；但结论是：苹果想卖的财富 500 强对 Lisa 毫无兴趣，对方还在用大型机、用 Pascal 编程，而 SQL 数据库当年还是新概念、Oracle 还是个小初创（原文锚点：`was uninterested in the Lisa system`；`We brought 80, or 90 companies through to look at this technology`）。

他做的研究结论是：应该把机器卖给"发明这些技术的人"——大学社区不用被教育，他们会自己买（原文锚点：`we should be selling this to the people who invented these technologies`）。部门没有采纳，他因此转投乔布斯接管的 Macintosh 部门，并带着三个条件上任：可以推翻既有做法；乔布斯只在被要求时帮忙；以及先付钱——"因为我知道他是个爱插手的人"（原文锚点：`I did it with full energy and enthusiasm under three conditions`；`because I knew he was a meddler`）。

结果印证了判断：Macintosh 上市时，他们组起了 24 所大学的联合体；而当时 Macintosh 在每个经销商处每月只卖出 4 台，制造端却在爬坡到月产 8 万台、年产百万台（原文锚点：`We set up the university consortia with 24 institutions`；`Macintosh sales stalled at four units a month per dealer`；`a million units a year`）。他们有 90 天窗口去削减供应链承诺，并在 1985 年 8、9 月把约 5 万台电脑投放进大学市场——Dan'l 说这救了苹果（原文锚点：`We had a 90-day window`；`That saved Apple's bacon`）。

至于 Macintosh 为什么对计算机系不够用：初代 Mac 只有 128K 内存、没有真正的操作系统，只有 ROM 里的一堆可调用例程；而大学——主要在卡内基梅隆——想要的是"3M 机器"：百万像素的屏幕、每秒百万条指令、1 兆内存，目标成本低于 3000 美元（原文锚点：`Macintosh 128K of RAM and no operating system`；`a machine that would have a million pixels on the screen`；`It needed to cost, roughly speaking, less than $3,000`）。Dan'l 说，这正是理解 NeXT 为什么存在的关键（原文锚点：`why the company existed`）。

他反复强调一个方法论：大学不是真实世界的子集市场，而是超集——"大学里发生的事比真实世界还多"（原文锚点：`the university is a superset of the real world`）。Geoffrey 补充历史背景：早期硅谷的研究实验室与仙童半导体、英特尔等公司及联邦资金交织在一起，正是这套体系让芯片和工作站被制造出来、创造了需求——没有早期政府的参与，今天的硅谷可能根本不存在；大学是这段故事的重要部分（原文锚点：`Universities are a huge part of this story`）。

这一带的大学脉络还有两个注脚：斯坦福写过自己的分时系统 LOTS，把 Macintosh 接进 LOTS 网络的连接能力后来孵化出了 Cisco（原文锚点：`became the company known as Cisco`）；Dan'l 的大学同学 Eric Schmidt 本科时在普林斯顿带头向贝尔实验室要来 Unix，去伯克利后与 Bill Joy 把互联网协议织进伯克利发行版（原文锚点：`as an undergraduate at Princeton, Eric was the ringleader`；`they put internet protocol in the Berkeley distribution`）。

### 技术押注：伯克利 Unix、Objective-C 与动态绑定

Dan'l 说，选型在 NeXT 早期就已定下：以伯克利发行版（BSD）作为基础，大学圈也正因 NeXTSTEP 基于伯克利发行版而对它很狂热（原文锚点：`We were pretty far down the pike having selected Berkeley distribution as the foundation`；`NeXTSTEP, which was based on the Berkeley distribution`）。主持人 Matt 补充：NeXT 还挖来了在卡内基梅隆做内核研究的 Avie Tevanian（逐字稿此处转写为 "mock kernel"，通行写法为 Mach kernel——编辑注）（原文锚点：`hired Avie Tevanian for his work at Carnegie Mellon on the mock kernel`）。Dan'l 补人物线：卡内基梅隆那个项目由 Rick Rashid 主持，Avie 是他的学生，Rick 后来创办了微软研究院（原文锚点：`Rick Rashid, who was running that project and Avie was one of his students`）。这批选择的意图是灵活、可移植、多线程与并行能力，外加底层受保护的内存空间，为的是长期稳定性（原文锚点：`The idea, obviously, was flexibility, portability`）。编译器则是从 MIT 的 Richard Stallman 那里授权的（原文锚点：`the compilers we licensed from Richard Stallman at MIT`）。

语言选择是整段历史里最关键的赌注之一。Dan'l 说，William 与 Bud Tribble 参与选定了 Objective-C 与"运行时动态绑定"的组合——当时所有人都走向了 C++（原文锚点：`of objective C and the notion of dynamic binding at runtime was key`；`Everybody else had gone another direction with C++ and the rest`）。Interface Builder 也因此顺理成章：界面控件要在运行时表达自己、再绑定进系统或应用层，而不是编译了事（原文锚点：`made interface builder a rational thing to have`）。

这条线的源头是 Smalltalk——Dan'l 称它把操作系统、工作环境与用户界面融为一体（主持人确认它是最早的面向对象语言之一，Dan'l 说"就是第一个"）（原文锚点：`living, working environment and user interface all rolled into one`）。但把这套东西产品化、装进商用机器里卖是另一回事；至于把 Smalltalk 商业化的 Parcplace 为什么没成，他说当年还有过不少争论（原文锚点：`There are lots of arguments with the Parcplace folks`）。把界面构建器做进 NeXT 的关键人物来了：Jean-Marie Hullot，来自法国 Inria，通过对象社区的交往来到 NeXT 展示他的成果（原文锚点：`It was really Jean Marie coming to the company`；`he was at Inria in France`）；Dan'l 还点名一位无名英雄 William Parkhurst——做过 Macintosh 的 3D 特效、深度参与对象社区（原文锚点：`the unsung hero on the whole approach was William Parkhurst`）。

结论是时间差。Dan'l 的说法是"NeXTSTEP 是先行者"，15 年以上的领先时间，给了收购 NeXT 之后的苹果很大的跑动空间（原文锚点：`NeXTSTEP was the pioneer`；`15-plus-year lead time`）。Matt 给听众补了一个今天的注脚：iOS/Mac 开发里仍然存在的 .nib 文件，名字就来自 NeXT Interface Builder（原文锚点：`there's a file called a .nib`）。

商业模式同样是赌注。当年的工作站厂商（Sun、Apollo 等）沿袭小型机模式——买完硬件还要为操作系统付月度维护费；NeXT 采用 PC 模式：操作系统随机附带，再做"工作站级功能"（原文锚点：`you had a monthly maintenance fee for the operating system`；`We were doing PC model and workstation plus functionality`）。同时每台 NeXT 都捆绑全功能 SQL 数据库 Sybase、Mathematica（逐字稿转写作 "Richard Wolfram 的技术"，通行拼写为 Stephen Wolfram——编辑注）与莎士比亚全集，让机器出厂就带着可供他人延伸构建的能力内核（原文锚点：`NeXT software distribution bundled a Sybase database with every machine`；`We bundled Mathematica, Richard Wolfram's technology, with every machine`）。

### 识人与信任：一致公认的天赋，与学着放手

Geoffrey 说，这是几乎所有受访者最先讲的事：他坐下来采访了 110 多位前 NeXT 高管与员工，大家不约而同地说，乔布斯最大的天赋是能看穿你是谁、想要什么、擅长什么，并把你最好的工作逼出来（原文锚点：`I sat down with more than 110 former NeXT executives and employees`）。

面试问题本身就带着筛选：他会问"你是你领域里最好的设计师吗？最好的工程师吗？"——只要犹豫或答"不是"，面试立刻结束（原文锚点：`Are you the best designer in your field? Are you the best engineer in your field?`）。他找的是有意志力、能顶回来的人：在走廊里随机巡场问大家在做什么，问题很难，但不是为了刁难，而是看你能否在他面前捍卫自己的想法（原文锚点：`he would walk around the hallways randomly`）。

代价是著名的"hero-shithead 过山车"：今天你是英雄，明天你就是混蛋（原文锚点：`there was something called the hero-shithead rollercoaster`）。按受访者的观察，这是乔布斯早期在苹果和 NeXT 的样子，而他在学习驾驭这一面——不是砍树，而是让森林生长；结果是他回归苹果后获得了八年高管层的稳定，Geoffrey 反问：2026 年还有几家上市公司做得到？（原文锚点：`eight years of executive stability`）他特别强调，这个结论在他的访谈里是普遍共识，没有听到一个反对者（原文锚点：`I didn't hear one dissenter`）。

Dan'l 从内部补了细节：他离开 NeXT 时，公司超过一半的人向他汇报；高管团队所有人都参与面试每一个人（原文锚点：`We all interviewed everyone`）。简历好的人不少，真正稀缺的是对使命有"感召"的人——尤其在没人见过产品、连模型都不能展示的年代，加入全凭信念。他概括的选人标准里最后一个 C 是 character（品格），并说乔布斯确实有本事看出人的品格——当然，这种判断也来自他信任的人共同参与面试把关（原文锚点：`The last C was character`）。Dan'l 还顺带讲了那个著名的段子：乔布斯被问及微软时的回应——"成功，但他们没有品味"（原文锚点：`successful, but they have no taste`）。

Pixar 是"学会信任"这条线索的平行样本。Dan'l 回忆：1985 年创办 NeXT，1986 年初乔布斯从乔治·卢卡斯手里买下 Pixar，他当时在场——Pixar 的公司章程与 NeXT 的逐字相同，只把 NeXT 换成 Pixar，股权表、创始人股份、乔布斯的前期出资都一样（原文锚点：`In early 1986, Steve bought Pixar from George Lucas`；`The articles of incorporation for Pixar were exactly the same word for word`）。到最后，乔布斯把个人净资产的大头投进去维持 Pixar 活着（原文锚点：`Steve had put the majority of his personal net worth into keeping Pixar alive`）。但在 Pixar 他不被允许横冲直撞：只许周五到场、不许碰技术——Ed Catmull 那批人是图形奇才，而他不是那类讲故事的人；Dan'l 认为他的人性成长正来自这段经历（原文锚点：`He was only allowed in on Fridays`）。本书前言由 Dan'l 撰写，后记由 Ed Catmull 撰写（原文锚点：`I wrote the foreword thanks to Geoff. Ed Catmull wrote the afterword`）。

乔布斯的"成长"还有一组内部轶事。制造业负责人离职后换了人，新负责人拿出 "Plan 10,000"：要在弗里蒙特那座小工厂里月产一万台（原文锚点：`He put together this plan that was called Plan 10,000`）。乔布斯把活页夹放在 Dan'l 桌上问"你打算怎么卖"——Dan'l 的回应是在 NeXT 退休会上端出 "Plan One Billion"（POB，十亿美元计划）：全团队层层演示如何卖出十亿美元，最后他把打好的鸡蛋"倒进"公文包，说这东西会"像你们从未见过的那样发起来"，全场约 150 人起立鼓掌，包括看穿了这场闹剧的乔布斯（原文锚点：`It was Plan One Billion`；`Got a standing ovation from the 150 people`）。他也讲了自己怎么"顶回去"：苹果时代乔布斯在前夜搅黄了他的大学活动，第二天他当面说"我这辈子再也不会为了做正确的事而错了"，乔布斯只回了句"哦，好吧"（原文锚点：`I will never in my life ever be right for doing the wrong thing again`）。Dan'l 还转述书中 Ed Catmull 提到的说法：乔布斯后来在苹果请一些董事退任，不是因为他们不好，而是"他们不挑战我"（原文锚点：`They don't challenge me`）。

### IBM 授权案：签了字却从未出货的交易，与 Dan'l 的离开

Matt 抛出"IBM 差点授权 NeXTSTEP"的说法时，Dan'l 立刻纠正：不是差点，IBM 真的授权了，只是从未出货（原文锚点：`IBM didn't almost license NeXTSTEP. They did.`）。他还原了时代背景：IBM 推出微通道架构并与微软合建 OS/2，业界集结成 EISA 总线联盟对抗，克隆市场由此而来（原文锚点：`created the EISA bus consortium`）。IBM 高层——副总裁办公室、CEO 办公室、CFO 办公室——态度非常明确：两家设计了由同一位设计师操刀的联合标识铭板，计划造一台电脑卖向全球，把 NeXTSTEP 装上每个员工的桌面，替换掉跑在大型机上的内部邮件系统 PROFS（逐字稿转写作 props——编辑注）（原文锚点：`They designed a joint logo plate that had NeXT and IBM's logo on it`；`They were going to put NeXTSTEP on every employee's desktop`）。他说这一切发生在市面上还是 Windows 2.0 的时候（原文锚点：`when Windows 2.0 was on the market`）。

交易破裂的细节发生在 Dan'l 离开之后：当时的方案是与 Perot Systems、ESL 一起进入政府和公司市场，每台 NeXT 上的 Sybase 数据库连着 IBM 大型机，让客户在 NeXTSTEP 环境里开发大型机数据的桌面应用；IBM 愿意非独占授权，且只在 NeXT 把它授权给别人时才分享版税。而 IBM 最终走开，是因为要求 NeXTSTEP、App Kit、Interface Builder 全部跑在自己的 Unix（AIX）上——Dan'l 说这本来很容易做到，工作已经开工（原文锚点：`which was AIX, which would have been easily done`）；IBM 需要它，是因为卖政府市场要有 POSIX 标准，而当时没有。

数字在今天看来很夸张：Dan'l 招来的人要去执掌 IBM 联邦系统部门，配额是 22 亿美元——只算美国政府业务；Perot Systems 曾为海军实施完全部 6 亿美元的 PC（原文锚点：`It had a 2.2-billion-dollar quota selling to the federal government for IBM`；`Perot Systems had implemented all 600 million dollars' worth of PCs into the Navy`）。他复述 IBM 方面对他们说的话："我们与英特尔和微软失衡了，需要换个方向，你们是我们的出路"（原文锚点：`we are out of balance with Intel and Microsoft`）。他说这些往来都有白纸黑字的文件。

离开的原因他讲得很直接：交易正在崩盘，"这就是我辞职的原因"；他走后，"把乔布斯拉回理性的那座桥没了"——IBM 还打电话问他"我们怎么办"，他的回答是"祝你好运"（原文锚点：`I left and the bridge back to getting Steve to do rational things went away`）。多年后那顿离职午饭上，他给乔布斯的临别赠言是：跟你斗了一年多，你得听听身边人的话，我累了，不斗了（原文锚点：`you need to listen to the people around you`）。

### Cube：美学上的经典，商业上的溃败

先说设计。Paul Rand——今天在平面设计圈外几乎被遗忘、当年设计了 IBM、UPS、ABC 标志的大师——为 NeXT 设计了那个标志；Geoffrey 说这是书中记录最完备的故事之一（原文锚点：`designed UPS, ABC`）。乔布斯曾在访谈里形容 Rand 是"抱着泰迪熊心的坏脾气男人"（Geoffrey 说明这是转述大意）（原文锚点：`the heart of a teddy bear`）。交易条款很硬：一个标志、不许改、10 万美元，就此为止（原文锚点：`You get one logo. You can't make any changes. It's $100,000`）。这个标志常被批评太贵，但 Geoffrey 在耶鲁大学档案馆翻到 Rand 留下的餐巾纸涂稿后，找到了乔布斯 90 年代的访谈，发现这是一道商业算术题——建立一个令人记得住的品牌要 10 年以上、数亿美元，而乔布斯想要一条捷径：像"圣诞礼物上人人认得的邮票"（原文锚点：`the Yale University Archive`；`it takes 10 years or more and hundreds of millions of dollars to build a brand`；`like a stamp that you could put on a Christmas gift`）。这颗标志如今进了设计院校的课堂，NeXT 机器至今陈列在世界各地的博物馆、并在伦敦苏富比拍卖（原文锚点：`It's studied today in graphic design schools`；`it's auctioned at Sotheby's auction houses in London`）。牵线人是 Susan Kare——Dan'l 说应当把"把 Paul 介绍给 Steve"记在她的账上（原文锚点：`We should give Susan Kare the credit for introducing Paul to Steve`）。

再说商业。Cube 于 1987 年 10 月发布（原文锚点：`It was released October 1987`）。Geoffrey 查过当时的书面数字：全生命周期总销量他相信约 5 万台，其中不少是赊给经销商、并未真正收到钱的"账面销量"；按月最多年卖 300 台上下，而定价是"能让它当一台机器用"的整套配置超过 1 万美元——光学碟片本身不够用，还得配硬盘（原文锚点：`I believe the total sales over its entire lifespan were about 50,000`；`maybe 300 at the most sold per month`；`it was just over $10,000 for the package that actually worked as a machine`）。目标客户大学买家的预算从头到尾只有一句话：3000 美元以内（原文锚点：`The budget is $3,000 or less`）。

Geoffrey 的诊断是乔布斯"没有在听客户"（原文锚点：`he wasn't listening to his customers`）。例子是一家叫 O'Connor 的金融公司：他们用 NeXTSTEP 做极速交易的自定义应用，成效可观，却被绑死在 Cube 硬件上——客户要的是能移植的软件，而不是昂贵累赘的硬件（原文锚点：`a financial firm specifically called O'Connor`）。

之后的崩塌按周计。CFO Marcel Gani 是被乔布斯凌晨两点的电话招来的，条件奇特：入职前不许看资产负债表（原文锚点：`I don't want you to be able to look at the balance sheets`）。他入职打开账本才发现："这是一家已经破产的公司，我刚加入了一家破产公司"（原文锚点：`I just joined a bankrupt company`）。1993 年底，他们向最大投资人佳能摊牌 "cram down"：周末之前到账 2000 万美元，否则关门——而佳能此时已投入超过 1 亿美元，最终这 2000 万到账、硬件部门关停（原文锚点：`You've got to invest 20 million dollars by the end of the weekend`；`had invested 100 million dollars or more`）。关停消息提前一天泄露，员工在上班路上从广播里听到自己失业了（原文锚点：`turned on the radio and heard a radio announcer say`）；《财富》杂志把乔布斯称作"蛇油推销员"，说他将被历史除名（原文锚点：`Even Fortune magazine called Steve Jobs a snake oil salesman`）；约三周后，乔布斯的父亲 Paul 去世（原文锚点：`Steve's father, Paul, actually did die`）。还有愤怒的用户从硬件主管 Rich Page 那里拿到几台 Cube，拉到劳伦斯利弗莫尔实验室点火——请来了联邦政府的焰火技师，却烧不起来，因为乔布斯把它造得烧不掉（原文锚点：`they decided that they were just going to light up these cubes in flames`）。

### 软件续命：OpenStep 与 WebObjects

硬件关门后，救公司的是两笔软件生意。第一笔是 OpenStep：由 NeXT 软件负责人 Bud Tribble 主导、与 Sun 合作，把 NeXTSTEP 这一层放到 Sun 及康柏、HP 等其他厂商的硬件上（原文锚点：`it was set up by a software engineer named Bud Tribble`）。Geoffrey 说，参与者告诉他这个项目当时占到 NeXT 营收的 40% 到 50%，是救命稻草——没有 OpenStep，乔布斯根本回不了苹果（原文锚点：`it comprised about 40% to 50% of NeXT revenues at the time`；`Without OpenStep, Steve Jobs would not even have returned to Apple`）。

不过这里有一处受访者之间的分歧，值得原样保留：乔布斯对外把与 Sun 的合作讲成"Sun 押上未来赌 NeXTSTEP"，而 Sun 高管们对 Geoffrey 的回应是——乔布斯在瞎编，当时没人把 NeXTSTEP 看作未来；Sun 只是把手里的牌全摊在桌上，看什么会成为未来的软件（原文锚点：`Steve was just making stuff up`；`Sun was simply spreading its cards across the table`）。Dan'l 补了一个少被写进历史的细节：Sun 拿走的不只是软件授权，更是知识产权与专利——那是 Sun 在被甲骨文收购之前活下来所必需的（原文锚点：`they got the intellectual property, and they had the patent rights`）。至于同场竞技的 Java，Dan'l 的一句话概括是"浏览器成为平台"——Sun 当时正退出桌面工作站、全面转向服务器（原文锚点：`Java was all about the browser becoming a platform`）。

第二笔是 WebObjects。故事的前置是：万维网本身就是 Tim Berners-Lee 在一台 NeXT 电脑上写出来的，比 WebObjects 早六年——NeXT 的开发者由此意识到，Web 是 NeXT 软件的天然归宿（原文锚点：`Sir Tim Berners-Lee had created the worldwide web on a NeXT computer`）。当时的网站是静态的，想卖东西、做搜索、在买车时选颜色配置，就需要一个能自我生成、自我更新的 Web（原文锚点：`websites at the time were static`）。Geoffrey 引述乔布斯 1996 年的一个杂志访谈（逐字稿作 Wire Magazine）：技术本身不改变世界，不如专注人们的实际用途（原文锚点：`technology by itself doesn't change the world`）。WebObjects 的客户变成了戴尔、迪士尼、BBC 这样的机构，Michael Dell、Bill Gates、Larry Ellison 这些人开始敲 NeXT 的门（原文锚点：`for companies like Dell and Disney, and the BBC`）。

主持人 Matt 以开发者身份补充定位（他自陈"我可能全说错了"，Dan'l 回应"你说的在范围内"）：1995 年的 Web 开发是 CGI、Perl 的拼凑，WebObjects 却是组件化、状态保存在服务端、1995 年就有对象关系映射器——"这些东西要到 2002 年的 ASP.net 才再见得到"（原文锚点：`had an object relational mapper in 1995`）。Geoffrey 补充：苹果收购后 WebObjects 一度被冷落，直到 iTunes 出现才成为其专属软件；Matt 指出 iTunes Store 直到 2000 年代后期仍由 WebObjects 支撑（原文锚点：`WebObjects became the go-to software for that`；`WebObjects actually powered the iTunes store`）。

### 4.27 亿美元的收购：苹果为什么需要 NeXTSTEP

Matt 概括交易：1996 年，苹果在最低点买下 NeXT，得到顾问身份的乔布斯和一批 NeXT 员工，代价约 4.27 亿美元（原文锚点：`about 427 million dollars`）。Geoffrey 解释苹果为何非买不可：苹果的软件卡在上一个年代，"转球式死亡"一来，没保存的数据可能全部丢失，系统没有内存保护（原文锚点：`Apple software was stuck in the previous decade in the 1980s`；`no memory protection in the Mac software`）。替代方案 Copland 是一场灾难：约 500 名工程师各加各的功能，"featureitis"，进度要落后好几年（原文锚点：`something like 500 engineers working on Copland`；`a featureitis situation`）。

CEO Gil Amelio 与他从老东家带来的 CTO Ellen Hancock 决定收购一家软件公司。候选里有 Sun 的 Solaris，也有 Jean-Louis Gassée 的 Be——正是 1985 年接管乔布斯 Macintosh 部门的那位宿敌，乔布斯曾骂他"非常邪恶的人"（原文锚点：`Steve once called Jean-Louis a very evil man`）。Geoffrey 特别强调：NeXTSTEP 一开始根本不在名单上，而且"这件事不是单一事件、不是一通电话决定的"，故事存在多个版本；他书写的是证据最充分的那一版——NeXT 员工 Garrett Rice 打给 Ellen Hancock、并得到回音的那通电话（原文锚点：`There's not one single event that happened`；`a call from a NeXT employee in Garrett Rice, who called Ellen Hancock`）。

接下来是 Gil Amelio 口中的 "shootout"（比稿）：Gassée 与乔布斯（带着软件主管 Avie Tevanian）各做一场演示（原文锚点：`this thing called a shootout`）。Gassée 自觉胜券在握、态度傲慢，让苹果"直接买软件"；乔布斯与 Avie 在 Stanford Court 酒店的演示则大获全胜——Geoffrey 描述他在 1996 年同时播放多部电影，Matt 特别强调书中写的是约 11 部同播，苹果团队当场拍板收购 NeXT（原文锚点：`Playing multiple movies at the same time in 1996`；`something like 11 movies at the same time`；`The Apple team pretty much decides on the spot that they're going to acquire NeXT`）。

### 从 Rhapsody 到 Mac OS X：今天的代码里仍有 NeXT

回归不是童话。Geoffrey 说，乔布斯回归之初（1997 年初）苹果内部立刻爆发一场"内战"：一派要留在旧系统（blue box，旧苹果 OS），一派要走 NeXTSTEP/OpenStep API 的过渡路线（yellow box），原定 1999 年完成迁移（原文锚点：`There is immediately a civil war that erupts`；`The blue box is the old Apple OS`）。而且他并非以 CEO 身份回来：从回归到真正当上 CEO 花了大约八到九个月（原文锚点：`It takes about eight or nine months before Steve Jobs actually becomes the CEO of Apple`）。中间的转折是他一度抛售收购所得的全部 150 万股苹果股票、股价随之下跌——Geoffrey 同时强调"乔布斯没有策划这一切"，这次抛售却在无意间启动了董事会解雇 Gil Amelio 的多米诺（原文锚点：`at one point sold off all of his shares, 1.5 million shares in Apple`；`Steve didn't engineer this`）。董事会随后请乔布斯出任 ICEO——临时 CEO，Geoffrey 说这是苹果第一次用上这个 "I"（原文锚点：`what they would call the ICEO, the Interim CEO`）。Dan'l 补了一则现场轶事：Gil 曾带乔布斯一起去见 Bill Gates，事后共事者提醒他——"你请乔布斯来开会，这就不再是你的会了"（原文锚点：`if you invite Steve to a meeting, it's not your meeting`）。

之后的部分是已被写透的历史。Matt 概括 Rhapsody 是"把 NeXTSTEP 套上 Mac 皮肤"；乔布斯让 Avie Tevanian 执掌软件、Jon Rubinstein（逐字稿作 John Rubinstein）执掌硬件，把 Rhapsody 与 OpenStep 变成了 Mac OS X；WebObjects 去了 iTunes；苹果代码里到处可见的 NS 前缀就是 NeXTSTEP 的 NS（原文锚点：`There's Rhapsody, which basically takes NeXTSTEP, puts a Mac skin on it`；`to take Rhapsody and to take OpenStep and to create the Mac OS X`；`There's that NS in Apple code that you see popping up everywhere`）。Matt 感叹，这些概念熬过了公司易主、三次 CPU 架构迁移和一门新编程语言，今天仍在 Swift 里使用；至于 NS 前缀的含义，他指出业界至今存在 NeXTSTEP 与 NeXT-Sun 两种说法，并无定论（原文锚点：`They've survived a company sale, three CPU architecture changes, and a new programming language`；`Some people think it stands for NeXTSTEP`）。

Geoffrey 说写这本书像考古——技术是层层堆叠的，NeXT 本来是一层，最后却被整个叠到了苹果的最上层，苹果今天的大量软件功底正来自这里（原文锚点：`it really did feel as if you're an archeologist in a way`）。

复兴也不是一夜之间。Dan'l 强调那是多年苦役：苹果进入唱片业时放话——"不给我 99 美分一首的单曲、非要卖整张专辑，我就让我的客户去偷你的歌"；再说服乔布斯做 Windows 版 iTunes，让人们在 PC 上存音乐后发现"还是 Mac 更好用"，才把人带回 Macintosh；之后是拆解手机市场、再做 iPad（原文锚点：`If you don't give me your product in 99-cent chunk`；`convincing Steve to build a Windows app to store music`；`it was a multi-year journey`）。他借与 John Rubinstein 的对话收拢时间感：在苹果七年、NeXT 十二年、再用十年让苹果的飞轮重新转起来（原文锚点：`Seven years, 12 at NeXT and then 10 at Apple`）。

### 尾声：旅程即回报

Dan'l 引用一句常被归于乔布斯的话作结："旅程即回报"（原文锚点：`The journey is the reward`）。他数了数那一代人的名单——Gates、Ballmer、Bill Joy、Eric Schmidt、乔布斯和他自己，自称都生在 1954–1955 年前后。Matt 请他讲"最喜欢的 NeXT 故事"，他讲了世界级杂耍演员 Randy Nelson——Karamazov 兄弟的一员，自称曾在白宫和克里姆林宫表演；为了写俳句去学了日语，然后写信给 NeXT 想来教人们编程，站在开发者面前一边抛接杂耍、一边现场把对象接进系统（原文锚点：`Randy Nelson is world-class juggler`；`I juggled the White House and the Kremlin`）。Dan'l 说，"每个学科里都有这样的人"（原文锚点：`we had people like that in every discipline`）。他还提醒：1950 年代在达特茅斯的校园里，人工智能已经被一小群人讨论并命名——"那些算法是老的，我们只是终于有了能跑它们的计算机"（原文锚点：`it was on the Dartmouth campus in the 1950s that artificial intelligence was discussed and named`）。

## 来源与定位

- 原始节目：[Steve Jobs in Exile](https://softwareengineeringdaily.com/podcasts/steve-jobs-in-exile/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 流行叙事与本书的"反转"论（原文锚点：`our memories have been warped by pop culture`；`The real story is that the Macintosh computer was not a commercial success`；`he tried to oust his CEO, who he brought on`）
  - NeXTSTEP 是成功与回归筹码（原文锚点：`NeXT Computer was a success`；`this is the operating system that powers a lot of the Apple software today`；`He was developing things in the years, 1987 and '88, that would appear in 2008 with the iPhone`；`That's where he both learned to lead`）
  - Lisa 起点与财富 500 强碰壁（原文锚点：`the beginning of the Lisa computing project`；`was uninterested in the Lisa system`；`We brought 80, or 90 companies through to look at this technology`）
  - 卖给发明技术的人与三个条件（原文锚点：`we should be selling this to the people who invented these technologies`；`I did it with full energy and enthusiasm under three conditions`；`because I knew he was a meddler`）
  - 大学联合体与 Mac 销量困局（原文锚点：`We set up the university consortia with 24 institutions`；`Macintosh sales stalled at four units a month per dealer`；`a million units a year`；`We had a 90-day window`；`That saved Apple's bacon`）
  - 3M 机器与 3000 美元预算（原文锚点：`Macintosh 128K of RAM and no operating system`；`a machine that would have a million pixels on the screen`；`It needed to cost, roughly speaking, less than $3,000`；`why the company existed`）
  - 大学是超集市场与联邦背景（原文锚点：`the university is a superset of the real world`；`Universities are a huge part of this story`）
  - 斯坦福 LOTS、Cisco 与 Schmidt（原文锚点：`became the company known as Cisco`；`as an undergraduate at Princeton, Eric was the ringleader`；`they put internet protocol in the Berkeley distribution`）
  - BSD 基础与 CMU 人物线（原文锚点：`We were pretty far down the pike having selected Berkeley distribution as the foundation`；`NeXTSTEP, which was based on the Berkeley distribution`；`hired Avie Tevanian for his work at Carnegie Mellon on the mock kernel`；`Rick Rashid, who was running that project and Avie was one of his students`）
  - 内核设计目标与 Stallman 编译器（原文锚点：`The idea, obviously, was flexibility, portability`；`the compilers we licensed from Richard Stallman at MIT`）
  - Objective-C 与动态绑定（原文锚点：`of objective C and the notion of dynamic binding at runtime was key`；`Everybody else had gone another direction with C++ and the rest`；`made interface builder a rational thing to have`）
  - Smalltalk 先例与 Parcplace 争论（原文锚点：`living, working environment and user interface all rolled into one`；`There are lots of arguments with the Parcplace folks`）
  - Hullot 与 Parkhurst（原文锚点：`It was really Jean Marie coming to the company`；`he was at Inria in France`；`the unsung hero on the whole approach was William Parkhurst`）
  - 15 年领先与 .nib 注脚（原文锚点：`NeXTSTEP was the pioneer`；`15-plus-year lead time`；`there's a file called a .nib`）
  - 商业模式与随机捆绑（原文锚点：`you had a monthly maintenance fee for the operating system`；`We were doing PC model and workstation plus functionality`；`NeXT software distribution bundled a Sybase database with every machine`；`We bundled Mathematica, Richard Wolfram's technology, with every machine`）
  - 110 位访谈与识人天赋（原文锚点：`I sat down with more than 110 former NeXT executives and employees`；`Are you the best designer in your field? Are you the best engineer in your field?`；`he would walk around the hallways randomly`）
  - 过山车、八年稳定与无反对者（原文锚点：`there was something called the hero-shithead rollercoaster`；`eight years of executive stability`；`I didn't hear one dissenter`）
  - 人人面试与品格（原文锚点：`We all interviewed everyone`；`The last C was character`；`successful, but they have no taste`）
  - Pixar 平行线（原文锚点：`In early 1986, Steve bought Pixar from George Lucas`；`The articles of incorporation for Pixar were exactly the same word for word`；`Steve had put the majority of his personal net worth into keeping Pixar alive`；`He was only allowed in on Fridays`；`I wrote the foreword thanks to Geoff. Ed Catmull wrote the afterword`）
  - Plan 10,000 与 Plan One Billion（原文锚点：`He put together this plan that was called Plan 10,000`；`It was Plan One Billion`；`Got a standing ovation from the 150 people`）
  - 顶回去与"不挑战我"的董事（原文锚点：`I will never in my life ever be right for doing the wrong thing again`；`They don't challenge me`）
  - IBM 确实授权了 NeXTSTEP（原文锚点：`IBM didn't almost license NeXTSTEP. They did.`；`created the EISA bus consortium`；`They designed a joint logo plate that had NeXT and IBM's logo on it`；`They were going to put NeXTSTEP on every employee's desktop`；`when Windows 2.0 was on the market`）
  - AIX 要求与政府市场（原文锚点：`which was AIX, which would have been easily done`）
  - 22 亿配额与海军 PC（原文锚点：`It had a 2.2-billion-dollar quota selling to the federal government for IBM`；`Perot Systems had implemented all 600 million dollars' worth of PCs into the Navy`；`we are out of balance with Intel and Microsoft`）
  - Dan'l 离职与临别赠言（原文锚点：`I left and the bridge back to getting Steve to do rational things went away`；`you need to listen to the people around you`）
  - Paul Rand 与 10 万美元标志（原文锚点：`designed UPS, ABC`；`the heart of a teddy bear`；`You get one logo. You can't make any changes. It's $100,000`；`the Yale University Archive`；`it takes 10 years or more and hundreds of millions of dollars to build a brand`；`like a stamp that you could put on a Christmas gift`）
  - 标志与机器的设计遗产（原文锚点：`It's studied today in graphic design schools`；`it's auctioned at Sotheby's auction houses in London`；`We should give Susan Kare the credit for introducing Paul to Steve`）
  - Cube 发布与销量数字（原文锚点：`It was released October 1987`；`I believe the total sales over its entire lifespan were about 50,000`；`maybe 300 at the most sold per month`；`it was just over $10,000 for the package that actually worked as a machine`；`The budget is $3,000 or less`）
  - 不听客户与 O'Connor（原文锚点：`he wasn't listening to his customers`；`a financial firm specifically called O'Connor`）
  - Marcel Gani 与破产真相（原文锚点：`I don't want you to be able to look at the balance sheets`；`I just joined a bankrupt company`）
  - 佳能 cram down（原文锚点：`You've got to invest 20 million dollars by the end of the weekend`；`had invested 100 million dollars or more`）
  - 泄露、舆论与变故（原文锚点：`turned on the radio and heard a radio announcer say`；`Even Fortune magazine called Steve Jobs a snake oil salesman`；`Steve's father, Paul, actually did die`；`they decided that they were just going to light up these cubes in flames`）
  - OpenStep 的由来与营收占比（原文锚点：`it was set up by a software engineer named Bud Tribble`；`it comprised about 40% to 50% of NeXT revenues at the time`；`Without OpenStep, Steve Jobs would not even have returned to Apple`）
  - Sun 视角分歧与知识产权（原文锚点：`Steve was just making stuff up`；`Sun was simply spreading its cards across the table`；`they got the intellectual property, and they had the patent rights`；`Java was all about the browser becoming a platform`）
  - WebObjects 的起点与客户（原文锚点：`Sir Tim Berners-Lee had created the worldwide web on a NeXT computer`；`websites at the time were static`；`technology by itself doesn't change the world`；`for companies like Dell and Disney, and the BBC`）
  - 1995 年 Web 开发定位与 iTunes Store（原文锚点：`had an object relational mapper in 1995`；`WebObjects became the go-to software for that`；`WebObjects actually powered the iTunes store`）
  - 收购框架与苹果的系统困境（原文锚点：`about 427 million dollars`；`Apple software was stuck in the previous decade in the 1980s`；`no memory protection in the Mac software`；`something like 500 engineers working on Copland`；`a featureitis situation`）
  - Be 与宿敌（原文锚点：`Steve once called Jean-Louis a very evil man`）
  - 不是一通电话与 Garrett Rice（原文锚点：`There's not one single event that happened`；`a call from a NeXT employee in Garrett Rice, who called Ellen Hancock`）
  - shootout 与当场拍板（原文锚点：`this thing called a shootout`；`Playing multiple movies at the same time in 1996`；`something like 11 movies at the same time`；`The Apple team pretty much decides on the spot that they're going to acquire NeXT`）
  - 内战与 blue box / yellow box（原文锚点：`There is immediately a civil war that erupts`；`The blue box is the old Apple OS`）
  - 八九个月到 CEO、抛股与 ICEO（原文锚点：`It takes about eight or nine months before Steve Jobs actually becomes the CEO of Apple`；`at one point sold off all of his shares, 1.5 million shares in Apple`；`Steve didn't engineer this`；`what they would call the ICEO, the Interim CEO`）
  - Gil 与 Gates 会面的轶事（原文锚点：`if you invite Steve to a meeting, it's not your meeting`）
  - 从 Rhapsody 到 Mac OS X 与 NS 前缀（原文锚点：`There's Rhapsody, which basically takes NeXTSTEP, puts a Mac skin on it`；`to take Rhapsody and to take OpenStep and to create the Mac OS X`；`There's that NS in Apple code that you see popping up everywhere`）
  - NS 概念的存续与前缀之争（原文锚点：`They've survived a company sale, three CPU architecture changes, and a new programming language`；`Some people think it stands for NeXTSTEP`）
  - 考古隐喻（原文锚点：`it really did feel as if you're an archeologist in a way`）
  - 多年复兴之路（原文锚点：`If you don't give me your product in 99-cent chunk`；`convincing Steve to build a Windows app to store music`；`it was a multi-year journey`；`Seven years, 12 at NeXT and then 10 at Apple`）
  - Randy Nelson、旅程即回报与达特茅斯（原文锚点：`The journey is the reward`；`Randy Nelson is world-class juggler`；`I juggled the White House and the Kremlin`；`we had people like that in every discipline`；`it was on the Dartmouth campus in the 1950s that artificial intelligence was discussed and named`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现（如 Cube 全生命周期销量约 5 万台、月销峰值约 300 台、IBM 联邦系统部门 22 亿美元配额、佳能累计投资超 1 亿美元、苹果收购价约 4.27 亿美元、OpenStep 占营收 40%–50%、受访者"110 多位前 NeXT 高管与员工"等，均为节目口径）；本期主持人为 Matt Merrill，嘉宾为《史蒂夫·乔布斯：流放岁月》作者 Geoffrey Cain 与 NeXT 联合创始人、前市场与销售副总裁 Dan'l Lewin。
- 逐字稿中部分专名按录音转写呈现，本文保留原样并加编辑注："mock kernel"（通行写法为 Mach kernel）、"Richard Wolfram"（Mathematica 作者通行拼写为 Stephen Wolfram）、"Wire Magazine"（通行写法为 Wired）、"props"（IBM 内部邮件系统通行写法为 PROFS）、"John Rubinstein"（通行写法为 Jon Rubinstein）；OpenStep 的 NS 前缀含义在节目中存在两种说法，本文如实呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
