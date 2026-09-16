---
item_id: software-engineering-radio-442bbb3e3b51
title: Eric Tschetter 谈解耦可观测性：BI 的三层蛋糕正在重演，统一 schema 是妄想
date: '2026-09-17'
published_at: '2026-04-23'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/04/se-radio-717-eric-tschetter-on-decoupling-observability/'
source_name: 'Software Engineering Radio'
input_type: video_agent_kit_asr
summary: 'Apache Druid 原始作者、Imply 首席架构师 Eric Tschetter 论解耦可观测性：可观测性与安全就是二三十年前的 BI,正重演"竖直墙园到三层蛋糕"的演化；统一 schema 是妄想,标准化要从查询语言入手,而采样的本质是一个经济问题。'
tags: [可观测性, 架构, 数据工程]
---

# Eric Tschetter 谈解耦可观测性：BI 的三层蛋糕正在重演，统一 schema 是妄想

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-04-23 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6696 字 · 阅读约 17 分钟
>
> 标签：[可观测性](/tags/%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7/) [架构](/tags/%E6%9E%B6%E6%9E%84/) [数据工程](/tags/%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/04/se-radio-717-eric-tschetter-on-decoupling-observability/)

## 速读

Apache Druid 原始作者、Imply 首席架构师 Eric Tschetter 与主持人 Amey Ambade 谈可观测性技术的下一个形态。他的核心判断:可观测性与安全市场就是二三十年前的商业智能(BI),正在重演同一条演化路径——从 Splunk、ELK、Datadog 这类竖直整合的"墙园",走向可视化、数据层与采集层解耦的三层蛋糕;而 OpenTelemetry 已经占据了 ETL 层的位置。

最值得带走的三点:统一 schema 是妄想——"一个开发者用新理由命名一个字段,你的 schema 就毁了",标准化要从查询语言入手;数据放一处、多套查询语言当"透镜",日志、追踪与指标只是同一份数据的不同视角;采样与压缩是一条光谱的两端——采样的本质是经济问题而非技术问题。

## 主题正文

### 可观测性是什么,与"画猫头鹰"的微服务之痛

Tschetter 给可观测性的定义超出了"看日志"的直觉:观察系统内部发生了什么、理解它、并据此对系统整体采取行动,"因为事情 inevitable 会出错"。构成上是大家熟悉的三件套——日志、指标、追踪(微服务时代追踪一个请求穿过基础设施尤其重要),他额外强调了两块常被漏掉的:告警基础设施(把人拉进来响应),以及"最近才进画面、全行业都还在摸索它如何 fit 的 agentic 与 AI"。微服务让这一切更关键,他用"画猫头鹰"的梗作比:教程从两个圆圈直接跳到"画完这只该死的猫头鹰"——Kubernetes 的教程也是如此,部署完 Hello World 之后,剩下的全靠你自己。微服务带来了关注点分离与独立伸缩,但代价是"到底是系统这部分还是那部分出的问题"需要可观测性系统回答更多。（原文锚点：`there's become a need to understand how the systems are operating`；`it starts with a picture of two circles and then it goes to draw the effing owl`）

### 紧耦合的现状:墙园、组织之痛与收购的噩梦

紧耦合栈的模样人人熟悉:从"我想看日志"出发,选一个把采集、存储、UI 全包了的系统——他第一个接触的 Splunk 就是如此(forwarder 采集、数据库层、UI 垂直一体),之后 Elasticsearch 生态长出了 ELK(Logstash→Elastic→Kibana),Grafana 从指标 UI 起家后补上了日志库 Loki,并力挺 OpenTelemetry(采集日志、指标、追踪的开源 agent 体系);再往上是 Datadog、Dynatrace、New Relic 这些云厂商——"漂亮的围墙花园,数据进去就出不来"。即便 ELK 与 Grafana 开源,你也总是整套整 stack 地用。痛苦在组织规模化时爆发:新团队要 Loki+Grafana+OTel,另一个团队要 Logstash+Kibana+Elastic;微服务团队的自治权连带出"日志去哪"这类基础设施选择;企业里的"象牙塔标准派"与敏捷新团队拉锯;收购来的公司对你的标准一无所知——最终每根竖直烟囱里都有一点数据,想跨栈看全局却做不到,只能发起"既然收购了你们,就把所有日志数据搬进我们的系统"的大迁徙,并卷入政治斗争。（原文锚点：`each of these things is always vertically integrated`；`you end up with this sprawl where each independent vertically or integrated stack has some data in it`）

