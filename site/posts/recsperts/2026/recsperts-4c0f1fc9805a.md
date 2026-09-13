---
item_id: recsperts-4c0f1fc9805a
title: '外卖推荐为什么难：Wolt 如何把「失败」的 NCF 调成生产级模型'
date: '2026-09-13'
published_at: '2026-05-12'
transcribed_at: '2026-09-12'
model: 'GLM-5.3-Flash'
source_url: 'https://share.transistor.fm/s/0c0643e0'
source_name: 'Recsperts'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/0c0643e0/transcript.txt
summary: 'Wolt 首席应用科学家复盘外卖推荐的坑：距离让协同过滤失灵、单页转化提升被「同类相食」抵消、登录数据偏向已排好的序；他们用 BPR 损失、上下文负采样救活 NCF，最终用一个 Transformer 取代四个模型。'
tags: [推荐系统, AI 架构]
---

# 外卖推荐为什么难：Wolt 如何把「失败」的 NCF 调成生产级模型

> 节目：[Recsperts](/podcasts/recsperts/)
>
> 节目发布：2026-05-12 · 逐字稿获取：2026-09-12 · 笔记整理：2026-09-13
>
> 全文共 4010 字 · 阅读约 11 分钟
>
> 标签：[推荐系统](/tags/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/0c0643e0) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/0c0643e0/transcript.txt)

## 速读

这期是推荐系统播客 Recsperts 的从业者特辑：主持人 Marcel 与嘉宾 Sasha Fedintsev（Wolt/DoorDash staff applied scientist）本就是同事，因此聊得格外具体。外卖推荐与普通电商的根本差异是「位置」——距离约束让经典协同过滤失灵、单页指标的提升会被「同类相食」抵消、只有成交会话的日志又偏向「本来就排得很好」。节目最有价值的是一条完整的工程叙事：从 cannibalization 的发现，到用 BPR 损失、上下文负采样和置信权重把学界「复现失败」的 NCF 做成生产级模型，再到用一个 Transformer（UVR）取代四个模型。适合推荐系统工程师与搭建评估体系的团队。

需要注意：官方逐字稿为 Whisper 自动生成、无时间戳，本文定位全部使用可搜索原文短语；具体业务数字（如 uplift 幅度）为嘉宾口述。

## 主题正文

### 位置约束：外卖推荐与电商的根本分野

Fedintsev 2019 年加入 Wolt 时是公司第二位数据科学家、第一位做推荐的——他特意从「已经做到 SOTA」的 Zalando 跳出来，想从零搭建，却发现「我知道怎么做」的假设完全失效：外卖和时尚电商是两门生意。核心差异是位置依赖：在 Zalando,算法推荐什么都买得到；在 Wolt,推荐再相关但超出配送范围的店，用户买不了；稍逊相关但配送费更高的店，用户会选便宜的或者干脆离开（原文锚点：`if you recommend something really relevant, which is outside of the delivery area`）。位置约束还直接打击协同过滤：用户-商家交互矩阵高度地理聚集，跨集群只靠少量「会跨区下单」的顾客提供弱连接，经典算法效果大打折扣；他把同品牌门店聚合成单一实体，才让连接变强（`this matrix becomes highly clustered`）。

位置也有红利：距离过滤天然就是候选生成——「第零级排序器是系统给的」，即便是最大的城市，过滤后候选也只有几千个，不用像 YouTube 那样建庞大漏斗。这是一把双刃剑（`the kind of first or zero stage ranker is already kind of given`）。

### 「同类相食」：单页指标好看，整体转化不动

节目中最有普适价值的是 cannibalization 案例。Wolt 的界面分为发现页（类 Netflix 的网格轮播）、餐厅 Tab（竖排列表）、商店页和搜索。团队先在餐厅 Tab 上线协同过滤模型，Tab 内转化率上升，整体转化却纹丝不动——用户只是从搜索和发现页转移到了餐厅 Tab,并没有买得更多（原文锚点：`that is called cannibalization of the traffic`）。多页结构是「因祸得福」：它让体验很难被搞砸（发现页不行还有搜索兜底），但也让整体转化极难拉动。

更深的坑在评估数据：如果只记录餐厅 Tab 里成交会话的曝光位置，这份数据会严重偏向「本来就排得好」的会话——再强的模型也很难打赢这个基线（`biased towards very good ranking`）。Fedintsev 的解法简单而巧妙：把「看了餐厅 Tab 却去别处成交」的会话也纳入，把实际成交映射回当初列表位置，构造反事实标签；同事 Marcus 则给出了贝叶斯重加权的方案。他还向学界喊话：那些没有成交的会话目前完全被浪费，希望研究者想想怎么利用（`sessions where users just didn't buy anything`）。

### 把「复现失败」的 NCF 做成生产级模型

节目用相当篇幅铺垫了 NCF 的学术公案：2017 年原始论文提出神经协同过滤；2019 年 RecSys 最佳论文《Are We Really Making Much Progress?》在 18 个算法中只复现出 7 个，且用调好的基线就能打败其中 6 个——NCF 赫然在列；2022 年的后续研究结论是「用 MLP 学点积可行但低效」。而当主持人在入职面试时听说 Wolt 生产环境在用 NCF,第一反应是「你们读过那些论文吗」。

