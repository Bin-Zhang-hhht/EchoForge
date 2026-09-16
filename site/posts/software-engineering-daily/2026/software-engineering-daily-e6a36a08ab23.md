---
item_id: software-engineering-daily-e6a36a08ab23
title: 数据库不再只给精确答案：Google 数据库掌门人的 AI 时代答卷
date: '2026-09-17'
published_at: '2026-09-15'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/inside-googles-database-infrastructure-for-the-ai-era/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1960-Google-Databases-2026.txt'
summary: 'Google 数据库工程 VP Sailesh Krishnamurthy 谈数据库五十年教条如何被 AI 撬动：Spanner Omni 的单二进制与 TrueTime 取舍、Spanner Graph 反洗钱实战、AlloyDB 过滤向量检索，以及 Agent 直连生产库时把授权写回数据层的 PSV 方案。'
tags: [数据库, AI Agent, 开发者工具]
---

# 数据库不再只给精确答案：Google 数据库掌门人的 AI 时代答卷

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-09-15 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 9218 字 · 阅读约 24 分钟
>
> 标签：[数据库](/tags/%E6%95%B0%E6%8D%AE%E5%BA%93/) [AI Agent](/tags/AI%20Agent/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/inside-googles-database-infrastructure-for-the-ai-era/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1960-Google-Databases-2026.txt)

## 速读

Google 数据库工程 VP Sailesh Krishnamurthy（AWS Aurora 老兵，现在同时管 Google Cloud 事务型数据库和全 Alphabet 的运营型数据库）与主持人 Matt Merrill 长谈一场：数据库五十年的两条铁律——别丢数据、给精确结果——正在被 AI 撬动，数据库越来越像搜索，卖的是"最相关的结果"而非"精确的答案"。

最值得带走的三点：Spanner Omni 把整套系统折叠成单二进制搬进客户机房，靠的是"外部世界的时间精度约等于 Google 2012 年"这个判断；反洗钱场景里 PageRank 直接跑在事务库上，不用再搭 ETL；Agent 直连生产库的真正底座，是把散落在应用 WHERE 子句里的授权用参数化安全视图写回数据层。

## 主题正文

### 五十年数据库教条，被 AI 撬动

Sailesh 90 年代中期从 IBM Db2 入行，Berkeley 读博做流式数据库，创业公司卖给 Cisco 后去 AWS 带 Aurora MySQL，2019 年加入 Google。他给自己总结的"数据库教条"（database dogma）五十年没变过：声明式地说要什么，系统负责做到，期间别丢数据、给精确结果。他还给了一个连环提醒——性能劣化拖长了就是可用性事件，可用性事件拖长了就是持久性事件，三者深度耦合。（原文锚点：`Database dogma is really being focused on specify what you want`；`A long-duration performance event effectively becomes an availability event`）

真正的变化是最近三四年：结构化与非结构化数据合流，应用开始期待把两者放在一起查询，数据库世界开始长得像搜索世界（学术一点说就是信息检索）——从只产精确结果，转向产"最好的、不精确的"结果，相关性和排序成了新的核心指标。他同时强调另一个背景变化：今天的 enterprise IT 早已不是买套装软件顺带装数据库的那个世界，开源把最佳实践带了过去，客户自己就是创新者。（原文锚点：`it's no longer just enough to not lose your data and produce exact results`；`the confluence of structured and unstructured data`；`Enterprise IT, I talk to customers all the time, just incredibly creative`）

### Spanner：广告分库之痛、选型逻辑与 Omni 的工程取舍

Spanner 的起源是 Google 广告系统：跑在分片 MySQL 上，每年都要为下一年的增长重新规划分片，团队最终认定"这是个必须下车的仓鼠轮"。它要同时满足三件事——企业应用的功能（二级索引、事务）、Google 级的规模、再加上全球部署，此前没人把这三样一起做成过，2012 年广告系统率先上生产。（原文锚点：`The ad system used to run on sharded MySQL`；`this is a hamster wheel that they had to get off`；`no one had figured out how to solve all these three together`）