### 历史重演:BI 的三层蛋糕与可观测性的宿命

为什么 BI 世界早已解耦成"可视化/数据层/ETL"的三层蛋糕,可观测性却没有?他的回答是:不是没跟随,而是时间线未到——"可观测性与安全,就是二三十年前的 BI"。BI 起点是决策支持系统(Siebel、早期 SAP),当时没有数据库没有 SQL,自然竖直整合;随后解耦出报表层与关系数据库层(Crystal Reports、MicroStrategy 进场),SQL 占据主导;再后来人们发现还需要把数据搬进数据层的工具,ETL 应运而生——驱动这一切的,正是墙园之痛:收购公司后"他们的数据能通过 SQL 访问,对接就容易得多;要迁移也只换一小块,保持人们的工作流不变"。BI 明确地从竖直墙园走向了三层解耦,而"可观测性与安全正走在完全相同的路上,因为这就是竖直整合栈的自然演化"。（原文锚点：`Observability and security, our business intelligence 20, 30 years ago`；`that is the natural evolution of a tightly coupled verticalized stack`）

### 统一 schema 是妄想,统一查询语言才是解

解耦后的层次与 BI 相同,而且 OpenTelemetry 已经占住了 ETL 层——一个 collector 路由到所有系统,"这已经在发生"。尚未发生的是数据层与交互/UI 层的分离。当年 BI 靠 SQL 完成了这一步,而可观测性的数据形态不同:人们需要的是更像编程、可以迭代修改的管道式查询语言,而非声明式陈述——Splunk 的 SPL、Kibana 的 JSON 风格、Grafana/Loki 的 LogQL、Azure Sentinel 的 KQL(Kusto)、CrowdStrike 的 CQL,指标侧还有事实标准 PromQL;追踪侧则尚无一家独大的语言。关键洞察是:"不同的查询语言其实并不不同——它们都归结为同样的基本操作",这话数据库实现者都懂,但很少有系统真的在同一个数据上执行多种查询语言。（原文锚点：`Open telemetry is basically the equivalent of the ETL layer`；`they all condense down to the same basic operations`）

统一 schema 可能吗?他的回答是断然的否定:"我从根本上不相信数据会有一个通用 schema。"他把数据形状比作人类——每个新生儿都与众不同;现实是"只要有一个开发者出于新理由用 X 命名字段,你的 schema 就毁了",这种事天天发生,"相信它可实现是个愚蠢的差事,你应该假设它不可能,然后想办法应对"。正确的标准化锚点是查询语言:标准几乎总是事实标准——先被广泛采用,标准组织才围绕它建立。每个新应用都会改变数据的形状,不变的是人们想用来与数据交互的方式;墙园之所以是墙园,也正因为它们的 UI 只对着自家的数据层说话。把多种查询 API 实现在同一份数据上,多团队就能各用各的透镜:span 可以当作日志行用 SPL/LogQL 查,同一批 span 借 trace ID 组合起来就是追踪视角(计算最早最晚时间戳的差值、统计错误数);数据甚至可以一部分来自 Logstash、一部分来自 OTel、一部分来自 Splunk forwarder——只要有相同的 trace ID 就能关联;指标也能从同一份数据聚合生成。映射到 BI 的对照非常直白:Tableau 对应 Splunk UI,Snowflake 对应 Splunk indexer;Elastic 世界里 Kibana 对 Elasticsearch;Grafana 对 Loki;Datadog/Dynatrace/New Relic 的用户只看得到 UI,背后各是它们自家的"Snowflake"。（原文锚点：`I fundamentally do not believe there will ever be a universal schema to data`；`believing that that can be achieved is a fool's errand`；`the real standard is not trying to figure out how that data should be shaped, but figuring out how that data should be interfaced with`）

