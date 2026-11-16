---
item_id: software-engineering-daily-44b68b31eb04
title: 'GitLab 与 DevSecOps 的进化：平台整合、Agent 治理与气隙部署'
date: '2026-11-17'
published_at: '2026-11-10'
transcribed_at: '2026-11-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/gitlab-and-the-evolution-of-devsecops/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/11/SED1977-GitLab-2026.txt'
summary: 'GitLab 工程副总裁 Tim Zallmann 对谈平台如何从“开源 GitHub”长成 DevSecOps 编排平台：把 AI 带进完整 SDLC，用 Orbit 知识图谱补企业级上下文与依赖排查，以复合身份和全程会话审计支撑治理与合规，并以自管理与气隙部署服务政府等受监管行业。'
tags: [开发者工具, 安全, 开源, AI Agent]
---

# GitLab 与 DevSecOps 的进化：平台整合、Agent 治理与气隙部署

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-11-10 · 逐字稿获取：2026-11-17 · 笔记整理：2026-11-17
>
> 全文共 13894 字 · 阅读约 35 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [安全](/tags/%E5%AE%89%E5%85%A8/) [开源](/tags/%E5%BC%80%E6%BA%90/) [AI Agent](/tags/AI%20Agent/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/gitlab-and-the-evolution-of-devsecops/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/11/SED1977-GitLab-2026.txt)

## 速读

GitLab 工程副总裁 Tim Zallmann 做客本期，与主持人 Gregor Vand 聊这家平台如何从“开源 GitHub”长成覆盖从想法、构建、部署到运行维护全程的 DevSecOps 编排平台，又如何在 AI 时代把上下文、治理与审计做成一套企业级组合。适合关注企业级 AI 平台设计、DevSecOps 落地与受监管行业（政府、汽车、金融）部署实践的读者。

最值得带走的三点：一是 Duo Agent Platform 把 agent 与确定性步骤组合成可扩展的 flows，目标是把 AI 带进完整 SDLC，他的团队已实现 bug 自动复现、自动修复、录屏取证并开出待合并 MR 的“no touch”流程；二是 beta 中的 Orbit 知识图谱把平台内数据索引成关系图（权限与终端用户对齐），让 agent 能在数万仓库中秒级定位依赖风险；三是复合身份（service account 附带发起用户）加服务端执行的全程会话审计支撑治理与合规，而自管理与气隙部署则是这套平台在受监管行业立足的现实底座。

## 主题正文

### 从“开源 GitHub”到 DevSecOps 编排平台

Tim 已在 GitLab 待了九年半，入职时公司大约 112 人，如今超过 2000 人。按他的定位，GitLab 本质上是“给软件团队构建软件用的平台”，再深一层是 DevSecOps 编排平台——目标是团队从想法、构建、部署到运行、维护的每一步都在同一平台完成。（原文锚点：`I'm here for nine and a half years`；`we are an orchestration platform for DevSecOps`）

路径是从 git 与源码管理起步、很早“与 CI/CD 联姻”，随后在代码评审上做强，再扩展到规划与安全领域，把这些能力装进一个平台。他强调安全扫描器是 GitLab 相当强的部分，对企业客户尤为重要。（原文锚点：`we married it with CI/CD`；`We have security scanners`）

开源是底色：GitLab 至今是完全的 open core 公司，源码可查，社区甚至客户都在贡献——有团队直接与客户工程师共建特性，他举例嵌入式开发客户需要在数百台设备上做构建后测试的场景。主客群是大型企业，有客户拥有数以万计的工程师与活跃项目；平台全球有数百万用户、数千套自管理安装。（原文锚点：`We are a completely open core company`；`Our main customer base is in enterprises, especially also large enterprises`；`tens of thousands of engineers`）

他反复强调自管理是巨大优势：版本可下载、可本地部署，甚至有客户在完全气隙、无任何互联网连接的高安全环境运行；这给客户带来可控环境，对可靠性、数据主权与可适配性都很重要。代价是升级由客户自己掌握，他也提醒工程师必须理解“有客户还在跑两年前的版本”意味着什么。（原文锚点：`We have even customers who run it completely air-gapped`；`this person is running a two-year-old version`）

### 上下文、治理与审计：平台 AI 战略的三个支点

