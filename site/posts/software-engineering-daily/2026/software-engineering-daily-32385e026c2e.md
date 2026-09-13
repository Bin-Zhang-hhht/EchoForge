---
item_id: software-engineering-daily-32385e026c2e
title: '苹果×Gemini、OpenAI 取消归属悬崖与 2026 就业市场：SED News 双周报'
date: '2026-09-14'
published_at: '2026-02-03'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-apple-bets-on-gemini-googles-ai-advantage-and-the-talent-arms-race/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-apple-bets-on-gemini-googles-ai-advantage-and-the-talent-arms-race/'
summary: 'Gregor Vand 与 Sean Falconer 的科技头条双周报：Gemini 版 Siri 据报二月落地、OpenAI 取消股权归属悬崖（股票薪酬约占预计营收一半）、OpenAI 对 Google 的"红色警报"背后的 TPU/GPU 架构之争，以及 2026 年开发者就业市场的冷读。'
tags: [LLM, 企业 AI, 组织转型]
---

# 苹果×Gemini、OpenAI 取消归属悬崖与 2026 就业市场：SED News 双周报

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-02-03 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 3936 字 · 阅读约 10 分钟
>
> 标签：[LLM](/tags/LLM/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [组织转型](/tags/%E7%BB%84%E7%BB%87%E8%BD%AC%E5%9E%8B/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/sed-news-apple-bets-on-gemini-googles-ai-advantage-and-the-talent-arms-race/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/podcasts/sed-news-apple-bets-on-gemini-googles-ai-advantage-and-the-talent-arms-race/)

## 速读

SED News 回归（停更约八周），Gregor Vand 与 Sean Falconer 扫了一遍假期前后的头条：特斯拉停用 Autopilot 辅助驾驶转注全自动驾驶、苹果据报将在二月推出 Gemini 驱动的 Siri、OpenAI 取消股权归属悬崖、Manus 以 20 亿美元卖身 Meta；本期中段话题是 2026 年开发者就业市场的冷静解读。花边也不少：两位主播自报了家门——Sean 的东家 Confluent 正被 IBM 收购，Gregor 已加入 Supabase。

最值得带走的三点：Google 对 OpenAI 的结构性优势是"数据 × 分发 × 自研芯片"三件套，NVIDIA 75% 的毛利率正是 TPU 要绕开的成本；OpenAI 取消一年归属悬崖是人才争夺的新打法，但代价是其股票薪酬预计达 60 亿美元、约占预计营收一半；对"AI 取代程序员"的恐慌，两位主播的读法是：就业总量在增长、岗位性质在变，资深工程师借助编码 Agent 变得更强，真正的隐忧是初级工程师的成长路径。

## 主题正文

### 头条扫读：从星链 Wi-Fi 到特斯拉转向

开场先是一段亲测体验：Gregor 特意选了星链联网的航班往返英国，"登机即连、全程可用、无需登录"——按他的说法，星链与航空公司合同里写明不得向乘客收费，八个小时的航程真能干活；Sean 也在回程航班上收到了联合航空的免费星链 Wi-Fi 通知（`0:01:11–0:03:08`）。人事方面：Sean 所在的 Confluent 于 12 月初宣布被 IBM 收购，"今年某个时候起该领 IBM 的工资了"；Gregor 去年 10 月前后加入 Supabase，刚开完 200 人的年度线下聚会——半数同事是第一次见面（`0:03:34–0:04:34`）。

头条第一弹是特斯拉"杀掉"了 Autopilot——这个 2014 年上车、从未被允许宣传为"自动驾驶"的辅助驾驶系统将被软件意义上的弃用，资源全面转向 full self-driving 模式。戏剧性在于：就在几周前，有人刚让一辆特斯拉从洛杉矶完全无 assist 地开到纽约，包括高速与充电环节。"它显然能行，但特斯拉决定不去那里。"Waymo 则因车辆越过校车的若干违规正在被调查——Gregor 认为这不影响自动驾驶的大势，新加坡的试点也快了（`0:04:34–0:07:08`）。

### 苹果×Gemini：让 ego 给体验让路

据 Bloomberg 与 TechCrunch 报道，Gemini 驱动的 Siri 将于二月落地；苹果 AI 负责人 John Giannandrea 离任被两人视为战略转向的注脚。Sean 的分析框架是各取所长：苹果强在用户体验与硬件设计、弱在模型，Google 恰好相反——"把两家巨人拼起来做点有趣的事"。两人还回望了语音助手一代的集体失速：Google Assistant、Alexa、Siri 当年许诺的是《她》那样的对话未来，结果沦为定时器与天气播报；ChatGPT 反而实现了原始愿景，一个重要差异是它没有押注语音，而是先用打字界面证明实力（`0:07:50–0:11:44`）。

### OpenAI 取消归属悬崖：抢人的新姿势

华尔街日报报道 OpenAI 将终止员工股权的一年归属悬崖——入职后按月或至少按季开始归属。应用负责人 Fidji Simo 的说法是让新人"敢于冒险而不必担心在拿到股权前被裁"。Sean 的疑虑直白：这可能招来"为钱而来的雇佣兵"而非为使命而来的人。成本侧的数字更惊人：OpenAI 今年预计的股票薪酬约 60 亿美元，接近其预计营收的一半——"每赚一块钱，五毛用来留住造产品的人"。两人顺带科普了流动性事件、二级市场、Databricks 式的回购友好政策与 Shopify 的"薪资-股权滑块"；给求职者的忠告是想清楚这家公司兑现股权的可能路径，别被高估的行权价画饼（`0:12:24–0:21:10`）。

### 红色警报：TPU 与 GPU 之争

节前的大新闻是 OpenAI 的"code red"——Google 在模型生产路线上反超，转折点被归于 Gemini 3（假期前刷屏的信息图大多出自它，Shopify CEO Tobi Lütke 也晒过一张把演讲变成信息图的案例；Nano Banana 的图像生成被 Sean 称为"一步到位"的台阶式跃升，附带伤害是 LinkedIn 被信息图淹没）。Sean 拆解了 Google 的三重不公平优势：一是数据——二十年的搜索索引协议连付费墙内容都拿得到；二是分发——数千个直达数十亿用户的 C 端产品面；三是芯片——GPU 为游戏与图形而生，渲染纹理、物理、光照的"架构包袱"对 AI 纯数学毫无用处，而 Google 2013 年造 TPU 的动因朴素至极：若每个安卓用户每天语音搜索三分钟，数据中心就得翻倍。自研 TPU 还绕开了 NVIDIA 约 75% 的毛利率。OpenAI 取消归属悬崖与这声警报被两人视为同一盘棋的两步（`0:21:23–0:29:04`）。

### Manus 卖身 Meta：20 亿美元的订阅梗

Manus 以约 20 亿美元被 Meta 收购——一个美国大众此前基本没听说的名字。它做的是"生产型"消费 AI：直接产出幻灯片、可托管的完整网站，而非聊天解释；代价是烧钱凶猛——Gregor 亲历过一场会议上用户当面向其 CTO 抱怨" credits 每周烧光"。据报道它有约一亿美元年收入，但产品市场契合度挣扎、融资传闻不断。新加坡渊源是关键背景：公司 2024 年从中国迁来，以脱开"中国生态"标签——两人认为这正是 Meta 敢出手的前提；至于战略意义，场上的玩笑是 Alex Wang 把"买个订阅"办成了"买个公司"，认真的解读只剩一条：Meta 缺能拿得出手的消费级 AI（`0:29:04–0:35:08`）。

### 中段话题：2026，开发者就业市场的冷读

本期正题是就业市场。2025 年的裁员名单（TechCrunch 整理）看着吓人，实际每月规模并不夸张，且不少属于效率重组而非 AI 替代——Google 前几年的被裁者很多已回流新岗位；整体科技就业指标其实在增长，AI/ML/数据技能岗位紧缺。真正的结构性变化在 Stack Overflow 调查的字里行间：Copilot 时代"利好初级、资深不屑"的共识，在编码 Agent 时代翻转——架构理解强的资深工程师借"Agent 实习生"变得更强，而始终被 AI 隔离在细节之外的初级工程师如何成长为资深，成了没人答得好的题。Sean 认为教育重心该从"精通某门语言"挪向"理解如何架构"；Gregor 的反驳偏经验主义：CS 学位没到没用的地步，他自己非科班出身反而吃了基础的亏；他观察到所在公司用 AI 工具的工程师至多对半开——底层代码仍由人写，AI 的甜区是 SQL 与安全审查；开源本该是练兵场，但维护者们已在成批拒掉疑似 AI 生成的 PR。结语调子是"没有新闻标题那么末日"：AI 辅助编码才进入第三个年头，关键的一年还在前面（`0:35:08–0:45:20`）。

### Hacker News 时刻

收官彩蛋是两人不约而同选中的同一个项目：《毁灭战士》被移植进了耳机——doomsbuds.com，运行在固件开源的 PineBuds Pro 上（双核 300MHz ARM、4MB 闪存、三个麦克风），一度还能通过 Twitch 排队遥控体验。此前他们还做过"在 TypeScript 类型系统里跑 Doom"的整期节目（`0:45:59`）。

## 来源与定位

- 原始节目：[SED News: Apple Bets on Gemini, Google's AI Advantage, and the Talent Arms Race](https://softwareengineeringdaily.com/podcasts/sed-news-apple-bets-on-gemini-googles-ai-advantage-and-the-talent-arms-race/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 星链航班的亲测与免费政策（0:01:11–0:03:08）
  - Confluent 被 IBM 收购与 Supabase 聚会（0:03:34–0:04:34）
  - 特斯拉弃用 Autopilot、LA→NY 无辅助横穿（0:04:34–0:06:29）
  - Waymo 调查与新加坡试点（0:06:29）
  - Gemini 版 Siri 二月落地与 Giannandrea 离任（0:07:50–0:11:44）
  - 语音助手失速与 ChatGPT 的打字界面（0:10:02–0:11:44）
  - OpenAI 取消归属悬崖与 60 亿美元股票薪酬（0:12:24–0:18:09）
  - 流动性事件、Databricks 回购、Shopify 滑块（0:19:16–0:21:10）
  - code red、Gemini 3 与 Nano Banana（0:21:23–0:29:04）
  - Google 的数据/分发/TPU 三重优势（0:24:04–0:27:18）
  - Manus 被 Meta 收购与新加坡渊源（0:29:04–0:32:09）
  - Meta 消费级 AI 之缺与订阅玩笑（0:32:50–0:34:31）
  - 2025 裁员盘点与就业总量增长（0:35:08–0:38:06）
  - Stack Overflow 调查与资深/初级之辩（0:38:06–0:41:53）
  - CS 学位、开源练兵场与拒收 AI PR（0:41:53–0:44:48）
  - Doom 进耳机（0:45:59）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 本期为新闻评论节目：文中所引数字（60 亿美元股票薪酬、约 50% 营收占比、NVIDIA 75% 毛利率、Manus 20 亿美元对价与约一亿美元年收入等）均为节目转述或受访者口径，未经独立核实；苹果×Gemini 的落地时间以"据报道"为准。
- 节目中少量与主线无关的闲谈（节日经历、LinkedIn 吐槽的细节等）未纳入正文。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
