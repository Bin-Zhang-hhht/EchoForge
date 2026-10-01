---
item_id: software-engineering-daily-8f0699d6ce4b
title: 'Vercel EVE：从单机会话到千路并发的云原生 Agent 框架'
date: '2026-10-01'
published_at: '2026-09-17'
transcribed_at: '2026-10-01'
model: 'GLM-5.3-Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/scaling-agent-workloads-at-vercel/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/09/SED1967-Shar-Dara-Andrew-Barba.txt'
summary: 'Vercel EVE 是一个开源云原生 Agent 框架：Agent 用目录和 Markdown 声明、编译成基础设施即代码，会话按 Workflow 分区、每步换新函数绕开 serverless 超时；本期还覆盖多人权限、评测套件、记忆槽位与「建公司即建 Agent」的愿景。'
tags: [AI Agent, 云服务, 开源]
---

# Vercel EVE：从单机会话到千路并发的云原生 Agent 框架

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-09-17 · 逐字稿获取：2026-10-01 · 笔记整理：2026-10-01
>
> 全文共 7594 字 · 阅读约 19 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [云服务](/tags/%E4%BA%91%E6%9C%8D%E5%8A%A1/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/scaling-agent-workloads-at-vercel/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/09/SED1967-Shar-Dara-Andrew-Barba.txt)

## 速读

Vercel EVE 是一个开源云原生 Agent 框架：Agent 用目录和 Markdown 声明、编译成基础设施即代码，会话按 Workflow 分区、每步换新函数绕开 serverless 超时；本期还覆盖多人权限、评测套件、记忆槽位与「建公司即建 Agent」的愿景。EVE 产品负责人 Shar Dara 与 Vercel Member of Technical Staff Andrew Barba 接受 Kevin Ball 采访，两人此前共同领导 Vercel 计费团队，今年 2 月起专职做 EVE（`00:01:49–00:03:11`）。

最值得带走的三点：其一，目录即 Agent——最小的 EVE agent 可以只是一个 instructions.md，框架把语法与槽位编译成一份基础设施即代码的 manifest，加了 skills 就配 sandbox、定了 schedules 就接事件设施，思路直接来自 Vercel 内部数据 agent D0 的手搓沉淀（`00:05:52–00:09:02`）。其二，规模化的底盘——一个 workflow 对应一个会话、会话之间完全分区，serverless 函数 15 分钟超时的限制被「每次调用工具就迁去新函数继续 workflow」化解，agent 实际上可以无限期运行；Vercel 内部已有数百个 agent 跑在 EVE 上（`00:22:54–00:34:52`）。其三，记忆与自我进化正在路上——memory 槽位按全局、单用户、渠道加用户分抽屉，provider 抽象让 recall/save 可插拔，自我进化被建模为一个 coding sub-agent 对自己的代码库开 PR（`00:35:25–00:43:20`）。

## 主题正文

### 从 D0 到 EVE：目录即 Agent，配置编译成基础设施

Barba 在 Vercel 待了三年半，2020 年曾是最早一批企业客户之一，先做了一年半 CDN、分布式系统、边缘网络与安全，又做了一年计费；Dara 在计费领域干了十年、加入 Vercel 一年半，2025 年大部分时间两人共同领导计费团队。今年 2 月，「把 agent 部署到 Vercel 需要什么」成了手里的命题，两人做出了 EVE（`00:01:49–00:03:11`）。

「云原生」是 Barba 刻意的定语：大家熟悉的 Codex、Claude Code 这类 harness 都跑在自己机器上、单人单会话，而 EVE 面向多人云环境。他爱举的思想实验是让一千个人同时发来 prompt——EVE 在 Vercel 或其他托管平台上水平扩容、快速并行拉起 harness、会话彼此隔离、状态持久，并带恢复、重试与错误处理。目标场景是驱动业务：万人企业的内部 agent，或者 B2C 公司把 agent 当主要产品（`00:03:22–00:05:31`）。

EVE 的前身是 Vercel 内部的数据 agent D0：全公司都在用，团队为把它跑上 Vercel 手搓了大量系统，包装 serverless 函数、sandbox、workflow 等自家产品。他们注意到 D0 的功能大量来自 Markdown、YAML（逐字稿写作 EAML）等规格文件——作为数据 agent，它的语义层就是在「教育」agent 各家缩略词指什么。由此 EVE 起步时立场非常激进：完全没有代码，纯粹用英文 Markdown 文本文件表达 agent（`00:05:52–00:07:44`）。

