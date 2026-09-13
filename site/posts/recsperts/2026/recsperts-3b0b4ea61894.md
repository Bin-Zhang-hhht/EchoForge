---
item_id: recsperts-3b0b4ea61894
title: '为惊喜设计，而不是制造惊喜：推荐系统里的 Serendipity 完整框架'
date: '2026-09-13'
published_at: '2026-01-28'
transcribed_at: '2026-09-12'
model: 'GLM-5.3-Flash'
source_url: 'https://recsperts.com/31-serendipity'
source_name: 'Recsperts'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/01289c0f/transcript.txt
summary: '布鲁塞尔自由大学 Annelien Smets 拆解 serendipity：它无法被工程化，只能「为其设计」；四种意图（理想/公益/中介/功能）、体验三要素（意外、焕新、增益，缺一不可）与可供性仓库；Netflix「给我惊喜」败在期待落空。'
tags: [推荐系统, 产品指标]
---

# 为惊喜设计，而不是制造惊喜：推荐系统里的 Serendipity 完整框架

> 节目：[Recsperts](/podcasts/recsperts/)
>
> 节目发布：2026-01-28 · 逐字稿获取：2026-09-12 · 笔记整理：2026-09-13
>
> 全文共 3165 字 · 阅读约 8 分钟
>
> 标签：[推荐系统](/tags/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F/) [产品指标](/tags/%E4%BA%A7%E5%93%81%E6%8C%87%E6%A0%87/)
>
> 🎧 [收听原节目](https://recsperts.com/31-serendipity) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/01289c0f/transcript.txt)

## 速读

「惊喜度（serendipity）」是推荐系统论文里最常被敷衍处理的指标之一——通常被算成「相关性 + 意外性」的加总。嘉宾 Annelien Smets（布鲁塞尔自由大学教授、Serendipity 学术研究网络联合创始人）把这团浆糊拆成了完整的框架：你不能工程化惊喜，只能「为其设计」；先想清楚四种意图（理想、公益、中介、功能），再理解体验的三个必要成分（意外、焕新、增益——是「与」不是「或」），最后用「可供性仓库」落到界面、内容与信息获取的具体设计上。Netflix「给我惊喜」按钮的失败案例是她最好的反面教材。适合做推荐策略、评估与产品设计的人。

官方逐字稿为 Whisper 自动生成、无时间戳，本文定位使用可搜索原文短语；结论以嘉宾及其团队发表的论文口径为准。

## 主题正文

### 悖论：算法在「计划」，惊喜在「意外」

Smets 的博士问题原本是「如何使用推荐系统而不制造过滤气泡」,导师抛给她一个当时没听过的词——serendipity,她笑称「认识这个词本身就是一次奇遇」。悖论在于语义：算法的任务是计划、预测、控制，而 serendipity 的本义是偶然与意外，两者天然相克。因此她的立场很明确：你无法计划或工程化 serendipity,唯一能做的是「设计环境让它更可能发生」（`you cannot plan serendipity, you cannot engineer serendipity`）。她给的两个类比：现实里独自去咖啡馆会增加奇遇的概率；城市设计里把楼梯铺成钢琴键让人更愿意走楼梯—— nudging 而非强制。

### 先问「为什么」：惊喜的四种意图

被低估的原因，是她认为学界很少问「serendipity 对体验者之外的其他利益相关方有什么价值」。Google 的研究提供了一个答案：把惊喜纳入设计能提升长期满意度与留存（她按「中介」类型归类）。她把设计意图分成四种：一是「理想」——像图书馆，只在乎用户与有价值内容的相遇；二是「公益」——聚合效应，多元观点滋养民主讨论；三是「中介」——把它当实现别的目标的手段（如让长尾商品获得曝光）；四是「功能」——惊喜本身就是产品价值主张，比如 coworking 社区 Seeds to Meet 卖的就是「与陌生人的奇遇」，或主持人节目中提到的 Slack 随机咖啡机器人。她特意强调：商业目标与 serendipity 并非天然对立，关键是平衡并守住惊喜的本质（`I don't think that commercial objectives are per definition against serendipity`）。

### 体验的三要素：是「与」，不是「或」

团队 2025 年在 UMAP 发表的访谈研究（17 位跨平台用户、历时半年）给出了体验侧的定义：serendipity 是「用户无意间遇到让自己觉得『侥幸、焕新且有益』的内容」的体验——三个成分缺一不可。意外但无益，不算；焕新也有多种口味：可以是全新内容，可以是对你「不寻常」的内容，甚至可以是「重拾遗忘的旧好」——节目里主持人恰好分享了自己的业余项目：用 GDPR 要回的 Spotify 数据构建近期口味画像，从两千首红心歌单里捞回最匹配的几十首，戏称「Rediscover Weekly」,正好对应论文里的「品味重生（taste reincarnation）」子类（`taste reincarnation`）。研究还区分了「拓宽品味」与「深化品味」两类风味：前者如 Zalando 用户被推荐了不合常规风格的鞋、买回后真香并扩展了整个穿衣风格；后者如用 Spotify 的歌曲电台深挖已喜爱的曲风。一个推荐甚至可能引发雪球——有受访者因一首 Taylor Swift 的歌一路听到演唱会，还有人因一部纪录片改成素食。测量上的陷阱也随之而来：把「相关性 + 意外性」加总会互相抵消，而三个成分必须同时在场（`the three components should really be there`）。

### 可供性仓库与「过犹不及」

设计侧的概念是「可供性（affordance）」——环境向你提供了什么可能性（门把手告诉你该推还是拉；把手高度也取决于使用者的能力）。团队 2022 年的研讨会上把图书馆研究的三大设计原则——环境可多样化、可穿越、可感知——落到推荐系统的三个层面：内容、用户界面与信息获取，建成了「特性仓库」。例如「可慢化（slowability）」：城市里放长椅会让人停下张望、开启攀谈；对应到产品里，「你的长椅在哪里」？操作建议是跨职能工作坊：拿仓库里的例子问设计师、数据工程师和科学家，产出十到二十个候选措施，再做投入产出排序。反例同样有力：直接跳到方案、不回答「为什么」，要么做了与你场景无关的体验（图书推荐的方案未必适用外卖），要么过犹不及——图书馆里乱放的书会带来奇遇，但对正按索书号找书的人是纯粹的挫败（`too much serendipity can also be very frustrating`）。

### Netflix 的教训与「惊喜不破过滤气泡」

最好的反面案例是 Netflix:2021 年上线的「Play Something」按钮（后更名「Surprise Me」）在 2023 年初因使用率过低悄然下线。后续研究发现，看到「给我惊喜」标签的用户是真的期待被惊到，而实际播放的内容约有一半他们记得曾被推荐过——「当人们期待惊喜却没有得到时，体验远差于压根不期待」。这是教科书级的「过度承诺、交付不足」，说明惊喜设计必须连期待管理一起做。指标上她反对「万能惊喜度指标」,方向是为每种风味找合适的代理指标（比如深化型看与用户画像的相关度），且因内容类型而异——音乐试错成本只有三分钟，电影要九十分钟。平台经济学也值得研究：她合作的剧院把订阅制改成「一年任意看十场」后，观众自然看了更多元的剧目——商业模式本身就能邀请探索（`is your business model actually allowing for serendipity?`）。

收尾她想纠正一个流行迷思：研究了多年惊喜之后，她最想消灭的说法是「惊喜度能打破过滤气泡」——人们完全可以在气泡内部获得惊喜（品味深化的例子就是）。如果你的「为什么」是对付过滤气泡，那多样性才是必须贯穿整个设计旅程的核心目标，而不是加一点惊喜就完事（`serendipity bursts filter bubbles` 这一说法应被淘汰）。

## 来源与定位

- 原始节目：[#30: Serendipity for Recommender Systems with Annelien Smets](https://recsperts.com/31-serendipity)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 悖论与「设计而非工程」（`you cannot plan serendipity, you cannot engineer serendipity`）
  - 四种意图与商业目标的共存（`commercial objectives are per definition against serendipity`）
  - 体验三要素与风味（`the three components should really be there`、`taste reincarnation`）
  - 可供性仓库与过犹不及（`too much serendipity can also be very frustrating`）
  - Netflix 教训、过滤气泡迷思与商业模式（`is your business model actually allowing for serendipity?`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3-Flash
- AI 编辑整理，请以原始节目为准。
