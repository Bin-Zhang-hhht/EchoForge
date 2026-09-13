---
item_id: software-engineering-daily-44e3a8d4c67b
title: 'OpenClaw 旋风、ChatGPT 的 60 美元千次曝光与 Mistral 买基础设施：SED News 三月报'
date: '2026-09-14'
published_at: '2026-03-03'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-openclaw-goes-viral-mistrals-compute-play-and-the-agent-arms-race/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/podcasts/sed-news-openclaw-goes-viral-mistrals-compute-play-and-the-agent-arms-race/'
summary: 'Gregor Vand 与 Sean Falconer 的头条双周报：OpenClaw 创始人 Peter Steinberger 卖身 OpenAI、ChatGPT 以每千次曝光 60 美元上线广告、Mistral 收购推理基础设施公司 Koyeb；中段话题是 agentic 编程四个月的剧变与"10x 属性工程师"的黄昏。'
tags: [AI Agent, LLM, 企业 AI]
---

# OpenClaw 旋风、ChatGPT 的 60 美元千次曝光与 Mistral 买基础设施：SED News 三月报

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-03-03 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 4956 字 · 阅读约 13 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [LLM](/tags/LLM/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/sed-news-openclaw-goes-viral-mistrals-compute-play-and-the-agent-arms-race/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/podcasts/sed-news-openclaw-goes-viral-mistrals-compute-play-and-the-agent-arms-race/)

## 速读

距离上期仅数周的 SED News：头条是 OpenClaw 的一个月旋风——奥地利开发者 Peter Steinberger 的开源自主 Agent 从 Clawdbot 改名躲过 Anthropic 的律师函，最终本人加入 OpenAI；随后是 ChatGPT 上线聊天广告（每千次曝光 60 美元）与 Mistral 收购推理基础设施公司 Koyeb；中段话题是过去四五个月 agentic 编程的剧变对软件行业的冲击。

最值得带走的三点：OpenClaw 踩遍了安全专家列出的每条红线（本地文件系统、API keys、"不审查代码直接上生产"）却因此爆红，它预示的是"有人终将以安全的方式做成 24/7 个人助理"这门大生意；ChatGPT 的广告定价（千次曝光 60 美元，与 Netflix 广告档相当、高于 Meta）与 NVIDIA 收回投资承诺的传闻，共同坐实了"订阅模式填不平基础设施投入"的行业判断；Mistral 买下 Koyeb 是模型厂商收购基础设施的第一案——护城河的公式正在变成"模型 + 端到端管道"。

## 主题正文

### OpenClaw：一场把安全建议反着来的爆红

OpenClaw 的故事线被快速铺开：这个开源、自托管、跑在本地机器上的自主 Agent 原名 Clawdbot，被 Anthropic 发了停止侵权函后改名（中间还有个 Moltbot 阶段），最终定名 OpenClaw 配上龙虾图标；而它的创造者 Peter Steinberger——一位曾成功创业、又为 AI 复出的奥地利人——如今加入了 OpenAI（`0:05:27–0:06:20`）。它是什么：给 Agent 你的 API keys、放开本地文件与应用的访问权限，它就变成 7×24 个人助理——管日历、发消息、写代码、在 WhatsApp 等聊天界面上应答。Sean 用旧事作比：当年有同事提议"用邮件当传输层远程执行 bash 命令"，他觉得酷但极度危险——"这就是那件事的 Agent 版，火力拉满"（`0:06:20`）。

爆红的方式 equally 惊悚：安全社区炸锅、有人的 API keys 被嗅探；他们还上线了 Moltbook——一个专供 AI Agent 发帖互动、"人类只能围观"的社交平台；Steinberger 本人的名言是"我没审查代码就推了生产"。Gregor 以 Supabase 员工身份补充了内幕：Steinberger 用 Supabase 做后端但没开行级安全（RLS），出事后背锅的却是 Supabase——"把 RLS 打开，就这么简单"（`0:08:11–0:10:36`）。两人对结局的判断：多数人不会因为安全顾虑用这东西，但已有一小撮人从中获得真实价值；谁能第一个"安全地"做成个人助理，谁就拿下一个远超当下 agentic 工程的大生意——这大概正是 OpenAI 收购其人与其影响力的逻辑。OpenAI 也特意声明 OpenClaw 将交由独立基金会管理，避免"开源项目被收购"的观感（`0:11:25`）。

### ChatGPT 的广告与 Anthropic 的反广告

