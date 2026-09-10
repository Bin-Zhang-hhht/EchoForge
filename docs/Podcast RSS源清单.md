# EchoForge — Podcast RSS 源清单

> 版本：v0.6 · 2026-09-11  
> 用途：维护经过人工调研的候选 Podcast RSS 白名单，供 `config/sources.yaml` 选择性启用。  
> 原则：只记录公开、无需私有令牌的 Feed；RSS 只是发现和元信息入口，Actions 不下载音频、不做 ASR、不调用大模型。本版仅同步 **EchoForge** 命名与 v0.6 版本，来源池本身不变。

## 1. 使用方式

这份清单是“来源池”，不是要求首版一次性全部启用。

M2 首次联调只启用 5 个 Feed：

1. Recsperts
2. Data Skeptic
3. Latent Space
4. Practical AI
5. Software Engineering Daily

这 5 个来源已经覆盖推荐系统、机器学习、AI Engineering、Agent / LLM 和通用软件工程，足够验证 RSS 解析、GUID 去重、过滤、积压查看和来源失败隔离。

首批跑稳后，再按实际阅读价值逐步加入其余核心源。候选源默认不要求进入首版验收。

## 2. 核心来源

| ID | Podcast | 方向 | 推荐策略 | RSS |
| --- | --- | --- | --- | --- |
| `recsperts` | Recsperts | 推荐系统 / RecSys | **强烈推荐，全量收集元信息。** 主题高度垂直，适合作为推荐系统核心来源。 | `https://feeds.transistor.fm/recsperts-recommender-systems-experts` |
| `data-skeptic` | Data Skeptic | ML / 数据科学 / 推荐系统 | **强烈推荐。** 历史主题较广，可先全量入库，再由本地任务判断是否处理。 | `https://dataskeptic.libsyn.com/rss` |
| `latent-space` | Latent Space | AI Engineering / Agent / Infra | **强烈推荐。** 对 Agent、模型、推理、AI Infra、开发者工具覆盖较好。 | `https://api.substack.com/feed/podcast/1084089.rss` |
| `practical-ai` | Practical AI | LLM / Agent / ML 工程 | **强烈推荐。** 偏落地实践，适合中文技术精编。 | `https://feeds.transistor.fm/practical-ai-machine-learning-data-science-llm` |
| `software-engineering-daily` | Software Engineering Daily | 软件工程 / 数据库 / AI / 分布式系统 | **强烈推荐，但建议关键词过滤。** 更新频率较高，主题跨度较大。 | `https://softwareengineeringdaily.com/feed/podcast/` |
| `software-engineering-radio` | Software Engineering Radio | 软件工程 / 架构 | **推荐。** 偏长期有效的工程知识，适合补充非 AI 内容。 | `https://rss.libsyn.com/shows/21070/destinations/23379.xml` |
| `cognitive-revolution` | The Cognitive Revolution | Frontier AI / Agent / RL / AI research | **推荐，精选处理。** 访谈较长，技术和产业讨论并存。 | `https://feeds.megaphone.fm/RINTP3108857801` |
| `developer-voices` | Developer Voices | 数据库 / 编程语言 / 系统 / AI | **推荐。** 深度技术访谈多，适合作为软件工程高质量来源。 | `https://feeds.zencastr.com/f/oSn1i316.rss` |
| `agentic-conversations` | Agentic Conversations（原 MLOps.community） | Agent / MLOps / Production AI | **推荐，关键词过滤。** 适合 Agent、MCP、生产部署与 AI Infra。 | `https://anchor.fm/s/174cb1b8/podcast/rss` |
| `changelog` | The Changelog | Open Source / DevTools / 工程实践 | **推荐，关键词过滤。** 只订阅主节目，不使用 Changelog Master Feed。 | `https://changelog.com/podcast/feed` |

## 3. 候选来源

这些节目质量高，但并不需要首版全部启用。保留在来源池，后续根据实际文章产出价值决定是否加入 `config/sources.yaml`。

| ID | Podcast | 方向 | 建议 | RSS |
| --- | --- | --- | --- | --- |
| `no-priors` | No Priors | AI / 创业 / Frontier AI | 技术与商业混合，适合按标题和简介筛选。 | `https://feeds.megaphone.fm/nopriors` |
| `oxide-and-friends` | Oxide and Friends | 系统 / 硬件 / Infra / 计算机文化 | 很硬核，但跨度较大，精选处理。 | `https://feeds.transistor.fm/oxide-and-friends` |
| `gradient-dissent` | Gradient Dissent | ML / AI Infra / 创业 | ML 工程与产业内容混合，按主题筛选。 | `https://feeds.captivate.fm/gradient-dissent/` |
| `dwarkesh` | Dwarkesh Podcast | AI / 科学 / 深度访谈 | 信息密度高但单集通常较长；先看 metadata，再决定是否进入转写。 | `https://api.substack.com/feed/podcast/69345.rss` |
| `interconnects` | Interconnects | Open Models / RL / Post-training | 研究味较强，适合 Frontier AI 专题。 | `https://api.substack.com/feed/podcast/48206.rss` |
| `talk-python` | Talk Python To Me | Python / Data / 后端 / AI | 节目稳定但范围较广，建议关键词过滤。 | `https://talkpython.fm/episodes/rss` |

