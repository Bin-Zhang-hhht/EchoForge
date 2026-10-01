---
item_id: recsperts-4aa6a8c25683
title: '从消费者记忆到 Semantic ID：DoorDash 快电商的生成式推荐实践'
date: '2026-10-01'
published_at: '2026-09-23'
transcribed_at: '2026-10-01'
model: 'GLM-5.3-Flash'
source_url: 'https://share.transistor.fm/s/08e89b67'
source_name: 'Recsperts'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/08e89b67/transcript.txt'
summary: 'DoorDash 新垂直业务（生鲜、便利、零售）搜索与个性化 ML 负责人 Raghav Saboo 聊快电商推荐：多方市场要为三方健康增长排序而非只看点击；LLM「消费者记忆」补上元数据噪声与意图长尾；Semantic ID 以残差 k-means 学出层级码本，在排序特征替换与查询改写中拿到线上提升，指向搜索、发现与 agent 的统一基底。'
tags: [推荐系统, LLM]
---

# 从消费者记忆到 Semantic ID：DoorDash 快电商的生成式推荐实践

> 节目：[Recsperts](/podcasts/recsperts/)
>
> 节目发布：2026-09-23 · 逐字稿获取：2026-10-01 · 笔记整理：2026-10-01
>
> 全文共 4789 字 · 阅读约 12 分钟
>
> 标签：[推荐系统](/tags/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F/) [LLM](/tags/LLM/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/08e89b67) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/08e89b67/transcript.txt)

## 速读

DoorDash 新垂直业务（生鲜、便利、零售）搜索与个性化 ML 负责人 Raghav Saboo 聊快电商推荐：多方市场要为三方健康增长排序而非只看点击；LLM「消费者记忆」补上元数据噪声与意图长尾；Semantic ID 以残差 k-means 学出层级码本，在排序特征替换与查询改写中拿到线上提升，指向搜索、发现与 agent 的统一基底。适合做电商/平台推荐、生成式检索与多目标排序的工程师。

官方逐字稿为 Whisper 自动生成：无时间戳、无说话人标注（偶有误插入的人名标签），文中说话人按对话语境归属嘉宾或主持人 Marcel；定位使用可搜索原文短语，无法核实的转写细节（如个别品牌名）未采用。

## 主题正文

### 多方市场：为三方的「健康增长」排序，而不是为点击

嘉宾所在的「新垂直」业务是 DoorDash 从餐厅外卖长出来的第二曲线：从生鲜起步、扩展到一般零售，连本地小商家也接入了平台（主持人补充集团背景：覆盖 40 多个国家、集团月活超 5600 万，2021 年并购 Wolt、2025 年并购 Deliveroo）。他强调，多方市场里任何产品或模型改动都要同时照顾三方：消费者要找得到小众且能履约的商品，商家要能呈现自己的品牌价值，骑手与履约网络是飞轮的第三方——「不只是拿到更多点击或互动，而是理解什么对这个市场的健康增长才是好的，让飞轮上的三方都受益」（`benefits all of the three stakeholders in this flywheel`）。搜索与发现的取舍也不同：搜索里「与查询的相关性至高无上」，错误结果会侵蚀用户对这个入口的信任；发现页则可以更大胆地探索、学习会话之外的消费者（`Relevance to the query is supreme for search`）。

### 从 embedding 到「消费者记忆」：LLM 补上的两个表示瓶颈

为什么传统表示不够用？他给出两个瓶颈（`the bottleneck of these representations come from two sources`）：一是目录规模与元数据质量——全部商家去重前约有几十亿商品、去重后仍有数亿，商家提供的元数据常常残缺，「非结构化的那部分，传统模型表示不了」；二是意图长尾与行为回环——消费者还没在平台上表现过的行为，模型永远学不到。LLM 内化的「世界知识」正好补位：把对消费者的理解随时间沉淀为自然语言的「记忆块」（`a concept of memory blocks`）——饮食偏好、是否养宠物、更信任哪些品牌等语义域，既有消费者记忆也有商家记忆（不能让「卖地毯的店看起来像生鲜店」）。这层原语既供内容生成复用，也供今年早些时候上线的 Ask DoorDash（生鲜与餐厅下单 agent）个性化其输出。业务框架是「熟悉、实惠、新鲜」三目标（`familiarity, affordability, and novelty`；他们在 KDD 2025 巴黎 workshop 报告过，主持人转述，DoorDash 工程博客有对应文章）：熟悉建立平台信任，实惠是在对的时机给对的优惠，新鲜即探索。落地的第一组件是意图驱动的内容池：LLM 基于消费者记忆生成个性化 collections（感恩节、宠物训练、每周生鲜采买等场景），并把 collection 表示成「消费者会去搜的搜索词」，再由搜索栈的向量召回与排序模型接住（`these search terms are resolved into items`）——个性化与搜索两套栈由此开始合流。他提到这套生态约有五个组成部分，逐字稿只展开到第一组件。

解释性正是从 collections 做起的原因之一：自然语言画像让产品、战略与运营伙伴能「从消费者视角」讨论购买模式，而不只是看数字。他呼应主持人转引的前嘉宾 Joe Konstan 的说法——「有时让东西有用的不是推荐本身，而是围绕它给出的信息」（`not the recommendation itself, but the information put around it`），并向消费者解释「为什么给我看这个」仍是无人做好的空白。风险同样真实：太具体显得「creepy」，太离谱立刻被识破，「两个极端都糟糕」（`Both extremes are bad`）。他总结 LLM 接入推荐栈至少有三种模式——放在栈前面做生成、放在最终阶段（第三种未展开）；DoorDash 当前选的是前者配传统检索与排序。

### Semantic ID：把目录学成一棵「机器自己的树」