### 解耦的运行时:索引即透镜,检测与调查是两种负载

存储与查询引擎分离后,索引策略对齐的是你要支持的查询模式,而非数据本身——"索引是一种你放在数据上的透镜";要做全文搜索就要全文索引,否则暴力扫描就要付出遍历全部数据的 CPU 代价。解耦确实引入延迟:冷启动问题——执行查询的机器得先把数据拉过来。他把可观测数据的用例一分为二。检测(detection)是常开的:只跑在最新数据上(近 5 分钟、15 分钟、1 小时;三天前的数据就不做主动检测了),这类负载绝不能吃冷启动,值得常驻基础设施。调查(investigation)则完全不同:安全场景里告警告诉你某个可疑 IP,你要回溯"它还去过哪、干了什么",发现新 IP 再扩大搜索——"你不知道要回溯多远,也不知道要看多宽的数据"。这类负载天然适合解耦带来的弹性计算:数据放 S3/对象存储保持便宜,真要查了再拉起临时机器、填满磁盘、迭代查询、用完即弃,但要保证查询间的持续性能——"这不是查一次就完,你会一路迭代下去"。缓存的本质推力在于:100MB 数据可能只需 1MB 就能回答查询,能否只下载那 1MB 来加速冷启动、其余用时再取,是解耦架构下缓存的核心权衡。（原文锚点：`there is a cold start problem`；`you don't know how far back you're going to need to go`；`that's kind of the fundamental push and pull of what it means to cache in these decoupled architectures`）

### Druid、Lumi 与"跳过 ETL 直查对象存储"

落到自家:Imply 是 Apache Druid(分布式 OLAP)的商业公司,新产品 Lumi 是构建在 Druid 之上的日志体验——利用 Druid 内核的即时缓存、分布式查询与可用性运营能力,再加上自研的日志专用压缩与日志专用索引,并在同一份数据上实现多种查询语言,让 Splunk UI、Kibana、Grafana 乃至 Tableau、Looker、SQL 客户端都能对接——这正是"把交互层从数据层解耦出来"的产品化。采集端支持 OpenTelemetry、Splunk forwarder 与 HEC 等格式,而他看到客户最想要的路由形态是:数据已经在流入 S3、GCS 或 Azure Blob(便宜、熟悉、工具齐全),然后说"我在这儿有数据了,请让我查询它"。他的愿景是把这个再推进一步——云对象存储的廉价单位经济,叠加"所有交互层都可用"的查询能力,才能彻底打破厂商锁定。（原文锚点：`we’ve implemented multiple query languages on top of that same data`；`they already have the data flowing into some cloud object store`）

### 采样 vs 压缩:一个经济问题

采样的本质被他一语道破:"任何你决定丢弃的数据,都是你在今天断言将来永远不需要它。"赌对了,这是最经济的选择;赌错了——他举了追踪场景的例子:用户说出了问题,开发者去查追踪却"没有这回事",因为那一次用户体验没进采样;这种事积累多了,用户坚称系统坏了而开发者坚称一切正常,"你就再也无法搞清这个系统了"。另一个新变量是监管:被法规要求必须保留的数据不能采样掉。所以采样"根本上是经济问题,不是技术问题"——技术只是应对成本的简便答案。它与压缩构成一条光谱的两端:压缩让单位成本下降、数据可保留可查;而如果你百分之百确定不需要,那就扔掉,别客气。（原文锚点：`any time you choose to throw data away, you are making a choice today that you will never need that data`；`It's really an economic question more than it is an actually meaningful technological question`）