## 4. 关键词建议

首版不做复杂评分系统，只保留确定性过滤。以下词表用于 `title + description` 的粗筛，后续根据真实积压再调整。

### 4.1 推荐系统

```text
recommendation
recommender
recSys
ranking
retrieval
personalization
personalisation
candidate generation
matching
ads
advertising
search ranking
feed ranking
```

### 4.2 AI / Agent

```text
LLM
agent
agentic
MCP
reasoning
inference
RAG
post-training
reinforcement learning
RL
fine-tuning
open model
foundation model
AI infrastructure
GPU
serving
context engineering
coding agent
```

### 4.3 软件工程 / Infra

```text
database
distributed
storage
compiler
runtime
Kubernetes
container
observability
DevOps
SRE
streaming
query engine
Linux
Rust
Python
TypeScript
architecture
```

不建议一开始设置过窄的排除词。广告、寒暄和赞助内容由后续正文整理阶段删除，不依赖 RSS 关键词判断。

## 5. 建议的首批 `sources.yaml`

M2 联调阶段建议只放下面 5 个真实源。先验证稳定性，再扩展数量。

```yaml
sources:
  - id: recsperts
    name: Recsperts
    url: https://feeds.transistor.fm/recsperts-recommender-systems-experts
    enabled: true
    include_keywords: []
    exclude_keywords: []
    min_duration_minutes: null

  - id: data-skeptic
    name: Data Skeptic
    url: https://dataskeptic.libsyn.com/rss
    enabled: true
    include_keywords: []
    exclude_keywords: []
    min_duration_minutes: null

  - id: latent-space
    name: Latent Space
    url: https://api.substack.com/feed/podcast/1084089.rss
    enabled: true
    include_keywords: []
    exclude_keywords: []
    min_duration_minutes: null

  - id: practical-ai
    name: Practical AI
    url: https://feeds.transistor.fm/practical-ai-machine-learning-data-science-llm
    enabled: true
    include_keywords: []
    exclude_keywords: []
    min_duration_minutes: null

  - id: software-engineering-daily
    name: Software Engineering Daily
    url: https://softwareengineeringdaily.com/feed/podcast/
    enabled: true
    include_keywords:
      - AI
      - agent
      - LLM
      - recommendation
      - ranking
      - database
      - distributed
      - infrastructure
      - compiler
      - DevOps
    exclude_keywords: []
    min_duration_minutes: null
```

## 6. 扩展顺序

首批 5 个来源稳定后，建议按下面顺序增加，而不是一次性全部打开：

```text
第一批：Recsperts / Data Skeptic / Latent Space / Practical AI / Software Engineering Daily
    ↓
第二批：Software Engineering Radio / Developer Voices / Agentic Conversations
    ↓
第三批：The Cognitive Revolution / The Changelog
    ↓
候选：No Priors / Oxide and Friends / Gradient Dissent / Dwarkesh / Interconnects / Talk Python To Me
```

是否升级为核心源，只看真实使用结果：有多少节目通过初筛、最终生成多少值得阅读的文章、重复主题是否过多，以及长音频是否带来过高的本地处理成本。不为此建立额外评分服务。

## 7. RSS 维护规则

- 优先使用节目官网或官方托管商公开的 RSS，不使用二次聚合 Feed。
- 不保存带用户身份、付费订阅 token 或私密参数的 RSS。
- 每个来源进入生产配置前，用采集器做一次 smoke test：HTTP 可访问、可解析、至少存在标题和稳定标识，Podcast Feed 应能读取 enclosure/audio 信息（若节目提供）。
- Feed 临时失败只记录错误并继续其他来源；不要因为单个源失败中断全部采集。
- Feed 地址迁移时更新 `url`，保留 `source_id`，避免因为换托管商把整个节目识别成新来源。
- 不订阅 The Changelog 的 Master Feed，以减少重复和无关节目；只保留需要的具体节目 Feed。

## 8. 本次核查说明

核查日期：2026-09-11。

本轮确认了上述来源仍可找到公开节目入口，并对主要 RSS 地址进行了直接 Feed 端点检查；RSS/XML 端点不一定适合浏览器页面直接展示，但可供标准 RSS 解析器读取。实际实施时仍以 `feedparser`/等价解析库的 smoke test 为最终准入条件。

节目定位参考：

- Recsperts — https://recsperts.com/
- Data Skeptic — https://dataskeptic.com/
- Latent Space — https://www.latent.space/
- Practical AI — https://practicalai.show/
- Software Engineering Daily — https://softwareengineeringdaily.com/
- Software Engineering Radio — https://se-radio.net/
- The Cognitive Revolution — https://www.cognitiverevolution.ai/
- Developer Voices — https://www.developervoices.com/
- Agentic Conversations / MLOps.community — https://mlops.community/
- The Changelog — https://changelog.com/podcast
- Dwarkesh Podcast — https://www.dwarkesh.com/
- Interconnects — https://www.interconnects.ai/podcast
- Talk Python To Me — https://talkpython.fm/