Tim 把 GitLab 在 AI 时代的差异化概括为三点组合。其一是上下文：平台握有全部 issue 及其讨论、设计、epic 与主题间关系，还有测试、构建、部署、所在云环境乃至可观测性数据，都可以交给 agent——这是只对着本地代码跑 CLI 的工具给不了的。（原文锚点：`we have all the issues, all the discussions around the issues, the designs, the epics`；`We can even go and bring in observability data`）

其二是治理：企业需要非常细的粒度去控制 agent 与用户分别能做什么，不同客户的限制互不相同，平台要能同时满足双方。其三是审计：以他举例的一万五千名工程师全天候产出为背景，组织必须有观察能力；AI 让这一点更重要，因为公司里多出了会“干疯事”的额外团队。他说如今每个新特性都要同时做到上下文增强、治理与审计，这就是今天的 GitLab。（原文锚点：`what agents can do, what their users can do`；`if you have 15,000 engineers who are doing stuff every day`）

### Duo Agent Platform：把 AI 带进完整 SDLC

Duo Agent Platform 是他与团队长期构建的主线，愿景是把 AI 带到完整 SDLC——像当年做 CI/CD 那样，让生命周期任意一点都能运行 agentic 能力，而不只是“问一句、写段代码”的点状工具。他说很多客户的第一步不是让 AI 写代码，而是让 AI 做代码评审；另一端则是完全自治。（原文锚点：`to bring AI to the full SDLC`；`run agentic stuff at any point in the SDLC`；`getting code reviewed by AI`）

平台支持客户构建 custom flows——agent 与确定性步骤的组合：跑 lint、跑测试这类确定性步骤结果是二元的、目标明确，通常也比让 agent 自己摸索便宜。整套平台完全模型无关，有客户在本地跑自己的模型，从而在 AI 环节同样保有对数据归属与流向的清晰掌控。（原文锚点：`combination between agents and deterministic steps`；`running linting, running tests`；`also completely model agnostic`；`run it with their own models on premise`）

开箱即用的是一组基础 agent 与基础 flows：在 issue 或 merge request 的任意评论里 @ Duo 开发者即可派活；MR 流水线红了可以自动触发修测试、修流水线的 flow；可以配置清晨六点跑的 custom flow，汇总 GitLab issue、MR 以及 Incident.io、Sentry 里的生产信号，生成现成的站会简报。此外还有直接的 AI 代码评审、修复流水线，以及安全漏洞进来即自动处置的流程。（原文锚点：`mention a Duo developer in any comment in an issue`；`tries to fix the tests and fixes the pipeline for you`；`received all the information maybe from Incident.io and from Sentry`；`if a security vulnerability comes in, it's automatically resolved`）

他自己部门的一个团队已把 bug 分诊自动化：bug 报告进来，triage agent 会收集周边信息、在自己的 VM 里复现并录下复现视频，符合条件就立即尝试修复，修复前后再各录一次屏、连同 MR 一起贴出来——工程师早上进来看到的是完整的分诊信息、对应的 MR 和视频，可以直接批准合并。他把这个方向称为“no touch”：人把任务交给 agent 后 fire and forget，agent 跑到流水线全绿、内部 AI 评审通过，再把结果、视频和测试证据交回。（原文锚点：`tries to reproduce it in its VM, is creating then a video of the reproduction`；`screen record the fix before and after`；`I call this no touch`）

### Orbit：跨 SDLC 的知识图谱（beta）

Orbit 目前是 GitLab 之上处于 beta 阶段的大型 add-on：一个覆盖整个 SDLC 的知识图谱，把平台内已有信息（直到代码）全部索引并建立关系——例如索引一个 epic 就知道其子项，从子项到相关 issue、到对应 MR、到 diff 改动、再到被改动的函数。关键设计是权限对齐：知识图谱只包含终端用户本来就能看到的信息，再把这种访问交给 agent，让它们不必逐文件翻找就能理解关系。（原文锚点：`currently in beta phase to GitLab itself, which is Orbit`；`a knowledge graph across the whole SDLC`；`the knowledge graph has only the same information that you would be also be able to see as an end user`）

主持人 Gregor 转述他的理解：Orbit 是图结构，几乎被定位成 RAG 的替代品，开发生命周期数据经 CDC 进 ClickHouse、支持解析 12 种语言。Tim 的回答是：很多用例 RAG 加 agent 也能做，但 agent 要“看很多次”才能找全；Orbit 把已有数据及其全部引用关系索引起来，直接给 agent 一张地图——“这个文件被另外 7 个文件引用”是指针而不是 grep 式暴力搜索。（原文锚点：`being positioned instead of RAG`；`via change data capture into ClickHouse`；`And it can parse through 12 languages on that basis`；`gives the agent a map into their hand`）

