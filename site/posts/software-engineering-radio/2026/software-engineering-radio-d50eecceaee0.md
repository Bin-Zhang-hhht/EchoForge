---
item_id: software-engineering-radio-d50eecceaee0
title: Martin Dilger 谈事件溯源：先建模后建码、切片化架构与"默认即事件溯源"的逆主流立场
date: '2026-09-17'
published_at: '2026-05-13'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/05/se-radio-720-martin-dilger-on-understanding-eventsourcing/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/05/se-radio-720-martin-dilger-on-understanding-eventsourcing/'
summary: '《Understanding Event Sourcing》作者 Martin Dilger 讲透事件溯源与事件建模：切片化架构的两类模式、持久化投影消灭耦合、事件版本化与 upcaster,以及三个鲜明立场——Kafka 不是事件存储、事件溯源应当是默认选择、代码复用在该架构中并不存在。'
tags: [软件工程, 架构, 事件驱动]
---

# Martin Dilger 谈事件溯源：先建模后建码、切片化架构与"默认即事件溯源"的逆主流立场

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-05-13 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 7861 字 · 阅读约 20 分钟
>
> 标签：[软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) [架构](/tags/%E6%9E%B6%E6%9E%84/) [事件驱动](/tags/%E4%BA%8B%E4%BB%B6%E9%A9%B1%E5%8A%A8/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/05/se-radio-720-martin-dilger-on-understanding-eventsourcing/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/05/se-radio-720-martin-dilger-on-understanding-eventsourcing/)

## 速读

Nebuilt GmbH 创始人、《Understanding Event Sourcing》作者 Martin Dilger 与主持人 Giovanni Asproni 系统梳理事件溯源(Event Sourcing)与事件建模(Event Modeling):前者换掉"只存现状不存历史"的存储方式,后者用一条从左到右的时间线让业务与工程找到共同语言——他甚至直接用事件模型生成代码。

最值得带走的三点:切片化架构里只有两类模式(状态变更与状态视图),系统像乐高一样拼装,新增功能只是新增切片,成本曲线是平的;持久化投影让每个用例拥有自己的"客户表",耦合问题随之消失;以及三个鲜明立场——Kafka 不是事件存储、事件溯源应当是默认选择而非特例、切片化架构中"代码复用"并不存在,复制粘贴是被鼓励的。

## 主题正文

### 事件溯源是什么:从"存对象"到"存历史"

Dilger 开门见山:事件溯源从技术上看"只是另一种存储和处理信息的方式"。典型 CRUD 架构存储的是没有任何历史的结构化对象;事件溯源把这一切翻转——用事件的形式记录系统里发生过的整段历史。他的例子是正在做的法律信息系统:打开新案件时,不再是往 cases 表里插一行,而是存一条"案件已创建"(case created)事件,谁在什么时候创建了哪个案件,完整可查。他也吐槽"事件"这个词被用滥了:"问两个开发者,你至少会得到三个答案"——event streaming、event storming、event driven、event modeling 各有所指。他强调自己说的 event 根本不是技术术语:事件就是"从业务视角看,系统里发生过的一件事",是一个事实,任何业务人员都能立刻理解。（原文锚点：`it's just a different way to store information and to process information`；`an event is just something that happened in the system from a business perspective`）

### Event modeling:让沟通问题消失的协作建模

event modeling 是"任何信息系统的起点",与 event storming 同属协作建模技术,区别在于它沿一条单一时间线展开,从左到右像讲故事一样一步步呈现系统——"每个人都知道怎么从左往右读"。他回顾二十年行业生涯的顿悟:"我们项目里面对的问题,从来都是沟通问题,从来不是技术问题。"把人尽早聚到一起、逼他们真正对话并找到共同语言(也就是 DDD 说的 ubiquitous language),很多问题会自己消散。事件模型还是事件溯源系统的完美蓝图,映射简单到"可以直接从模型生成代码"——他与客户建模完成后,经常直接生成代码。更根本的一点:业务人员从不思考表和类,他们思考的是过程;而事件让开发者也开始思考过程——"这个发生了、然后那个发生了、然后用户注册了、通知发出了",自然语言讲出来的故事可以直接映射到事件溯源系统。（原文锚点：`it was always communication, it was never technology`；`we used the event model directly to generate code from this`）