第二个头条是 ChatGPT 开始在聊天里投放广告，定价为每千次曝光 60 美元——据称与 Netflix 广告档相当、明显高于 Meta。动机被总结为钱：NVIDIA 收回部分投资承诺的传闻连带冲击 Oracle（"Oracle 专门发声明说没影响，专门发声明这个行为本身就说明有影响"），行业共识是订阅费填不上下一代模型的训练投入。Sean 给出了结构性的悲观类比：视频流媒体的黄金年代终结于版权方纷纷自建平台、碎片化成"按需有线电视"；LLM 聊天的黄金年代可能同样止于广告。两人还交换了商业模式情报：Anthropic 靠企业客户"足额甚至超额"付费补贴 20 美元的个人订阅——个人版定价本就低于真实成本；Dario 说过"现在的模型是赚钱的，钱都投进了下一个模型"；OpenAI 则押 B2B 与消费互相导流（Zoom 是先例）（`0:12:11–0:19:43`）。

对照鲜明的是 Anthropic 的"反广告"：据报投了包括超级碗在内的电视广告，创意是把聊天中突然弹出约会广告的噩梦场景演给你看。Gregor 的读法是品牌人设之争——Anthropic 总有"懂用户"的酷劲，OpenAI 则是"我们会告诉你该用什么"。Sean 两周前在 LinkedIn 写过：Anthropic 像早期的 Google，天才扎堆、层级扁平、放养式创新——问题是这种文化能规模化到多远（`0:19:43–0:21:39`）。

亚洲花絮同样有信息量：农历新年（火马年）之际，阿里拿出 4.3 亿美元给通过千问聊天机器人点单的用户送奶茶，六天拉动超 1.2 亿订单。Sean 借此把话题引向 agentic commerce：用户已经习惯先问 AI 再去买，把"问"与"买"接起来只剩时间问题——Google 已在投资安全购买的标准（`0:21:39–0:23:20`）。

### Mistral 买 Koyeb：模型厂商的护城河公式

法国模型公司 Mistral 旗下有 Mistral Compute，这次直接收购了推理公司 Koyeb——Gregor 强调这是"模型厂商整建制收购基础设施提供商"的第一案：Koyeb 约 13 人、客户更成熟，不像 Lovable 此前收购的三人小团队 Molnett 那么轻。一个细节也被点破：Koyeb 的数据库/容器化应用能力背后其实是 Neon 在供货——隔着一层，Mistral 仍然认为值得买。Sean 总结出的护城河逻辑：光有模型，切换成本就低；当模型附带了业务上下文、Agent 托管、应用部署，"为什么要走"就成了问题——模型正在长出端到端管道。由此引出悬念：Lovable 这类应用层公司往哪走？Gregor 预测今年所有玩家都会有"台阶式"动作（`0:25:43`）。

### 中段话题：agentic 编程的四个月剧变

为什么突然连主流媒体都在宣告"编程被颠覆"？Gregor 的风向标是退休且不在科技圈的父亲的转发。Sean 拆解了变化的结构：一次性生成函数的时代只有两三成的效率改善，而现在的 agentic 工程——Claude Code、Cursor、Codex 5.3——能把几小时的活一次性完成；再往上是 Ralph Wiggum 循环、Gastown 与多 Agent 编排（Steve Yegge 的说法是 Agent 把聊天放进了循环，而这些把 Agent 放进了循环），桌面上摆六台 Mac mini 常驻跑 Agent 的玩家已经出现；MCP 服务器生态爆发与上下文压缩让一切更顺滑。Gregor 补了自己的一个"毛骨悚然时刻"：新开一个 Claude 会话，对方主动接上了他另一个项目的上下文（`0:26:33–0:33:07`）。

由此抛出的组织问题相当扎心：PM 与工程师的比例还要不要维持？前后端的分工还清晰吗？当语言与框架的深度专长可以外包给 Agent，人的价值向品味、判断与人际协调迁移——Sean 直接点名"10x 属性工程师"（靠不可替代的专长让团队容忍其糟糕协作的老兵）在 AI 优先的公司里还剩多少位置；Gregor 补充谈判是硬通货——两个专家有分歧时，不会有人提议"让 OpenClaw 裁决"，因为"你的 Agent 怎么配置的、凭什么信"（`0:33:07–0:36:10`）。至于"是不是要不了那么多工程师"，Sean 用工业革命作类比：务农的人少了、产出反而爆炸，但转型期对身处其中的人并不温柔。对"有了 Codex 谁还需要 SaaS"导致 SaaS 股票下挫的说法，两人一致认为是金融市场的膝跳反应——SaaS 公司的价值从来不只是代码（`0:39:40–0:41:47`）。