动机部分来自 TIGER、PLUM 等生成式检索研究（源自 DeepMind、Google/YouTube）：统一栈需要一种「语言模型能当作 token 学习」的目录标识。而人工 taxonomy 的老大难有二：分类师团队要服务多个团队，粒度只能做粗；节点划分带任意性——酸面包的全部变体可以是终端节点，「非酸面包」却挤在一个大节点里。Semantic ID 的构建：用内容 embedding（LLM 依品名、品牌、规格等文本生成；商品图因各商家拍摄方式差异太大、噪声高而弃用）做递归 k-means——每层聚出码本、对残差继续聚类（`we use what is referred to as residual k-means`），ID 序列天然层级化，等于一棵「学出来的 taxonomy」。当前为三层、每层 512 个码字（512³ 码本）。它聚在人类不会那样切、却看得到意义的属性组合上，比如「破洞男式牛仔裤」「漂白 mom jeans」这类现有人工分类里不存在的簇；定性评估看各层条目共享的常见词，人工检查的结论是「初看不会那样分，细想能理解」。他强调电商比视频推荐更需要这种内容理解：商品「本身携带大量语义」，推荐歪了用户不会轻轻划走（`items really carry a lot of meaning`）。

### 两个落地证据：排序特征替换与查询改写

用例一在排序：他们的排序模型是深度多任务多标签模型，约 250 个特征（稠密特征约 180 个），覆盖四级人工 taxonomy 的聚合特征。做法是把 Semantic ID 的 n-gram token 作为聚合维度，在商品与「消费者×商品」粒度上聚合约 4/8/12 周购买等稠密特征。关键不是「加了更好」，而是「能做减法」：把 top 50 稠密特征中的 20 个换成 Semantic ID 特征、移除约 17–20 个 taxonomy 特征后，线上指标仍有可观提升（`replace 20 of the top 50 dense features`）——以内容为主的 Semantic ID 对个性化任务同样有效。用例二在搜索：把查询也表示成 Semantic ID，驱动查询改写推荐（`using semantic IDs for query reformulation`），对应两条路径——沿层级向下逼近具体商品（berries → 有机草莓），或横向找替代与互补（做水果沙拉还缺什么）；相比过去对历史字符串查询做图遍历，「纯字符串查询很难学」。首个小规模实验里查询改写的点击率上升，这让团队有信心把 Semantic ID 当作搜索、发现与 agent 三个表面共享的目录理解。相关工作成文于 RecSys 2026 USRW workshop 论文《One Hierarchy, Two Systems: Semantic Product IDs for Discovery-Surface Ranking and Search-Page Query Reformulation》（10 月 2 日现场报告）。

### 统一是基底，不是「一个模型统治一切」

面对「要不要一个端到端大模型」的追问，他给出的答案是分层：Semantic ID 与 LLM 可读的消费者记忆是两个共享积木（`we have a common substrate`），其上是可复用的 foundation model/骨干（学习跨表面表征，不必直接驱动某个表面），最外层才是各表面的任务模型。搜索、发现与 agentic 下单三个表面将长期共存，agent 不会取代搜索——对话输入成本高，消费者适应也需要时间。他对 agentic 的定位值得记住：它不是一种新系统，「而是用户体验问题」（`but rather a user experience question`）；ChatGPT、Claude 的普及让聊天范式成为新常态，但现状是「我们展示搜索结果与推荐的用户体验许久没有进化——所有 app 长得都一样」（`All apps look the same`），「界面还不够可塑，谈不上真正统一」（`our user experiences are not malleable enough`）。他的理想形态是 app 像「活的」：依据输入（语音、对话、滑动方式）自行演化成搜索流、聊天流或发现流。当下搜索与推荐合流的具体例子是购物车补全（沙拉 → 马苏里拉 → 樱桃番茄）；agent 按显式意图生成整个购物车，则提供了跨栈学习回环、避免三套栈各自进化掉队的可能。收尾的职业建议同样坦率：这个领域的变化节奏已从半年一变加速到每季度一变，好奇心是燃料也带来倦怠风险；要善用 LLM 当快速学习工具，更要训练「判断什么不值得投入」的品味（`what you should not waste your time on`）。他与主持人及 Wolt 同事将在 9 月 28 日以「外卖平台推荐系统」教程为 RecSys 2026（明尼阿波利斯，会议 2007 年诞生地）开场。

## 来源与定位

- 原始节目：[#34: From Consumer Memory to Semantic IDs: Generative RecSys for Quick Commerce with Raghav Saboo](https://share.transistor.fm/s/08e89b67)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 多方市场的三方健康增长约束（`benefits all of the three stakeholders in this flywheel`）
  - 搜索以查询相关性为先（`Relevance to the query is supreme for search`）
  - 两个表示瓶颈与目录规模（`the bottleneck of these representations come from two sources`）
  - 消费者记忆原语 memory blocks（`a concept of memory blocks`）
  - 熟悉、实惠、新鲜三目标（`familiarity, affordability, and novelty`）
  - collections 表示为搜索词并接入搜索与排序栈（`these search terms are resolved into items`）
  - 解释性与「信息环绕」（`not the recommendation itself, but the information put around it`）
  - Semantic ID 的残差 k-means 构建与层级码本（`we use what is referred to as residual k-means`）
  - 排序模型用 Semantic ID 特征替换 taxonomy 特征（`replace 20 of the top 50 dense features`）
  - 查询改写用例与首次小规模验证（`using semantic IDs for query reformulation`）
  - 统一栈的共同基底（`we have a common substrate`）
  - agentic 的定位是用户体验问题（`but rather a user experience question`）
  - 从业建议与「不浪费时间」的判断力（`what you should not waste your time on`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3-Flash
- AI 编辑整理，请以原始节目为准。