### 切片化架构:状态变更与状态视图,像乐高一样拼系统

Dymitruk 说事件溯源靠两个核心模式,Dilger 更愿意说四个,但本质一致:把系统分解成极小的切片(slices),切片只有两种。状态变更(state change)切片解决"信息怎么进来":典型的是一个屏幕、用户点一个按钮、发出一条命令(command),一切顺利则系统里多了一条新事件。状态视图(state view)切片解决"信息怎么出去":把系统里已有的事件投影给下一个屏幕或后台过程。"世界上任何系统,无论多大多复杂,都可以拆成状态变更与状态视图,像乐高积木一样拼起来。"他的最大心得是:软件里几乎所有事情都不复杂,看起来复杂只是因为没拆——"一千人天"的故事拆开就是一千个微小的步骤,每一步都很简单。（原文锚点：`state change slice`；`state fuse slice`；`like Lego bricks, that's basically your system`；`it's just 1000 tiny steps in this process`）

他随后完整演示了 event modeling 工作坊的流程:第一步头脑风暴,30 个人把 100 到 500 个事件贴上白板——这一步已经在塑造 DDD 所说的统一语言,因为人们生平第一次开始争论"这个东西到底该叫什么";第二步故事板,把事件云排成顺序,系统的故事和体量立现;第三步画屏幕,这是与 event storming 的关键差异,也是让业务与非事件思维者跟上的锚——他有条著名规则:"画一个屏幕如果超过两分钟,你绝对做错了",丑屏幕是必修技能,UX 同事起初会恨你;然后才定义命令与读模型:命令是发给系统的指令(如"注册用户"),背后是一堆业务规则的校验,成功执行即产生新事件;读模型(事件模型里的绿色便签)则是把已有事件投影成屏幕要显示的信息。整套方法追求的是"信息完整性"(information completeness):每一步都明确信息从哪来,错误的假设在项目最早期就暴露,而不是等到预算排完、冲刺排好才发现走不通。（原文锚点：`putting sticky notes on a giant whiteboard`；`If it takes you more than two minutes to draw a screen, you are absolutely doing it wrong`；`this is what we call information completeness`）

### 时间维度、事件流与持久化投影

书里有一个观点:事件溯源为系统加上了时间的维度。传统架构里,用户表没有任何历史——是谁注册的?手动还是自动?被改过几次?这些信息在摊平进关系模式时全部丢失;运气好可以去翻日志或 temporal tables,但他见过的大多数客户对"你们常用 temporal tables 吗"的回答是"从来不用,因为不好用"——他紧接着的类比是"那你们常用备份吗?也从来不用"。而事件溯源把"如何走到今天"变成架构的一等公民:有客户跑了十多年,系统诞生以来每个决策都以事实形式存着,"那是信息金矿;如果你只存现状而故意扔掉历史,我永远无法理解"。对"数据会无限膨胀"的担忧,他的回答是按业务流程切流:每个客户的事件流通常只有 10 到 100 条事件,流沿着业务过程定义(客户注册是一个流、电商的购物车会话是一个流);聚合(aggregate)则是流的保护者——命令进来先由聚合校验"执行之后系统是否仍然一致"。流之间的依赖,团队通常想到 saga 模式,而他自己从不用:事件建模里的"自动化"(automation)就是一个把信息从一条流搬运转换到另一条流的小过程,"你可以叫它微型 saga"。（原文锚点：`informational gold that they have there`；`Maybe it's 10, 15, 20, 30 events`；`this aggregate is basically a protection for your stream`；`you could call it the tiny little saga`）

性能是必被问到的问题,而答案打破了一个普遍误解:不是每次查询都去重放全部事件——实践中的标准做法是持久化投影(persistent projections)。每来一条新事件,就更新到一张关系表里;运行时的读路径与任何传统架构无异,还是"查客户表",只是那张表不再是真相源,而是事件的一层投影;需要新信息时,随时为新用例再建新投影。这还带来调试超能力:想看系统在十天前的状态,用事件重建当时的投影即可——"你确切知道用户点这个按钮时系统处于什么状态,问题在哪一目了然"。更深的收益是解耦:传统架构里所有用例共用一张客户表,改一个用例要回归测试所有用例;事件溯源为每个用例定义专属投影,"不是一张客户表,而是许多张更小的客户表",耦合问题随之消失。（原文锚点：`this can be a relational table for example`；`it's not your source of truth, the customer's table`；`you can just build a new projection out of it`；`It doesn't need everything in this table`）