agent 还可以取回当前 schema 并即时编写查询、遍历关系、找到相似数据；他确认所有数据存储在 ClickHouse，并强调 Orbit 的价值在宽口径统计分析类查询与精确性——多 GB 级的巨石仓库里，一个函数可能还有 10 处引用，知识图谱能保证 7 处引用全部列出。（原文锚点：`access to retrieve the current schema and to write queries against it`；`All the data is stored in ClickHouse`；`huge monoliths, which are multi-gigabytes`）

杀手级用例是依赖风险排查：他说有客户拥有 5 万个仓库，如果明天进来一份 CSV、说某依赖的某版本有安全问题，Orbit 可以对全部项目即时查询，几秒内找出哪些仓库跑着这个确切版本——这是本地 CLI 加单仓库做不到的事。另一个方向是内部依赖：很多项目的内部 UI 组件库没有发布到 NPM，agent 本身够不着；本地知识图谱可以与实例上的远端知识图谱关联，直接找到所用函数的源头。（原文锚点：`I know some customers who have 50,000 repositories`；`there is a security problem with dependency ABC`；`it can literally give you an answer in seconds`；`might not be published on NPM`；`a local knowledge graph with a remote knowledge graph`）

### 开放而非封闭：外部 Agent、MCP 与 AI Gateway

Tim 对封闭性看得很实际：“人们不会只用 GitLab”，不少客户至今仍用 Jira 做规划与项目管理。因此 Duo Agent Platform 按平台的方向开放：可以把 Claude Code 作为平台上的 runner job 运行来实现任务，也支持 Codex 等外部 agent。（原文锚点：`people just use GitLab and nothing else in the world`；`use Jira for planning and project management`；`We also support Codex and others`）

数据同样开放：官方 GitLab MCP server 接近 GA，可以以经典 MCP 方式访问基础数据；Orbit 本身也以 MCP gateway 的形式暴露，早期 beta 阶段已可直接试用。（原文锚点：`an official GitLab MCP server, which is very close to going to GA`；`we also expose Orbit as an MCP gateway`）

AI Gateway 分三层形态。默认情况下，无论 .com 还是自管理实例，Duo Agent Platform 都连接 GitLab 运营的多租户网关，模型开箱即用，客户无需自己与多家模型供应商签约。其次，自管理客户可以自装 AI 网关——否则“自管理实例→云端网关→客户本地模型”是太远的 ping-pong；这一能力同时支撑完全不连外网的气隙环境，他称已有不少满意客户在跑这类自定义模型配置。（原文锚点：`It's a multi-tenant gateway`；`run and self-install an AI gateway`；`that's a very far ping-pong`；`to support an air-gapped environment where there is no connection to the outside world`）

第三层面向 Dedicated——介于 .com 与自管理之间、由 GitLab 为客户托管运行的单租户版本：把单租户 AI Gateway 带到了 GA，拥有 Dedicated 合同与实例的客户可以连接自己的模型。他强调 AI 版图变化极快，这种“无论什么理由都能保有的灵活性”很重要。（原文锚点：`this is exactly what we have brought now to GA`）

### 复合身份与全程审计：企业治理的落地

企业客户基于自身监管与合规设置，需要既能细粒度配置、又能事后讲清“事情怎么发生”的能力。GitLab 的答案是复合身份（composite identity）：agent 运行在所谓的 service account 上——即 agent 本身的账号——但平台始终附带记录是哪个用户发起了当前任务；即便进入自治流程（建 issue、交给 agent 出实现计划再到实现），事后仍能追溯“这是这个 agent、这个配置跑的，但由这个用户发起”。（原文锚点：`the composite identity`；`we always attach which user has started`；`it was initiated by this user`）

控制粒度随之做细：可以规定某类 agent 只允许用某些工具、且每次都要审批（他表示这种“永远要审批”的能力正在建设中），可指定允许使用的 MCP server，并锁定到 skill 级别；管理员发布的 skill 甚至带数字签名，执行引擎与 CLI 能发现篡改。（原文锚点：`this kind of agent is only allowed to use these tools`；`this is locked down up to the level of skills`；`these skills are available, and they are even digitally signed`）