至于日常开发者何时该用它，他的回答很克制：单机就能跑的东西，Postgres 足够好；Spanner 的位置是全球多区域同步容灾、极致弹性伸缩，以及在一个系统里同时要关系、图、全文、向量的多模型场景——他坦承多模型这块"我们可能略微超前于时代"，Postgres 生态也在长出同样的能力。（原文锚点：`if what you're trying to do is something that will run in a single node, Postgres is just fine`；`you can have a graph database, you can have full-text search, you can have vector search`）

新发布的 Spanner Omni 让客户在自己的机房甚至其他云上跑 Spanner，工程上约两年交付。动机很现实：受监管客户的数据驻留与退出选择权（他引了一位银行客户的抱怨——从两个半九的系统迁到四五个九的系统，监管反而要他论证合理性）；以及 AI 时代客户在多家云、neocloud 之间抢容量，"皇冠珠宝留在自己数据中心"是 2025、2026 年的真实生态。打包方式上最大的取舍是把 Google 内部大量微服务折叠成单个二进制（主要是 C++），下载就能跑。（原文锚点：`I know that I'm considering moving from a system which gives me two and a half nines`；`their crown jewels will remain in their data center`；`we collapsed it all into a single binary`）

最硬的两块积木是存储和时间。存储靠 Google 内部的 Colossus：扩缩容分裂合并时只需要复制元数据而不是数据，他认为这是 Spanner 和 Bigtable 领先其他横向扩展系统的"超能力"。时间就是著名的 TrueTime——靠数据中心里的原子钟把时钟偏差（epsilon）压到极低，从而控制提交等待；离开 Google 机房后，他的判断是外部世界今天的时间原语"大约相当于 Google 2012 年内部水平"，而 Spanner 恰好是为那个年代设计的，配套的软件定义 TrueTime 让 Omni 在外部基础设施上"对很多场景足够好"。他甚至说有客户问能不能也装原子钟——"来聊，我乐意支持"。（原文锚点：`We only have to copy metadata`；`to be able to talk about what we call the epsilon`；`the world outside is kind of like the world inside Google in 2012`）

### Spanner Graph：把 PageRank 搬进反洗钱生产线

Spanner 的图能力走的是"覆盖层"路线：一条 `CREATE PROPERTY GRAPH` 的 DDL，把既有关系表建模成图视图，数据不动、仍然声明式查询。这解决的是"关系数据上问关系问题"的老矛盾——过去要么搭一条 ETL 管道把数据搬去图系统，要么放弃这类问题。（原文锚点：`You have a DDL command that says create property graph`；`By the way, it's still declarative. The database dogma is not lost.`）

他给出的最完整案例是金融反欺诈：复杂的洗钱和合成身份欺诈往往是一张不断变形的合谋账户网络，孤立分析单笔交易看不清全局。做法是把账户作为节点、交易作为边，在 Spanner 里原生跑社区发现算法（弱连通分量、模块度聚类）找出可疑簇，再对簇内节点跑 PageRank 找关键账户——PageRank 虽然为网页而生，找网络中心节点照样在行。印尼支付平台 DANA Pay 用这套做反洗钱，价值在于实时：能在交易链路里直接标记甚至拦截，而不是事后批处理。（原文锚点：`Sophisticated fraud, like money laundering or synthetic identity fraud, often involves networks of colluding accounts`；`although PageRank was originally for web pages, it's actually really very, very good at identifying who are the most influential nodes`；`DANA Pay. It's an Indonesian digital payment solution`；`if I can flag and block the transaction, I can prevent financial losses`）

### 向量检索别拆出去：AlloyDB 的过滤向量检索

聊到"AI 创业标配 Postgres 加 pgvector"，Sailesh 先夸 pgvector 和 HNSW 对多数场景够用，然后介绍 AlloyDB 里塞进的 Google 自家 ScaNN（YouTube、搜索内部用了十几年的向量检索技术，节目称可扩展到百亿级向量）：官方口径是内部测试中向量查询比 HNSW 快 6 倍、内存省 4 倍，接口刻意做得和 pgvector 兼容。这些数字是厂商测试口径，听听即可；他还坦承不确定其中 HNSW 的改进是否回馈了上游。（原文锚点：`we have this amazing technology called ScaNN`；`we can get 6x faster vector queries than HNSW, PGVector, and standard Postgres`）