今天的 EVE 仍然「字面意义上是一个目录」：最简单的 agent 可以只有一个 instructions.md。EVE 的语法和槽位会被编译成一份 manifest——也就是主持人所说的基础设施即代码——按声明按需供给：加了 skills 就配 sandbox，定义了 schedules 就接事件设施。Barba 称之为「盒装 ChatGPT」：放进 instructions.md，就得到一个云端托管的前沿模型（`00:08:17–00:09:02`）。

### 原语、Evals 与写给编码 Agent 的文档

EVE 的核心原语分两层。第一层是「大脑与操作」：instructions 是身份；skills 是渐进式披露机制——只在提示里给出「何时该用」的线索，模型需要时再自行拉入上下文，Barba 说 D0 的功能九成是 skills；tools 跑确定性代码、接确定性数据（PostgreSQL、开放 API）；connections 是 tools 的特化，MCP 链接是一等公民，丢进去自动暴露工具。第二层是调用：channels 是所有入口，默认是 HTTP 路由（自家 TUI 与 Next.js 应用都用它），Slack、Teams、GitHub 则提供第一方事件接入。再往外是 sub-agents——最简单的形态是上下文管理，把不想塞爆父 agent 的大任务交出去独立处理再汇报；Vercel 内部甚至整支团队拥有一个 sub-agent。Evals 同样是一等公民（`00:09:19–00:12:40`）。

Evals 分两类：一类偏确定性，比如天气 agent 收到提问时必须调用了 get weather 工具；另一类是 LLM as judge，对回答打分，D0 上甚至能给生成的 SQL 评分、核对查的表对不对。eval 函数是 agent 的完整编程接口，可以起 turn、触发 human in the loop。最有说服力的一点：EVE 仓库自己的测试套件就是一整套 Evals，用评测框架测框架本身——Barba 说这是他们敢一天发布多个新版本的信心来源（`00:13:05–00:14:44`）。

主持人追问「把 prompting 变成优化函数」的方向——用 Evals 定义应然、再迭代 agent 使其成真。Barba 说自己没从这个角度想过，但有个现成现象：用编码 agent 构建 EVE agent 时，它会真的边迭代边写、边跑 Evals，因为包内文档提示了「EVE 用 evals 测试」；他没见过先写 eval 再写实现的用法，但认为可以逼近（`00:14:57–00:16:27`）。

文档本身也在为编码 agent 优化。Next.js 的教训是模型训练数据停留在旧版本，而 EVE 对这些模型来说根本不存在，所以包里必须自带 LLM 友好文档：scaffold 附 agents.md 指向文档，并内置 changelog——agent 只需读自己当前版本到最新版本之间的 diff。对一个每周都在破坏性变更的 pre-1.0 框架，changelog 是用户升级不翻车的主要手段（`00:16:43–00:18:23`）。

### 多人世界里的身份与权限

EVE 从第一天就是多人设计。渠道层先回答「你是谁」：Slack 渠道的身份是工作区 ID 加用户 ID；代码里处处可得的 context object 会告诉你本轮用户是谁、发起这一轮的又是谁——两者可以是不同人，不同人可以在不同时间接续同一会话。写惯了后端 REST API 的人可以照旧做鉴权：身份在渠道层解析，权限判断还是自己的代码（`00:19:08–00:22:35`）。

更进一步是 tool approvals：把某工具标成 always require approval，就触发 human in the loop 消息，且按调用渠道渲染——从 Slack 进来是一种样子，从 SMS 进来是另一种。提问者与审批者可以不是同一个人，接不接受由开发者自己决定。Barba 强调这是 code first 框架的立场：框架不预设所有用法，让你写代码得到想要的体验（`00:19:08–00:22:35`）。

最难的一层是「只看你该看的」。D0 能访问 Vercel 整个数据湖，谁在提问决定了哪些数据可看——Barba 举例：同事 Guillermo 提问时能碰到的内容，换他来问就不该看到。他们为此做了一个动态解析 API（逐字稿写作 defined dynamic），按当前调用者解析出不同的工具与连接集合，甚至可以对我隐藏某个工具而对别人可见。他称这是高级用例但文档完善，agent 对这种模式学得很好（`00:19:08–00:22:35`）。

### 规模化的底盘：会话分区与「每步换函数」

采用上，Dara 给出口径：EVE 最初瞄准企业——需求大多来自那里，基建现成，顺便解决自己的问题；上线后 Vercel 内部所有内部 agent 都跑在 EVE 上，数百个；很快又有数千外部用户采用，从企业业务 agent 到周末给 iMessage 搭多人 agent 的爱好者都有。职能分布从工程起步，逐渐扩散到 go-to-market、营销（内容与社媒自动化）、计费与产品文档问答，但工程仍占大头，随自进化等能力成熟会更平均（`00:22:54–00:25:11`）。