另一处与其他方案的不同：平台上的一切执行——包括本地代码变更这类本地 workload——都在服务端构建和执行，而不是把 prompt 发给 API 了事，因此能保证治理、合规与审计轨迹。CLI、IDE 插件、网页聊天、自治 flow 中的每个会话都是一个 Duo Agent Platform session，记录模型的每条返回、每次工具调用与每次审批。（原文锚点：`always built up and executed on the server`；`versus something that just sends LLM prompts to an API`；`we can ensure certain governance, compliance, auditing trails`；`trace and track everything`）

跨用户审计因此可行——企业能知道内部某个 agent 试探了多少次 API key、用了哪些工具，进而控制终端用户与 agent 各自的可行范围；workload 甚至能在本地与远端之间迁移。几个月后仍可回放：这个用户、这个时间、这个模型、全部步骤与工具调用——这段代码就是这么来的。（原文锚点：`has tried to find an API key`；`move workload from local to remote and from remote to local`；`know this user on this time with this model`）

### 气隙部署的现实：发布节奏、升级纪律与行业版图

回到气隙话题，Tim 说这不是当年刻意规划的产品路线，而是“发生在 GitLab 身上”：因为一直提供自管理，需要气隙的客户自然找上来；至今公司大部分收入仍来自自管理——他知道不少竞品曾提供自管理、后来要求“人人都得迁到云上”，GitLab 没有走这条路，而是继续做成不连任何地方、不需要 ping 谁、不需要在线下载东西的版本。（原文锚点：`air-gapped originally came simply and happened to us`；`our majority of revenue comes from self-managed`）

这反过来塑造了工程纪律：每个月的某个时点切发布、打成包，客户拿到后可能数月停在那一版；有客户的版本老旧不是以月计而是以年计。工程师必须理解这种节奏。（原文锚点：`This release is put into a package`；`I'm not talking about months. I'm talking about years`）

因此要把 breaking changes 压到绝对最少：只在每年一次的大版本里做，部分变更需要提前六个月乃至十二个月公告；质量与测试也变成完全不同的题目——要在不同环境、不同设置里跑，而不能只测云端那一份。他提醒工程师：你写的东西可能四个月后才落到某台客户机器上；有人忘了某个镜像不能再随手下载，客户七个月后才回来问“为什么在下载东西”。（原文锚点：`reduce the amount of breaking changes to an absolute minimum`；`once a year a major version`；`announced six months or rather 12 months ahead of time`；`the customer comes back seven months later`）

而平台方能提供的，主要是按客户规模区分的参考架构；硬件与配置不可控——他记得有客户的 Git 服务跑在机械硬盘而非 SSD 上，几千用户一上来就慢得惊人。他视这种“控制不了”为巨大复杂度、也是巨大优势：“这就是我们的市场。”（原文锚点：`a so-called reference architecture for different sizings`；`not on SSDs, but rather on classic hard drives`）

哪些行业需要气隙？他说经典是政府与高安全领域；汽车业有大量从未进入开源世界的专有软件，当然也不愿把这类源码发给 AI 模型；金融安全软件同样巨大。他提醒人们常对客户构成感到意外：如今各类公司都在造软件；还有客户同时运营非气隙与气隙两套实例，为部分项目加一层安全。（原文锚点：`government and high security topics are the classic ones`；`send that kind of source code to AI models`；`an instance that is not air-gapped and an instance that is air-gapped`）

### 生态变局与组织调适

主持人提到 Cursor 等新玩家宣布进入代码仓库托管空间，Tim 回应说这一两年该领域变化的速度与数量前所未见，公司纷纷转向、进入他人的领地，Cursor 进入代码托管“是个有意思的动作”。他的定位是：与 Cursor 既竞争又互补，正在与 Cursor 等伙伴合作做好集成、互相把 agentic 能力带给对方；他认可 Cursor 执行得很好、移动很快，但认为 GitLab 在企业市场提供完整平台的地位稳固——代码托管正是许多年前起步、此后大幅扩展的地方。（原文锚点：`coming into the code repository space`；`the speed and amount of change in that space has never been higher`；`competitive, but we are also very much complementary`；`We are doing partnerships with Cursor and others`）

复盘变化时他说：两三年前主要对手还是 GitHub 与 Jira，如今竞争者与技术可能性都多得多；紧迫感很重要，但不应过度放大——不能什么新风潮都追，有些十天后就过时了。组织上，一年半前他把部门压平、更贴近彼此与 AI 项目——GitLab 要同时有客户端、AI 客户端、IDE 插件、CLI、网页 agentic 聊天，加上网关与模型供应商这些外部变量，必须更轻更快地转向。（原文锚点：`our main competitor is GitHub`；`We flattened the organization to be much closer to each other`）

