# EchoForge — Podcast RSS 源清单

> 人工维护的候选来源池；运行时只读取 `config/sources.yaml`。启用一个来源 = 把对应条目加进 `sources.yaml`（`enabled: true`）。Actions 只采集元信息，不下载音频、不做 ASR、不调用模型。

| ID | Podcast | 方向 | RSS |
| --- | --- | --- | --- |
| `recsperts` \* | Recsperts | 推荐系统 | `https://feeds.transistor.fm/recsperts-recommender-systems-experts` |
| `data-skeptic` \* | Data Skeptic | ML / 数据科学 | `https://dataskeptic.libsyn.com/rss` |
| `latent-space` \* | Latent Space | AI Engineering / Agent | `https://api.substack.com/feed/podcast/1084089.rss` |
| `practical-ai` \* | Practical AI | LLM / ML 工程 | `https://feeds.transistor.fm/practical-ai-machine-learning-data-science-llm` |
| `software-engineering-daily` \* | Software Engineering Daily | 软件工程 / 系统 | `https://softwareengineeringdaily.com/feed/podcast/` |
| `software-engineering-radio` | Software Engineering Radio | 软件工程 / 架构 | `https://rss.libsyn.com/shows/21070/destinations/23379.xml` |
| `cognitive-revolution` | The Cognitive Revolution | Frontier AI / Agent | `https://feeds.megaphone.fm/RINTP3108857801` |
| `developer-voices` | Developer Voices | 数据库 / 编程语言 / 系统 | `https://feeds.zencastr.com/f/oSn1i316.rss` |
| `agentic-conversations` | Agentic Conversations | Agent / MLOps | `https://anchor.fm/s/174cb1b8/podcast/rss` |
| `changelog` | The Changelog | Open Source / DevTools | `https://changelog.com/podcast/feed` |
| `no-priors` | No Priors | AI / 创业 | `https://feeds.megaphone.fm/nopriors` |
| `oxide-and-friends` | Oxide and Friends | 系统 / Infra | `https://feeds.transistor.fm/oxide-and-friends` |
| `gradient-dissent` | Gradient Dissent | ML / AI Infra | `https://feeds.captivate.fm/gradient-dissent/` |
| `dwarkesh` | Dwarkesh Podcast | AI / 深度访谈 | `https://api.substack.com/feed/podcast/69345.rss` |
| `interconnects` | Interconnects | Open Models / RL | `https://api.substack.com/feed/podcast/48206.rss` |
| `talk-python` \* | Talk Python To Me | Python / 后端 | `https://talkpython.fm/episodes/rss` |

带 \* 为当前已启用。

## 维护规则

- 优先使用节目官网或官方托管商的公开 RSS，不用二次聚合 Feed；不保存带用户身份、付费 token 或私密参数的地址。
- 新来源进 `sources.yaml` 前做一次 smoke test：可访问、可解析、有标题和 GUID / 链接等稳定标识。
- Feed 地址迁移时更新 `url`、保留 `source_id`，避免整档节目被识别成新来源。
- 只订阅 The Changelog 的具体节目 Feed，不用 Master Feed。
- 高流量源可用 `include_keywords` 做粗筛（整词匹配、排除词优先，见架构文档 3.1）；需要时再按主题现拟词表。