真正有普适价值的是他讲的"过滤向量检索"难题：现实查询几乎从不只有向量一个谓词，总要多带一个"价格低于 50"之类的过滤条件。先探向量索引再过滤，可能翻页翻到地老天荒；先按标量索引预过滤，又可能面对百万级候选集没法做近邻。AlloyDB 的做法是让多个索引同时被探测、在飞行中自适应决定先探哪个。他的更大论点是：把向量系统拆成独立组件是"很糟糕的主意"——跨系统拼接的预过滤/后过滤没人做好，而查询只会越来越复杂，混合检索（向量加全文）紧随其后。（原文锚点：`We call this filtered vector search`；`we can actually probe both of them at the same time`；`it's a really poor idea to go build a completely separate vector system`）

### 激活存量数据库：上下文比 schema 更稀缺

面对"Agent 都自己写查询了，schema 设计还重要吗"，他的答案分三层。第一层：存量应用不会一夜消失，紧急问题不是改 schema，而是"点亮"既有数据库供 Agent 使用。他给出 agentic data cloud 的三要素——AI 原生基础设施（图、向量、全文）、无边界（跨云 lakehouse、两个 Omni）、信任。（原文锚点：`we think there are three important pieces`；`just the schema itself is actually not even enough`）

第二层是本期最被低估的观点：对 Agent 来说，schema 本身根本不够，稀缺的是 schema 周围的上下文。他举的例子很具体——账单地址和发货地址两列，其中一列为空时隐含"两者相同"的业务知识，这不在 schema 里；city 列里到底存的是小写全名还是三字机场代码，Agent 生成 SQL 前必须有人告诉它。他甚至翻出三十多年前 Db2 时代觉得多余的 SQL COMMENT 语法：如今记录语义的元数据突然值钱了。（原文锚点：`If I have a table with a billing address and a shipping address`；`the values in the city column, are they in lowercase? Are they three-letter airport codes?`）

第三层是应用形态的演变：他预期会出现"临时工作流"式的新应用——知识工作者让 AI 现场组合系统 A 和 B，应用本身没有四壁，轨迹和中间状态都要落到数据系统里；现有系统会因此被逼出弹性（他举的例子是连续三个月每周在不同东南亚国家旅居时，给银行设二十条欺诈警报会把系统噎住），schema 或许要变得更前瞻。写操作他持保守态度：眼下大家默认 Agent 只读，写应该走"提案"而非直接落库。生态侧的落点是开源的 MCP Toolbox 和托管 MCP 服务（企业级治理、直连控制平面建库部署），他团队自己的应用已经能根据用户请求连接 MCP 服务器动态生成 UI。（原文锚点：`applications are ephemeral workflows. The application as such doesn't exist`；`I want a fraud alert. I want one week in Vietnam`；`You make a proposal for a change`；`we're able to generate UI on the fly by connecting to these MCP servers`）

### Agent 直连生产库：把授权写回数据层，然后拥抱混沌

LLM 连上生产数据库怎么控制爆炸半径？他先讲了一个结构性断层：分析库世界里，业务分析师带着自己的凭证连接、系统内有访问控制；而三层 Web 架构之后，运营库的最终用户身份根本不在数据库里——应用拿服务主体连接，授权散落在应用代码各处的 WHERE 子句里。让一个手握服务主体全量权限的 Agent 替两千个门店经理中的任何一个提问，这条路走不通。（原文锚点：`the end user's credentials are not actually part of the operational database schema`；`using where clauses in SQL queries that are scattered in the application`）

Google 的答案是参数化安全视图（PSV）：建立在 Postgres 安全视图的 security barrier 之上——它阻止优化器把谓词下推进视图，封死用除零报错做信息推断的攻击面；再把原本写在应用里的授权检查挪进视图的 DDL 参数，Agent 侧只授予 PSV 权限。LLM 可以被诱导生成任何查询，但登录用户的凭证作为侧信道在运行时绑定视图参数，查询被动态限定在该用户可见的范围里。他引用 1975 年的端到端论点收束：非确定性世界里，安全必须落在数据这一端，而不是管道里。（原文锚点：`we've built something called parameterized secure views`；`it makes sure that you cannot engage in an information theoretical attack`；`You can attack the LLM. You can convince the LLM, spoof it`；`We take that logged in user's credential and have it as a side channel`；`the End-to-End Argument in System Design`）