收尾时他分享的内部效果：站会、状态报告在他的部门已完全自动化，人们省下的时间转向改进测试、减少技术债与创造前向价值；产品侧刚发布了带全新 agentic loop 的完整新 CLI，他邀请听众去 GitLab.com 试用。（原文锚点：`everything is currently completely automated in my department`；`complete new CLI with a complete new agentic loop`）

## 来源与定位

- 原始节目：[GitLab and the Evolution of DevSecOps](https://softwareengineeringdaily.com/podcasts/gitlab-and-the-evolution-of-devsecops/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 九年半任期与公司规模变化（原文锚点：`I'm here for nine and a half years`）
  - DevSecOps 编排平台定位（原文锚点：`we are an orchestration platform for DevSecOps`）
  - 与 CI/CD 联姻、向规划与安全扩展（原文锚点：`we married it with CI/CD`）
  - 安全扫描器是强项（原文锚点：`We have security scanners`）
  - 完全 open core 公司（原文锚点：`We are a completely open core company`）
  - 主客群是大型企业（原文锚点：`Our main customer base is in enterprises, especially also large enterprises`）
  - 数万工程师规模的客户（原文锚点：`tens of thousands of engineers`）
  - 自管理与完全气隙客户（原文锚点：`We have even customers who run it completely air-gapped`）
  - 客户可能停留在两年前的版本（原文锚点：`this person is running a two-year-old version`）
  - 平台上下文：issue、讨论、设计、epic（原文锚点：`we have all the issues, all the discussions around the issues, the designs, the epics`）
  - 可观测性数据接入 agent（原文锚点：`We can even go and bring in observability data`）
  - 对 agent 与用户的细粒度治理（原文锚点：`what agents can do, what their users can do`）
  - 大规模审计的动因（原文锚点：`if you have 15,000 engineers who are doing stuff every day`）
  - Duo Agent Platform 的完整 SDLC 愿景（原文锚点：`to bring AI to the full SDLC`）
  - 生命周期任意一点运行 agentic 能力（原文锚点：`run agentic stuff at any point in the SDLC`）
  - 客户常从 AI 代码评审起步（原文锚点：`getting code reviewed by AI`）
  - custom flows＝agent＋确定性步骤（原文锚点：`combination between agents and deterministic steps`）
  - 平台完全模型无关（原文锚点：`also completely model agnostic`）
  - 评论里 @ Duo 开发者派活（原文锚点：`mention a Duo developer in any comment in an issue`）
  - 红流水线自动修复（原文锚点：`tries to fix the tests and fixes the pipeline for you`）
  - 站会简报聚合 Incident.io 与 Sentry（原文锚点：`received all the information maybe from Incident.io and from Sentry`）
  - 安全漏洞自动处置（原文锚点：`if a security vulnerability comes in, it's automatically resolved`）
  - bug 分诊 agent 在 VM 复现并录屏（原文锚点：`tries to reproduce it in its VM, is creating then a video of the reproduction`）
  - “no touch”协作方式（原文锚点：`I call this no touch`）
  - Orbit 为跨 SDLC 知识图谱、处于 beta（原文锚点：`currently in beta phase to GitLab itself, which is Orbit`）
  - 覆盖整个 SDLC 的知识图谱（原文锚点：`a knowledge graph across the whole SDLC`）
  - 知识图谱权限与终端用户对齐（原文锚点：`the knowledge graph has only the same information that you would be also be able to see as an end user`）
  - 相对 RAG 的定位讨论（原文锚点：`being positioned instead of RAG`）
  - 主持人转述：CDC 进 ClickHouse、解析 12 种语言（原文锚点：`via change data capture into ClickHouse`）
  - 给 agent 一张地图（原文锚点：`gives the agent a map into their hand`）
  - agent 取回 schema 并即时写查询（原文锚点：`access to retrieve the current schema and to write queries against it`）
  - 数据存于 ClickHouse（原文锚点：`All the data is stored in ClickHouse`）
  - 多 GB 巨石仓库的引用精度（原文锚点：`huge monoliths, which are multi-gigabytes`）
  - 5 万仓库的依赖秒级排查（原文锚点：`I know some customers who have 50,000 repositories`）
  - 依赖告警秒级定位确切版本（原文锚点：`it can literally give you an answer in seconds`）
  - 本地与远端知识图谱互联（原文锚点：`a local knowledge graph with a remote knowledge graph`）
  - “不会只用 GitLab”的开放姿态（原文锚点：`people just use GitLab and nothing else in the world`）
  - 外部 agent：Claude Code、Codex（原文锚点：`We also support Codex and others`）
  - 官方 GitLab MCP server 接近 GA（原文锚点：`an official GitLab MCP server, which is very close to going to GA`）
  - Orbit 以 MCP gateway 暴露（原文锚点：`we also expose Orbit as an MCP gateway`）
  - 默认多租户 AI 网关（原文锚点：`It's a multi-tenant gateway`）
  - 自管理可自装网关（原文锚点：`run and self-install an AI gateway`）
  - 支持无外网连接的气隙环境（原文锚点：`to support an air-gapped environment where there is no connection to the outside world`）
  - Dedicated 单租户网关 GA（原文锚点：`this is exactly what we have brought now to GA`）
  - 复合身份（原文锚点：`the composite identity`）
  - service account 附带发起用户（原文锚点：`we always attach which user has started`）
  - agent 工具白名单与审批（原文锚点：`this kind of agent is only allowed to use these tools`）
  - skill 数字签名（原文锚点：`these skills are available, and they are even digitally signed`）
  - 执行在服务端而非只发 prompt（原文锚点：`always built up and executed on the server`）
  - 服务端执行带来治理与审计轨迹（原文锚点：`we can ensure certain governance, compliance, auditing trails`）
  - 会话 trace 全部消息、工具调用与审批（原文锚点：`trace and track everything`）
  - 跨用户审计：agent 找 API key 的次数（原文锚点：`has tried to find an API key`）
  - 事后回放用户、时间与模型（原文锚点：`know this user on this time with this model`）
  - 气隙非刻意规划（原文锚点：`air-gapped originally came simply and happened to us`）
  - 大部分收入仍来自自管理（原文锚点：`our majority of revenue comes from self-managed`）
  - 发布打包、客户数月停留（原文锚点：`This release is put into a package`）
  - 客户版本老旧以年计（原文锚点：`I'm not talking about months. I'm talking about years`）
  - breaking changes 压到绝对最少（原文锚点：`reduce the amount of breaking changes to an absolute minimum`）
  - 只在每年一次的大版本做破坏性变更（原文锚点：`once a year a major version`）
  - 变更提前 6/12 个月公告（原文锚点：`announced six months or rather 12 months ahead of time`）
  - 按规模的参考架构（原文锚点：`a so-called reference architecture for different sizings`）
  - 机械硬盘导致 Git 服务缓慢（原文锚点：`not on SSDs, but rather on classic hard drives`）
  - 政府与高安全是经典气隙行业（原文锚点：`government and high security topics are the classic ones`）
  - 汽车专有源码不发给 AI 模型（原文锚点：`send that kind of source code to AI models`）
  - 同时运营气隙与非气隙实例（原文锚点：`an instance that is not air-gapped and an instance that is air-gapped`）
  - 主持人提到 Cursor 进入代码仓库空间（原文锚点：`coming into the code repository space`）
  - 变化速度前所未见（原文锚点：`the speed and amount of change in that space has never been higher`）
  - 与 Cursor 竞争又互补并合作（原文锚点：`competitive, but we are also very much complementary`）
  - 两三年前主要对手是 GitHub（原文锚点：`our main competitor is GitHub`）
  - 部门压平贴近 AI（原文锚点：`We flattened the organization to be much closer to each other`）
  - 状态报告全面自动化（原文锚点：`everything is currently completely automated in my department`）
  - 全新 CLI 与 agentic loop（原文锚点：`complete new CLI with a complete new agentic loop`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语；归档原文中的 [H:MM:SS] 标记未当作逐句可对位的时间戳使用，正文不引用推算时间。
- 无法独立验证的数字与案例（公司员工数、用户与安装规模、15,000 名工程师、50,000 个仓库、12 种语言、10 处引用等）仅作为节目中的观点或案例呈现；其中 CDC 进 ClickHouse 与“解析 12 种语言”出自主持人转述，Tim Zallmann 仅确认数据存于 ClickHouse。本期主持人为 Gregor Vand，嘉宾为 GitLab 工程副总裁 Tim Zallmann。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
