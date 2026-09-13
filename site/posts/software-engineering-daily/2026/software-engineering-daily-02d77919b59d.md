---
item_id: software-engineering-daily-02d77919b59d
title: '苹果的 AI 焦虑与 token 账单时代：SED News 六月刊'
date: '2026-09-14'
published_at: '2026-06-09'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-apples-ai-problem-the-real-business-model-of-ai-and-token-cost-reckoning/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-apples-ai-problem-the-real-business-model-of-ai-and-token-cost-reckoning/'
summary: 'Gregor Vand 与 Sean Falconer 的月度新闻：Siri 假演示招来 2.5 亿美元集体诉讼、DuckDuckGo 因 Google 强推 AI 模式涨了 28% 访问、Remote 零增员做到 3 亿美元 ARR，以及 Simon Willison 那个判断——模型公司的真正商业模式是企业席位。'
tags: [企业 AI, 开发者工具, LLM]
---

# 苹果的 AI 焦虑与 token 账单时代：SED News 六月刊

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-06-09 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 4574 字 · 阅读约 12 分钟
>
> 标签：[企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [LLM](/tags/LLM/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/sed-news-apples-ai-problem-the-real-business-model-of-ai-and-token-cost-reckoning/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/podcasts/sed-news-apples-ai-problem-the-real-business-model-of-ai-and-token-cost-reckoning/)

## 速读

SED News 每月一期的新闻深聊，本期主题非常"钱"：苹果为什么在 AI 时代反而最安全又最危险；Google 把 AI 模式设为默认后用户用脚投票；以及从 Simon Willison 的博客引出的本期主话题——编码 Agent 的商业模式：二十美元的订阅在财务上必然亏损，真正的生意是企业席位和企业 token 账单。

最值得带走的三点：苹果的护城河（App Store 抽成）恰恰是 AI 最先冲击的对象；"收入/员工"正在取代"员工数"成为新的炫耀指标；以及 token 成本优化即将重演 Snowflake 账单时代的历史。

## 主题正文

### 苹果：最赚钱的"非 AI 公司"走到了十字路口

开篇是 Financial Times 对苹果的深挖。新披露的细节相当难堪：两年前 WWDC 上那段惊艳的 Siri 演示基本是假的，产品并没有做出来，管理层随后告诉工程师"你们有 9 周把它做出来"，结果失败，还招来 2.5 亿美元的虚假广告集体诉讼——这正是 AI 负责人离任的背景（`00:02:30–00:03:45`）。Sean 的对比是：Salesforce 玩了几十年 vaporware 演示都没事，因为它卖的不是消费者，吃不到集体诉讼；而苹果在 AI 上"从来没做出过真正有影响力的东西"，语音助手时代（他在 Google Assistant 做过）最后都沦为开关灯和查天气。奇怪的是资本市场并不惩罚它：别人破纪录的财报因 AI 焦虑跌，苹果股票却在历史新高（`00:03:45–00:06:25`）。

Gregor 补充的数字把结构性风险讲透了：苹果在法律文件里自己承认过，一个真正能干的 AI 助手可能让手动下载 App 变得多余——而 App Store 抽成正是服务收入的大头，服务收入几乎是 Mac 销售的三倍；iPhone 仍占 2025 年收入的近 70%；研发占比在 iPhone 繁荣期从 8% 滑到 2%（`00:06:25–00:08:09`）。FT 文章里那个滑门时刻很扎心：2010 年 Jobs 收购 Siri 时被问"你要进入搜索行业吗"，他答"不，我进入的是 AI 行业"。如果 Jobs 还在，苹果会不会是另一家公司？如今的接班人玩的是供应链与回购的极致游戏——每天十亿销售额、万亿返还股东、服务 75% 毛利，"但那不是创新，那是印钞机"（`00:06:25–00:08:09`）。AI 对苹果的威胁还有具体形态：Gregor 的伴侣不想为倒时差应用 Time Shifter 付费，直接用免费的 Claude 生成时差调整方案——"app-pocalypse"不需要杀死所有应用，只需要让足够多的小应用变得没必要，App Store 的抽成模式就会慢慢漏水（`00:08:09–00:10:21`）。

### 搜索的 AI 化与用户反弹

Google I/O 的亮点是"后台常驻 Agent"（Gemini Spark）：不是你问它答，而是它持续监控、主动干活。Sean 说这是他呼吁一年多的方向——Agent 不该被锁在聊天框里，希望 Google 的入场能教育市场（`00:11:13–00:12:30`）。但另一条新闻显示了用户的真实态度：Google 把 AI 模式设为默认后，DuckDuckGo 的访问量涨了 28%。Sean 拿 News Feed 早期反弹作类比，怀疑这只是阵痛；Gregor 的体验则是搜索结果已经变成"AI 回答 → 广告 → 自然结果"的三道障碍赛——他搜一家公司，AI 模式给了一段维基百科式的概括，而他想要的只是 Reddit 讨论列表、新闻列表和官网链接。"Google 被夹住了：要对抗 ChatGPT 和 Perplexity，就得牺牲搜索本来的核心价值；要保护未来收入，就得牺牲当下体验"（`00:12:30–00:16:26`）。

### 零增员的 3 亿美元：人效成为新北极星

Remote（阿姆斯特丹的远程薪酬平台）ARR 突破 3 亿美元、现金流转正，而且宣称实现这一切时 headcount 保持持平。两人从两个角度展开。一是"收入/员工"成为新的流行指标：Gregor 做了十年服务外包，那本来就是看人效的行业——"你卖的就是人的时间"；低利率时代炫耀的是扩张了多少 headcount，如今反过来了，炫耀的是不招人。二是效率到底去了哪：Parkinson 定律全额生效——省下来的时间立刻被更高的产出预期填满；而且每个人的输出都是别人的输入，"你用 AI 把三句话扩成一份文档，读者再用 AI 把它压缩回三句话"，人机接力的循环正在消耗省下来的时间（`00:16:26–00:23:00`）。Sean 还观察到 AI 工具的成瘾性：像老虎机一样投 token、出结果、想再来一把，"不用我的算力就是在浪费"，加上裁员压力和同行竞争，工作时长不降反升——"一场由冲刺组成的马拉松"（`00:17:59–00:20:17`）。

### 主话题：模型公司的真实商业模式是企业席位

本期主话题基于 Simon Willison 的博客：Anthropic 和 OpenAI 已经找到产品市场契合——不是因为消费者订阅划算，而是因为企业在大把掏钱。Willison 自己买了 Anthropic 和 OpenAI 各 100 美元/月的顶配订阅，30 天跑完 token 统计：消耗了约 2000 美元额度的用量——消费者侧在财务上完全不对等，企业侧付得远比这多，那才是商业模式（`00:23:00–00:25:02`）。Sean 的补充很有信息量：这像开源的打法——让个人便宜地用、形成全行业的网络效应，员工们"没了这工具没法干活"，再自下而上推动公司买单，叠加公司自上而下的 AI 焦虑，双向火箭燃料。更大的判断是竞争轴心的迁移：大约从 2025 年 11 月起，模型对工具场景而言已经"好得够用"，竞争从"最好的模型"变成"最好的 agentic harness 和上下文管理"——护城河在模型周围的信息环境，不在模型本身（`00:25:02–00:28:53`）。商业模式类比也随之改写：ChatGPT 约 9 亿用户、个位数百分比付费，那是门好生意但撑不起万亿估值；Anthropic 提前想明白的 B2B 路线意味着"它们不是新 Google，而是新 Salesforce"——卖席位、做企业销售，完全不同的肌肉（`00:26:00–00:28:53`）。

企业侧的疯狂也有实证：Uber CTO 说 2026 全年 AI 预算几个月就烧完了。Gregor 读出的潜台词是炫耀而非事故——"2025 年定的预算没料到这些工具会变得不可或缺"，正如 Willison 说的，这不是 AI 失败的故事，是预算失算的故事（`00:28:53–00:31:39`）。接下来的推演是 Sean 的强项：企业很快要给每个岗位算"完全负担成本"——保险、福利，再加一条 token 用量，"资深工程师 vs 产品市场岗的人均 token 账单"会成为报表科目；现在没人敢当"不用 AI 的恐龙"，但当员工人均月账单到两万美元时，总得有人付钱。历史剧本他信手拈来：网约车的 VC 补贴期结束于涨价，Snowflake 狂飙期没人看账单，市场转向利润后催生了整个成本优化生态，最后 Snowflake 把优化工具内置进产品。动态路由（按任务把提示词派给更便宜的模型）创业潮已经出现（`00:31:39–00:34:34`）。Gregor 的收尾很实在：Remote 没披露 AI 开销——假设百人公司每月花 1 万美元买工具，等于放弃两三个 headcount 换其他 100 人生产力，划算；但真正的拐点是"什么时候大家开始盯着这笔账"。Supabase 内部养着两三个全职优化 AWS 账单的工程师，本身就是症状（`00:34:34–00:36:10`）。

开放权重模型的机会随之而来：Cursor 的 auto mode 跑的正是 Fireworks 托管的调优开源模型。Gregor 的猜想是会有企业算明白"同样输出、自托管开源模型一年便宜 20 倍"；Sean 补充这个市场 TAM 巨大，会跑出开源推理的赢家。节目的预测环节：Sean 押 token 成本优化工具六个月内爆发；Gregor 押 Anthropic 的 S1 文件会让市场"惊喜地看到它们多能赚钱"，成为"下一个微软"级别的话题（`00:36:10–00:48:23`）。

### Hacker News 精选

轻松收尾：有人在 GL.iNet Slate 7 Pro 旅行路由器（2.8 英寸触摸屏的 Linux 网络设备）上跑了 Doom，评论区照例争论人类是否该换个不那么暴力的传统移植对象；于是有了 Doombench——"你的技术栈能不能跑 Doom"性能测试。Sean 推荐了《Can We Have the Day Off》：如果 AI 真带来 10 倍生产力，周五能休吗——作者顺带提了加州每月 6000 美元的托儿费，时代情绪拉满。YouTube 开始自动检测并标注照片级 AI 生成视频（不再靠创作者自觉）；Gregor 说他观鸟时被 AI 生成假鸟烦透了，只想要个可过滤的标签。最后是 SimCity 3000 的 4K 复刻，以及一个温柔的悖论：Metal Gear Solid PS4 版提供原画质和增强画质两档，他反而更爱原版（`00:40:15–00:46:29`）。

## 来源与定位

- 原始节目：[SED News: Apple's AI Problem, The Real Business Model of AI, and Token Cost Reckoning](https://softwareengineeringdaily.com/podcasts/sed-news-apples-ai-problem-the-real-business-model-of-ai-and-token-cost-reckoning/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Siri 假演示、9 周交付与 2.5 亿美元集体诉讼（00:02:30–00:03:45）
  - 苹果的 AI 缺位、资本市场的宽容与文化错位（00:03:45–00:06:25）
  - App Store 抽成风险、R&D 占比下滑与"印钞机非创新"（00:06:25–00:08:09）
  - Time Shifter 案例：AI 替代小应用的 app-pocalypse（00:08:09–00:10:21）
  - Google 后台常驻 Agent 与 DuckDuckGo 28% 流入（00:11:13–00:14:53）
  - 搜索的三道障碍赛与 Google 的两难（00:14:53–00:16:26）
  - Remote 零增员 3 亿美元与人效北极星（00:16:26–00:18:26）
  - AI 工具的成瘾性与"冲刺马拉松"（00:17:59–00:20:17）
  - Parkinson 定律与 AI 文档的膨胀循环（00:20:17–00:23:00）
  - Simon Willison 的 PMF 论：订阅亏损、企业付费（00:23:00–00:25:02）
  - 竞争轴心迁移：从模型到 harness 与信息环境（00:25:02–00:28:53）
  - 新 Salesforce：席位制 B2B 路线（00:26:00–00:28:53）
  - Uber 预算烧穿的解读与人均 token 账单（00:28:53–00:34:34）
  - Snowflake 历史重演、成本优化创业潮与开源权重机会（00:31:39–00:40:15）
  - HN 精选：Doom 移植、"周五能休吗"与 YouTube AI 标注（00:40:15–00:46:29）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字（诉讼金额、收入占比、订阅用量等）仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