隔离和可观测性是另外两块。他转述了一位银行客户的质问："我们花了几年确保批扫描跑不进运营库，你现在想让我在上面跑 Agent？"——但他认为当年隔离分析负载的功课同样适用于 Agent；至少要能回答"这条查询来自 Agent 还是应用"。至于 Google 内部 AI 写代码（Matt 引述其此前"约四分之三新代码由 AI 生成"的说法），他的口径很谨慎：Paxos 这类 Spanner 心脏协议大概率仍不适合让 Agent 大改，关键是每个团队为自己的场景建 harness、以 evals 持续度量，并在试点项目里"遇到瓶颈就修瓶颈，而不是绕过去"。收尾的建议是：两代工程师学的是确定性系统，这个时代要接受数据是乱的、结果是有相关性光谱的——"我们必须拥抱混沌"，而 evals 正是拥抱之后还能看清质量的方式。（原文锚点：`We just spent years making sure batch scans can't run against your operational databases`；`Give me a list of queries that came from an agent versus from the application`；`that's Paxos technology, that's the heart of Spanner`；`when you hit the bottleneck, fix the bottleneck, don't go around it`；`we have to embrace the chaos`）

## 来源与定位

- 原始节目：[Inside Google’s Database Infrastructure for the AI Era](https://softwareengineeringdaily.com/podcasts/inside-googles-database-infrastructure-for-the-ai-era/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 数据库教条、可用性-持久性耦合与 enterprise IT 的成熟（`Database dogma is really being focused on specify what you want`；`A long-duration performance event effectively becomes an availability event`；`Enterprise IT, I talk to customers all the time, just incredibly creative`）
  - 结构化与非结构化数据合流、从精确结果到相关性与排序（`it's no longer just enough to not lose your data and produce exact results`；`the confluence of structured and unstructured data`）
  - Spanner 起源：广告系统分片 MySQL 的仓鼠轮与企业功能、规模、全球三合一（`The ad system used to run on sharded MySQL`；`this is a hamster wheel that they had to get off`；`no one had figured out how to solve all these three together`）
  - 选型建议与多模型能力（`if what you're trying to do is something that will run in a single node, Postgres is just fine`；`you can have a graph database, you can have full-text search, you can have vector search`）
  - Spanner Omni 的监管动机、混合云生态与单二进制打包（`I know that I'm considering moving from a system which gives me two and a half nines`；`their crown jewels will remain in their data center`；`we collapsed it all into a single binary`）
  - Colossus 元数据复制、TrueTime 与外部环境的时间取舍（`We only have to copy metadata`；`to be able to talk about what we call the epsilon`；`the world outside is kind of like the world inside Google in 2012`）
  - Spanner Graph 的图视图与反洗钱案例、DANA Pay 实时拦截（`You have a DDL command that says create property graph`；`Sophisticated fraud, like money laundering or synthetic identity fraud, often involves networks of colluding accounts`；`DANA Pay. It's an Indonesian digital payment solution`；`if I can flag and block the transaction, I can prevent financial losses`）
  - ScaNN 与过滤向量检索、反对拆分独立向量系统（`we have this amazing technology called ScaNN`；`We call this filtered vector search`；`we can actually probe both of them at the same time`；`it's a really poor idea to go build a completely separate vector system`）
  - agentic data cloud 三要素与上下文比 schema 更重要（`we think there are three important pieces`；`just the schema itself is actually not even enough`；`If I have a table with a billing address and a shipping address`；`the values in the city column, are they in lowercase? Are they three-letter airport codes?`）
  - 临时工作流、写提案与 MCP 生态、动态生成 UI（`applications are ephemeral workflows. The application as such doesn't exist`；`You make a proposal for a change`；`we're able to generate UI on the fly by connecting to these MCP servers`）
  - 运营库授权断层、PSV 与端到端论点（`the end user's credentials are not actually part of the operational database schema`；`we've built something called parameterized secure views`；`We take that logged in user's credential and have it as a side channel`；`the End-to-End Argument in System Design`）
  - 隔离、可观测性、AI 写代码的 evals 与拥抱混沌（`We just spent years making sure batch scans can't run against your operational databases`；`that's Paxos technology, that's the heart of Spanner`；`we have to embrace the chaos`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- ScaNN 性能倍数、向量规模、AI 生成代码比例等数字均为节目中的厂商口径或受访者引述，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