另一个积极面被反复强调：工具把"爱好者开发者"带回来了——80 年代一个人就能写出被千万人使用的游戏，如今一次性小应用的成本趋近于零（OpenClaw 本身就是单人作品的最佳注脚），代价是噪音也更多。Gregor 补充了体感：现在爱好者项目的水准期望值（UI、顺滑度）被抬得极高，而 Supabase 这类工具正是把数据库与认证的时间压缩到近零的推手（`0:41:47–0:43:09`）。

### Hacker News 与下月预测

HN 环节的四件宝：其一，"老式视觉特效：云雾水箱"——斯皮尔伯格时代用巨型水箱拍《第三类接触》《夺宝奇兵》的大气效果；其二，把 2D 航班追踪做成 3D 地球的项目（住在航线下方的 Gregor 福利：常见三条航线垂直堆叠、相隔约 2000 英尺）；其三，有人逆向工程 1990 年 DOS 版《铁路大亨》——修了金额溢出 bug、渲染分辨率无关化、去掉存档上限，顺带剖析了当年运行时覆写代码的 overlay 与帧缓冲把戏；其四，GrapheneOS 冲上千分——强化内核、把 Google Play 服务关进隔离环境，缺点是只支持 Pixel（`0:44:20–0:51:15`）。

下月预测：Sean 押"垂直化的 Claude Code"（Anthropic 已上线 Co-work，还有面向金融服务的版本）——但他也指出工程之外的行业要过关很难，因为编码是个"硬真值环境"：失败可检查、git 分支可回滚，法律这类领域缺的就是这些。Gregor 押模型厂商推出"别把代码跑在别家、跑我这"的一体化服务；他还转述了一位 DevRel 的观察：vibe coder 们正从 Lovable 迁往 Cursor——"不够 pro 了"。至于真假，下月见分晓（`0:51:32–0:53:51`）。

## 来源与定位

- 原始节目：[SED News: OpenClaw Goes Viral, Mistral's Compute Play, and the Agent Arms Race](https://softwareengineeringdaily.com/podcasts/sed-news-openclaw-goes-viral-mistrals-compute-play-and-the-agent-arms-race/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 东京见闻与星链对比（0:01:33–0:05:27）
  - OpenClaw 沿革：Clawdbot→OpenClaw、Steinberger 加入 OpenAI（0:05:27–0:06:20）
  - OpenClaw 是什么与邮件执行命令的旧事（0:06:20）
  - Moltbook、API key 嗅探、"不审查就上生产"与 Supabase RLS（0:08:11–0:10:36）
  - 安全个人助理的生意与独立基金会声明（0:10:36–0:12:11）
  - ChatGPT 广告定价与 Oracle/NVIDIA 传闻（0:12:11–0:14:11）
  - 流媒体黄金年代类比与订阅经济学（0:14:11–0:17:25）
  - Anthropic 企业补贴个人、B2B 导流（0:16:03–0:19:43）
  - Anthropic 超级碗反广告与"早期 Google"类比（0:19:43–0:21:39）
  - 阿里千问奶茶战役与 agentic commerce（0:21:39–0:23:20）
  - Mistral 收购 Koyeb 与 Neon 细节（0:25:43）
  - 护城河公式与 Lovable 的处境（0:25:43）
  - agentic 编程剧变：Opus 4.6、Codex 5.3、Ralph Wiggum/Gastown（0:26:33–0:31:07）
  - 上下文压缩与跨项目记忆时刻（0:31:07–0:33:07）
  - 组织之问与"10x 属性工程师"（0:33:07–0:36:10）
  - CLI/桌面作为 Agent 居所与本地优先（0:37:08）
  - 工业革命类比、SaaS 股票膝跳（0:39:40–0:41:47）
  - 爱好者开发者复兴（0:41:47–0:43:09）
  - HN：云雾水箱、3D 航班追踪、铁路大亨逆向、GrapheneOS（0:44:20–0:51:15）
  - 下月预测：垂直化与"跑我这"（0:51:32–0:53:51）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 本期为新闻评论节目：所引数字（60 美元/千次曝光、4.3 亿美元、1.2 亿订单、约一亿美元年收入等）均为节目转述或受访者口径，未经独立核实；NVIDIA/Oracle 一节为节目中的传闻性评论，文中以"传闻"标注。
- 逐字稿个别词形按上下文校订（如消息渠道 "Teleport" 当为 Telegram）；开场闲谈（买房、东京旅行细节）仅择要保留。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