他总结出三种采用形态：最常见的是经 Slack 渠道对话的 agent——Vercel 自己是 Slack 公司，D0 即如此；其次是后台 agent，定时跑报表发进 Slack 或邮件；第三种是应用——前端是一个 web app，实际由 agent 驱动并内嵌聊天界面，go-to-market 团队是重度用户（`00:25:55–00:26:52`）。

与 Next.js 的集成走约定式路线：agent 目录与 Next.js 应用并置有一等支持；也可以完全独立部署、通过 HTTP 连接——EVE channel 协议负责发消息、取消等操作，最终交还一条 durable stream 给你渲染任意 UI。Barba 的定位很干脆：EVE 是后端框架，不是前端框架（`00:27:17–00:28:22`）。社区已经出现「agentic 原生应用」：一个开源 CRM，录入姓名与邮箱后由后台 agent 研究线索、补全一切；一个 AI 音乐 maker，用户定 tempo，agent 与你在站点上协作完成曲子（`00:28:23–00:29:05`）。

规模的答案建在 Vercel Workflow（他称「我们的 temporal 版本」）上：早期模型是单个 workflow 对应单个 EVE 会话，如今实际是两个 workflow，但可以当作一个理解；分区方式是会话之间完全隔离，要共享数据得自带存储并参照指南。一千个会话和一个会话对你应当没有区别——这是云该干的活（`00:33:20–00:34:26`）。serverless 函数历史上 15 分钟超时，agent 显然会跑更久；EVE 的办法是每次调用工具就把执行迁到新函数继续 workflow，如今每个步骤都换一次函数。只要 workflow 足够快，这一切无感，agent 实际上可以无限期运行（`00:34:32–00:34:52`）。

应用形态还有个值得一记的细节：发消息时可以指定 output schema，让 agent 按 UI 需要的形状 agentically 生成数据；底层建在 AI SDK 之上，框架产出一个名为 submit result 的工具做校验，缺属性就回灌提示让模型重来——不保证成功，但在前沿模型上表现相当好（`00:30:12–00:32:03`）。主持人指出 tool call 是个同步块、schema 结果不会流式分片返回，UI 需要等待态；Barba 确认，但中间的推理流始终可见（`00:32:03–00:32:48`）。

### 记忆、自我进化与「建公司即建 Agent」

记忆与自我进化是 Barba 当前最大的工作项，全部代码以 open PR 形式公开可查。出发点回到个人用例：企业场景反而不太需要「越用越懂你」。与 Hermes 这类能原地改自己代码并重启的 agent 不同，EVE 把自我进化建在 git 上：定义一个 coding sub-agent，部署时自带代码库沙箱与相应提示，知道何时该调它改东西，目标是对框架自己开 PR——想要多强的监督由你配置，让它自动合并或全部人审都行（`00:35:25–00:38:14`）。

memory 将是一等 slot（slots 即 skills、tools、sandbox、channels 这些顶层目录）：内部按作用域分「抽屉」——全局共享的工作区记忆、单用户记忆、渠道加用户记忆——并且把工具绑定到对应作用域，agent 无从猜错 user ID。主持人的复述是：权限这类事要确定性地沉到 agent 行为之下；Barba 补充，他们正是在见过「抓错人记忆」的问题后才确定记忆必须一等公民化，由框架提供护栏和干净 API（`00:38:26–00:40:02`）。

实现上 EVE 不预设记忆工具的形态：框架确定性地调用三个函数——recall、save 与一个 tools 函数，其余交给 provider。随框架发布的 file provider 最简：recall 把整个文件作为上下文返回，save 是空实现，提供 add memory 与 forget memory 两个工具，改动后把文件重写回 blob 存储——类比 Hermes 的 user.md。主持人确认：文件内容会出现在每一轮 agent prompt 里（`00:40:12–00:41:34`）。

provider 抽象也为外部记忆服务留了位置：比如 Supermemory（逐字稿称 super memory）这类服务不暴露工具，而是在确定性的 save 时机拿整段消息历史跑一个 agentic 过程决定存什么，recall 则基于入站消息做 agentic 检索——与 file 版完全不同（`00:41:34–00:42:32`）。recall 的调用时机除每轮 turn start 外还包括 compaction 之后，因为框架无法保证压缩保留你的记忆，provider 可以据此决定要不要重新注入（`00:42:42–00:43:10`）。注入方式上，默认以 user 角色追加消息、避免打爆 prompt cache，也可以覆盖成 system 角色，但那样每次增删记忆都会破坏缓存（`00:43:20–00:43:42`）。