Fedintsev 的答案很诚实：成功 partly 因为「我开工前没找到那些论文」。关键转折是 cannibalization 分析带来的洞察——真实业务里大部分成交来自复购，模型只是把用户买过的店排得更靠前，这用启发式就能做到；要拉动转化，必须专门优化「从新店成交」的会话子集，同时不破坏复购会话的表现（`improve metrics on this subset with a constraint`）。当时Spark ALS 在这个子集上表现很差，而公司几乎没有机器学习基础设施（没有特征仓库），NCF 的自包含性恰好合适：用户与商家嵌入放进 Redis 即可服务，无需额外网络往返。当然，第一次上线的结果「令人失望」——离线指标连 ALS 都没打过，他还一度自责复现能力差（`it was a disappointment`）。

翻盘来自一连串方法论改进：把 BCE 损失换成 BPR 排序损失，指标立涨（他在线下分享中给出约 20% 的相对 MRR 提升）；负采样从全库均匀采样改为「上下文感知」——只从同一城市、同一区域的商家中采，直接利用了位置约束（`there is no point in sampling negatives from a different city`）;按用户维护过滤后的负例集，防止把另一个正例采成负例；引入 Hu、Koren、Volinsky 隐式 ALS 论文的置信权重（购买、收藏、点击的线性组合再取对数——取对数效果更好，可能因为降低了流行度偏差）；从低权重正例中采负例，让正例之间也建立排序；再加 Dropout 抗过拟合，让训练跑得更久、更有机会采到难负例。所有改进先离线验证，攒出大幅提升（口述量级约 50%）才上 A/B——此前的初步 A/B 教训是「小提升不值得烧流量」。最终长周期确认实验（90/10 留出）验证了假设：新店成交会话的 MRR 提升转化为业务指标，商业收益显著（`it actually confirmed my hypothesis`）。

### 从 NCF 到 SPR 再到 UVR：一个 Transformer 取代四个模型

NCF 的一个工程亮点是速度：内存中排名数千商家，p99 延迟 30 毫秒以内（嘉宾口述），这让二层排序成为可能——SPR（second pass ranker）对头部几百家重排，显式引入距离、配送预估、菜单规模等内容特征；对比试验里梯度提升与神经网络精度相当，神经网络因缓存友好而略快。但 SPR 学的是「平均人群的距离重要性」，真正的个性化有限。由此引出序列建模：把用户旅程表示成动作序列，用 Transformer 预测下一次购买，并把 Uber H3 六边形位置、时间、星期等上下文编码为嵌入（`we use Uber H3 library`）。2025 年初与主持人合作的结论是：这一个模型不仅追平了 NCF+SPR 等四个模型的组合，还实现了超越——即 UVR（Universal Venue Ranker）,随后的 A/B 带来可观提升，并且更擅长推荐新店（`bringing transformers into production`）。

在新旧之间，Fedintsev 立场鲜明：模型应当强烈优化「推荐新东西」，复购需求交给启发式和专门的「再来一单」UI——因为在混合数据上训练天然偏向旧店；UVR 已对复购会话降权并看到业务指标改善，他甚至愿意押注「完全不管复购会话的性能」会更好。他也承认这是待验证的直觉，主持人补充了折中方案：实时识别用户处于探索还是「懒惰复购」模式，再用多项式混合一类方法做融合（`downweights a little bit recurrent`）。广告技术则是同一问题的镜像：排序要的是相关性分数，竞价需要「校准良好的概率×出价」——第一代广告模型就是 NCF 加校准层，新一代同样转向 Transformer,且对延迟更苛刻。他留给社区的最大难题是商品级推荐：如何在 iPhone、香蕉和卫生纸之间读懂用户当下意图——朴素模式学习永远只会推荐卫生纸这类高频复购品（`whether to recommend an iPhone or a banana`）。

节目尾声转向嘉宾的另一重身份——长寿研究（他在《American Journal of Physiology》等期刊有发表）。他给出的数学论证相当警醒：即使心血管疾病和癌症在 110 岁前被 100% 治愈，仍有约 99.8% 的人会患上失智症（`even if we cure all diseases`）——这是他持续发声推动抗衰老研究的理由。

## 来源与定位

- 原始节目：[#32: RecSys in the Delivery Industry at Wolt with Sasha Fedintsev](https://share.transistor.fm/s/0c0643e0)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 位置依赖与协同过滤的失灵（`this matrix becomes highly clustered`）
  - 多页结构与同类相食（`that is called cannibalization of the traffic`）
  - 成交日志偏差与反事实修正（`biased towards very good ranking`）
  - NCF 的翻盘：损失、负采样与置信权重（`there is no point in sampling negatives from a different city`）
  - UVR 单模型取代四个模型（`bringing transformers into production`）
  - 新店探索优先与长寿研究收尾（`even if we cure all diseases`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3-Flash
- AI 编辑整理，请以原始节目为准。