### 事件演化、Kafka 误区与"默认即事件溯源"

事件随时间演化怎么办?他的处理顺序固定:先问"这真的是对既有事件的结构性修改,还是一个新事件?"——比如客户地址要加邮编字段,也许更该引入一条"邮编已添加"的新事件,只要它有真实的业务含义,新增事件永远是首选。确实需要改结构时,就给事件做版本(CustomerRegistered v2),逐步把依赖它的投影迁移到新版本,再由称为 upcaster 的小基础设施把 v1 转成 v2,系统从此只面对 v2。upcaster 会不会越积越多?实践中不会——业务过程非常稳定,而"我们建模讨论的正是业务过程";技术细节变得快,过程不会。就算改一个事件,影响也被限制在极小的范围内,不像改关系模式那样波及全系统。（原文锚点：`a postal code added event`；`a customer registered v2`；`the concept is called an up caster`）

采用之难,他的观察是"大多数公司对事件溯源怕得要死"——"我们试过一次,惨败,再也不碰了"。深挖下去几乎都不是事件溯源本身的问题,最典型的元凶是:"我们用 Kafka 当事件存储。"他的态度斩钉截铁:Kafka 既不是事件存储,也不适合事件溯源——它是事件流平台,是"系统之间的高速公路",以光速把信息从 A 搬到 B;而记录系统内部的决策与历史是另一回事。"请千万不要把 Kafka 当事件存储。"更进一步,他摆出了一个与业界主流相反的立场:主流说"默认 CRUD,只有受监管、需审计等特殊场景才用事件溯源";他主张事件溯源永远应该是默认——"因为它是一种更简单的建系统方式"——只有在非常明确的纯表单类应用里才退回 CRUD,而且"那些表单迟早会长成真正的应用,那时你还是会受益于事件溯源"。嵌入式、算法类系统则确实不适合;事件溯源的高光地带是信息管理系统:信息进入、转换、多路使用、需要沿时间线追踪。（原文锚点：`Kafka is neither an event store nor is it suitable for event sourcing`；`It's your highway between systems`；`please don't use Kafka as an event store`；`event sourcing is always the default`）

### Unlearning、平坦成本曲线,与"切片周期时间"度量

权衡与起步建议里最诚实的一段是心态:命令团队"从明天起改用事件溯源"注定失败——他自己花了近两年才摆脱旧观念,"最难的部分通常是真的要忘掉学到的东西";过去的最佳实践在这种架构里恰恰是要预防的问题。基础设施门槛倒是很低:Postgres 甚至 SQL Server 就能当事件存储,很多客户就这么跑;等到规模真的大了、数据库慢了,再评估商业产品,而多数系统永远到不了那个规模。需要忘掉的最佳实践中他挣扎最久的是代码复用:切片化架构里复用"基本不存在",五年没用过抽象类——DRY 在独立切片之间不成立,切片之间就是复制代码,"这完全没问题";如今复制粘贴意味着用 AI 生成,"复制粘贴的加强版",而且 AI 会告诉你改动会波及哪两三个投影——"这真的不再是个问题"。（原文锚点：`It also took me almost two years`；`the hardest part with this is typically really unlearning`；`It's basically, it's non-existent in my projects`；`copy paste on steroids`）