开源运营有个现实难题：EVE 的测试套件要打真模型、真部署项目到 Vercel、消耗一堆 secrets，外部贡献者的 PR 因此没法直接跑套件——他们得把改动小心拉进沙箱排查恶意行为，再以 co-author 名义用自己的账号重新提交才能测试。Barba 坦言这很扫兴，正在改进流程；内部则用 EVE agent 每天分析外部 PR、挑出值得收入的。团队规模：3 月到 7 月中全职工只有两人，近期新进四人，现在约六名工程全职（`00:44:09–00:45:21`）。

愿景上两人侧重不同。Barba 重申早期原则——押注模型越来越聪明：见过的多数 agent 框架在纵向扩展，代码越堆越多、确定性越来越强、最后像 workflow API；EVE 选横向，押注模型自己做出正确决策，文件夹结构就是给模型更多材料（`00:45:49–00:46:44`）。Dara 的说法更进一步：建公司就是建 agent——EVE 比公司注册证书更根本，agent 先于网站、域名乃至公司注册存在；你从 agent 开始，它渐进为你搭好包含完整软件开发生命周期的软件工厂，你的工作是微调这座工厂，EVE 则要成为公司的大脑（`00:46:46–00:47:25`）。

主持人顺势问 Vercel 之外怎么托管。Barba 说这很重要：已有客户在自己硬件的 Kubernetes 上跑 EVE，靠的是 workflow 里的 world 概念——他们的测试套件就在 PostgreSQL world、local world 等不同 world 上验证；只要能为你的基础设施定义一个 world（大量其他 provider 的 world 已存在）就能自托管，但让这个体验变好还有大量工作要做。记忆、自进化、动态调度这类能力则依赖 adapter contracts：动态调度在 Vercel 上是一等公民，别处要自带，关键是这些适配 API 在早期就设计好，而不是等在 Vercel 上跑通后再补（`00:47:44–00:48:49`）。

## 来源与定位

- 原始节目：[Scaling Agent Workloads at Vercel](https://softwareengineeringdaily.com/podcasts/scaling-agent-workloads-at-vercel/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 嘉宾背景与 EVE 立项（00:01:49–00:03:11）
  - 云原生定位与千人并发思想实验（00:03:22–00:05:31）
  - D0 起源、语义层规格文件与「无代码、纯英文」立场（00:05:52–00:07:44）
  - 目录即 Agent、manifest 编译为基础设施即代码、盒装 ChatGPT（00:08:17–00:09:02）
  - 核心原语：instructions/skills/tools/connections/channels/sub-agents/Evals（00:09:19–00:12:40）
  - 两类 Evals、测试套件即 Evals、一天多次发布（00:13:05–00:14:44）
  - Evals 作 guardrails 与编码 Agent 边建边评（00:14:57–00:16:27）
  - LLM 友好文档：agents.md 与包内 changelog（00:16:43–00:18:23）
  - 渠道身份、context object、tool approvals 与按调用者解析工具集（00:19:08–00:22:35）
  - 内部数百 agent、数千用户与采用人群扩散（00:22:54–00:25:11）
  - 三种采用形态（00:25:55–00:26:52）
  - Next.js 集成、HTTP channel 与后端框架定位（00:27:17–00:28:22）
  - agentic 原生应用案例（00:28:23–00:29:05）
  - output schema、submit result 校验与 tool call 同步块（00:30:12–00:32:48）
  - Workflow 会话分区（00:33:20–00:34:26）
  - 每步换新函数与无限期运行（00:34:32–00:34:52）
  - 记忆 open PRs、git 式自我进化与监督配置（00:35:25–00:38:14）
  - memory 槽位、作用域抽屉与确定性护栏（00:38:26–00:40:02）
  - provider 三函数与 file provider（00:40:12–00:41:34）
  - Supermemory 类 provider（00:41:34–00:42:32）
  - compaction 后 recall 与 role user 注入（00:42:42–00:43:42）
  - 外部贡献难题与团队规模（00:44:09–00:45:21）
  - 押注模型变聪明（00:45:49–00:46:44）
  - 建公司即建 Agent（00:46:46–00:47:25）
  - 自托管 world 与 adapter contracts（00:47:44–00:48:49）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3-Flash
- AI 编辑整理，请以原始节目为准。