### 成功标准、治理与迁移路径

可观测性系统自身的可观测性是"乌龟叠乌龟":Imply 用自己的产品观测自己的产品,递归到某处总有一个系统把遥测发给自己;自建的团队最终也会走到这一步。解耦的成败标准被他定义得极其朴素:数据放进一个地方之后不需要再搬家,多个团队无需学习新工具就能继续用各自的工具、并且看到了更多数据——那就是成功;反之,若数据集中后每个团队都得学新工具、改工作流,那就是失败。成本上解耦理应更省(减少重复存储、更有效压缩、更充分利用 CPU);治理上则要有两手:访问控制之外还要基础设施隔离——业务分析师与安全/可观测性团队的查询模式天差地别,要防"吵闹的邻居"占满 CPU。至于"倔强的团队坚持要用 Grafana"?"那正是成功的定义"——Grafana 团队、Splunk 团队、Kibana 团队应该都能看到同一份数据、保留各自的工作流。什么时候不该解耦?只有小规模:三个人的团队,挑一个竖直方案直接跑就好;数据孤岛与倔强用户的痛苦,是随规模增长的。迁移路径则是渐进的:从"一个墙园里没有、但很想要的数据集"开始,放进解耦世界并让它在墙园里可用——证明不影响任何人的工作流之后,再逐步扩张,先补新数据集还是先解锁被锁住的旧数据,完全可以按案例决定,快慢由团队自定。技能方面,买商业产品就无需操心;自己干则需要数据系统与分布式系统的知识——好在微服务时代 these skills 正在普及。他给评估者的一条建议是个思想实验:"想象一下,如果那个数据集突然可以开放给更多团队,会变成什么可能?"——解耦是必然的方向,"这是事情自然要去的地方"。（原文锚点：`you were able to put the data in one place and you don’t have to move that data`；`it should allow for reducing duplication of storage`；`The only time when it could maybe not make sense is actually at a small scale`；`think about what do you think could become possible`）

## 来源与定位

- 原始节目：[SE Radio 717: Eric Tschetter on Decoupling Observability](https://se-radio.net/2026/04/se-radio-717-eric-tschetter-on-decoupling-observability/)
- 定位：时间戳取自 ASR 逐字稿。
  - 可观测性定义与"画猫头鹰"的微服务之痛（00:00:59–00:04:44）
  - 紧耦合栈：Splunk、ELK、Grafana 与云厂商墙园（00:04:44–00:07:32）
  - 组织之痛：自治团队、象牙塔标准与收购噩梦（00:07:32–00:10:44）
  - BI 的演化史：从决策支持系统到三层蛋糕（00:10:44–00:14:27）
  - OpenTelemetry 占位 ETL、管道式查询语言百家争鸣（00:14:27–00:18:16）
  - 多语言同数据、trace ID 关联与 BI 对照（00:18:16–00:21:17；00:27:02–00:31:50）
  - 墙园经济学与数据孤岛（00:20:14–00:21:17）
  - schema 之辩：统一 schema 是妄想、标准化在查询语言（00:21:44–00:27:02；00:32:14–00:33:26）
  - 索引即透镜、冷启动与检测/调查两种负载（00:33:32–00:39:20）
  - 缓存的推力与 Druid/Lumi 的多语言实现（00:39:22–00:45:56）
  - 对象存储直查的愿景（00:43:40–00:45:56）
  - 采样 vs 压缩光谱与经济本质（00:46:01–00:48:14）
  - 自观测递归、成功标准、治理与迁移路径（00:48:41–00:59:20）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 嘉宾姓名（Eric Tschetter）与主持人（Amey Ambade）按节目出版方元数据核正；KQL、PromQL、OpenTelemetry 等专名按公开名称校正。
- "一至两个数量级""600 个检测器"等表述均为嘉宾口述口径，本文未独立验证；对 Imply/Lumi 产品的介绍按嘉宾身份（Imply 首席架构师）保留其立场归属。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