对业务方,他给出的价值论证直击行业痼疾:传统架构在绿地期很轻松,但耦合随时间累积——后期每加一个功能都要连着改五个别的功能,晚期开发贵得吓人,"这个问题困扰了我们二十多年"。切片化架构里任何新功能都只是一个新切片:成本曲线是平的,没有曲棍球杆式的指数增长;切片像系统内部的微型微服务,需求不变就不碰。时间到市场快得惊人,而且与 AI 是天作之合——"你的编码 agent 永远不需要理解整个代码库,它只需要理解一个切片,可能就五个类",再也不需要百万 token 的上下文窗口。落地路径:第一步永远是事件建模而不是事件溯源(用 event storming、domain storytelling 也行,对现有 CRUD 系统建模就能立刻受益);然后挑一个最有把握的小流程做概念验证,蓝图架构自己搭——.NET 生态用 Marten 和 Wolverine,JVM 上常见 Axon,自研框架也没问题,"借助 AI 一两天就能搞定";他见过"两天建模、第三天开始建、两天内系统上生产"的速度,而且业务与工程共同建出的系统,往往正是业务真正需要的。遗留系统现代化他用 AI 从两头抽取事件模型:让 agent 分析既有代码库,同时让 agent 走一遍 UI、把截图直接放进事件模型——"你无法现代化你不理解的东西,那是注定失败的"。greenfield 也可以增量:先高层建模,挑一个最有把握的小工作流(注册功能,可能就五个切片)做到生产,再按模型挑下一个过程,方向错了随时可以调,因为一切以切片为单位。测试则重度依赖 BDD:在事件模型里用业务人员定义的 given/when/then 规则生成可执行规格——"测的是业务定义的真实业务规则,而不是测试无关紧要的技术单元"。度量上他只推一个指标:slice cycle time——建一个切片要多久(典型从两三天,借助 AI 更短,逐渐缩到半天,含 UI),切片按生产就绪标准交付,就能一天多次持续上线;最后给团队的建议是一个"FedEx day":用一天时间建模加交付,你会对自己能做到的事感到惊喜。（原文锚点：`any new feature is typically just a new slice`；`The cost curve is very flat`；`It just has to understand one slice`；`You cannot modernize what you don't understand`；`I call it the slice cycle time`；`it's called a FedEx day`）

## 来源与定位

- 原始节目：[SE Radio 720: Martin Dilger on Understanding Eventsourcing](https://se-radio.net/2026/05/se-radio-720-martin-dilger-on-understanding-eventsourcing/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 事件溯源的定义、法律系统案例与事件术语之乱（`it's just a different way to store information and to process information`；`an event is just something that happened in the system from a business perspective`）
  - 沟通才是问题、事件模型单时间线与直接生成代码（`it was always communication, it was never technology`；`we used the event model directly to generate code from this`）
  - 两种切片与乐高式组合、千人天问题的拆解（`state change slice`；`state fuse slice`；`like Lego bricks, that's basically your system`；`it's just 1000 tiny steps in this process`）
  - 工作坊七步：头脑风暴塑造统一语言、故事板与两分钟屏幕规则（`putting sticky notes on a giant whiteboard`；`If it takes you more than two minutes to draw a screen, you are absolutely doing it wrong`；`this is what we call information completeness`）
  - 时间维度、temporal tables 的尴尬与信息金矿（`informational gold that they have there`）
  - 事件流、聚合保护与微型 saga（`Maybe it's 10, 15, 20, 30 events`；`this aggregate is basically a protection for your stream`；`you could call it the tiny little saga`）
  - 持久化投影、按时间重建投影与按用例解耦（`it's not your source of truth, the customer's table`；`you can just build a new projection out of it`；`It doesn't need everything in this table`）
  - 事件演化：新事件优先、版本化与 upcaster（`a postal code added event`；`a customer registered v2`；`the concept is called an up caster`）
  - Kafka 误区与"事件溯源应是默认"的逆主流立场（`Kafka is neither an event store nor is it suitable for event sourcing`；`event sourcing is always the default`）
  - 两年 unlearning、复用不复存在与"加强版复制粘贴"（`the hardest part with this is typically really unlearning`；`It's basically, it's non-existent in my projects`；`copy paste on steroids`）
  - 平坦成本曲线、AI 只需理解一个切片与遗留现代化（`any new feature is typically just a new slice`；`The cost curve is very flat`；`It just has to understand one slice`；`You cannot modernize what you don't understand`）
  - BDD 可执行规格、切片周期时间度量与 FedEx day 收尾（`I call it the slice cycle time`；`it's called a FedEx day`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 文中"两天内上生产""切片周期时间缩至半天"等为嘉宾口述的实践口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
