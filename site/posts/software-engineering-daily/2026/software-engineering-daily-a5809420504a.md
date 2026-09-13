---
item_id: software-engineering-daily-a5809420504a
title: 'FastMCP 的三个十年之问：装饰器、code mode 与 MCP 的企业重心'
date: '2026-09-13'
published_at: '2026-04-07'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/fastmcp-with-adam-azzam-and-jeremiah-lowin/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1920-FastMCP.txt'
summary: 'FastMCP 两位维护者谈 MCP 生态：一个装饰器起家、3.0 重构让变革性功能只需几百行、code mode 上下文优化，以及"绝大多数 MCP 用例发生在企业内部"。'
tags: [MCP, AI Agent, 开发者工具]
---

# FastMCP 的三个十年之问：装饰器、code mode 与 MCP 的企业重心

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-04-07 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3806 字 · 阅读约 10 分钟
>
> 标签：[MCP](/tags/MCP/) [AI Agent](/tags/AI%20Agent/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/fastmcp-with-adam-azzam-and-jeremiah-lowin/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1920-FastMCP.txt)

## 速读

Prefect 创始人 Jeremiah Lowin 与产品 VP Adam Azzam 做客 SED，讲 FastMCP——MCP 的高层 Python 框架——从周末副项目到每天 200 万次下载的历程。这期对做 MCP 服务器、评估 MCP vs CLI 之争的人是必听材料：它把争论从技术偏好拉回商业现实——"绝大多数 MCP 用例发生在公司内部供自家员工使用"，企业内部有数百个被重度使用的 MCP 服务器，公开世界只有 20-30 个流行的（数字为受访者约数）。

最有技术含量的部分是 code mode：把"LLM 逐个调用工具"变为"LLM 写一段程序、在沙箱里一次执行"，FastMCP 3.1 用一行代码为 300 工具的服务器开启此模式。文中数字多处为受访者约数，已标注。

## 主题正文

### 起源：周末写出的初版与"管家"身份

Jeremiah 约 20 年买方金融背景（"软件预算无限、人头预算为零"），曾属原始 Airflow 团队，2018 年创立 Prefect。MCP 公布约一年半前，他判断 MCP 是"桥接程序化工作流与 agentic 工作流"一直缺的一环，随即写了 FastMCP 第一版；官方 SDK 是低层框架（类比 Starlette），他们想要 FastAPI 式的高层体验——约定下周一起做，Jeremiah 周末独自写出初版。Adam 是数学 PhD（偏微分方程）转向数据科学，2023 年入职 Prefect。（`00:01:35–00:07:09`）

一个重要澄清（纠正主持人的表述）：FastMCP 不是公司，只是项目与生态；Prefect 是盈利软件公司，两人以"管家/维护者"身份、无外部融资压力地维护它。1.0 的核心就是一个装饰器——把"这个函数属于这个 MCP server"变成 Python 惯用法；FastMCP 名字是对 FastAPI 的致敬。Anthropic 的 MCP 发明者 David Soria Parra 亲自致电请求把 FastMCP 纳入官方 SDK，代码被复制进官方 SDK 并保留至今；官方 SDK 中的同名对象"即将改名"以消除两个 FastMCP 的混淆。（`00:07:27–00:12:07`）

### 增长时间线与 3.0 重构的"巨大错误"

冷启动期：从 11 月底到次年 3 月"没人关心"，关注者以"几十"计。转折是 2025 年春协议获巨头支持（Jeremiah 说 OpenAI and Google，Adam 说 OpenAI and Microsoft——两人表述不一致，已如实保留）；此后 issue 淹没、下载量涨到当时的约 100 倍；秋季 Databricks、Snowflake 的 MCP 服务器与 MLflow 采用标志从爱好者转入主流企业采用。3.0（约一个月前发布）的动机是 Jeremiah 自称 "I've made a huge mistake"——2.x 所有功能都是增量拼接、成了彼此独立的代码路径；企业要的一千件事本身不难，缺的是中央设计哲学。重构收益的量化案例（code mode）：在 2.X 上与 Claude 结对得到约 +4000/−20000 行的改动；换到 3.X 重做只需几百行（两人当场核对的数字略有出入，结论一致）。（`00:08:11–00:21:41`）

### 三大支柱与"大多数 MCP 客户端很糟糕"

FastMCP 3 分 servers/clients/apps 三支柱。Server 是"肉和土豆"：认证、授权、版本化、模块化、传输等，框架给"讲道理的默认值"；想完全从零自建就该用官方 SDK。Client 不是 LLM 客户端，职责是连接服务器、盘点能力；客户端质量参差——多数只支持 tools，约一半支持 resources/prompts，"your mileage may vary"。Jeremiah 的强断言："大多数 MCP 客户端很糟糕"，只实现 tool calling，且"很可能要负全责于 MCP 未能发挥潜力的正当指控"；他点名好客户端：Goose、VS Code、Claude Code、MCPJam。一个反例：Claude Web 把所有服务器全部工具塞进上下文窗口可能"惩罚或 lobotomize"LLM；Claude Code 则动态搜索工具目录（Adam 猜是 BM25），塞 10 万个工具仍只高亮相关者。（`00:21:41–00:31:48`）

### Apps 与 Prefab：MCP 的生成式 UI

Apps 的出发点：MCP 服务器返回 100 家餐厅的 markdown 长列表不是好的呈现。Jeremiah 的场景判断：SQL 查询返回 10,000 行时，塞进上下文窗口或让 LLM 写摘要都不对；预期图表、数据表、表单将占 MCP apps 用例的 80%-90%。Prefab（录制时首次公开谈论）是一个 JSON 协议、可编译为"受限但功能完备"的 React 应用——LLM 可写 JSON、人可用 Python DSL；目标是解决 app 与 MCP 服务器变更不同步的紧耦合问题。（`00:24:34–00:36:57`）

### Code mode：从客户端关切到服务器侧能力

默认做法的两个问题：把所有工具给 LLM 导致上下文膨胀；LLM 逐个串行调用工具、每步回传全部对话，token 二次方增长。演进脉络：Block 几个月前首创"先搜索目录再执行"模式；Cloudflare 推进"让 LLM 直接用工具集写程序"（TypeScript），把数百次工具调用变为一次程序执行——但当时是客户端侧关切、难落地。转折是近几个月"远程沙箱/代码沙箱"复兴，使服务器侧 code mode 可行。FastMCP 3.1（录制前夜发布）：给 300 工具的 server 一行代码开启 code mode，对外只暴露"搜索目录 + 执行客户端提交的代码"两个工具；沙箱运行时可自带（Modal、Daytona、Cloudflare 等），开箱默认是 Pydantic 的 Monty 安全本地沙箱；沙箱线程只能访问该服务器工具、无其他互联网连接。已知局限：多个 code mode 服务器同时挂载会出现命名空间冲突，"肯定会演变"。（`00:36:57–00:47:56`）

### MCP vs CLI 之争与企业重心

这期最有趣的争论。Jeremiah 部署过三个迭代版本的 OpenClaw bot（家用起步、逐步加大信任）；OpenClaw 不原生带 MCP 集成。他的核心论证：无论技术/传输是什么，都需要一个协议约定"写软件的人与消费软件的 agent 之间的契约"——选 CLI 就得写自然语言帮助文档、命令发现、参数发现，"不知不觉你就发明了某种协议"，今天那个协议恰好叫 MCP。实例很生动：他的 OpenClaw"每小时自杀一次"——装音频转录软件时反复幻觉出不存在的 CLI 参数、写进配置、重启网关、非法调用而死；正是"没有工具广播确切可用能力与调用方式"的痛。他让步：MCP 服务器有别的包袱（不易安装、需要托管），"我也用 CLI"。

Adam 的 token 经济反驳：CLI --help 渲染全部选项与渲染工具列表的 token 相当；LLM 用 CLI 会传错参数类型、422 错误也进上下文，而 MCP 把 JSON schema 类型提示"提前付税"；"凭经验看，这类 token 消耗论证不太有说服力"。Adam 的治理论证：内部服务器里有的工具会改/删数据、有的只读，应按人呈现不同界面（"多面 API"），这用经典 REST 难以表达；MCP 还天然承接长任务与进度通知——"要么叫它 MCP，要么你自己在发明协议"。HN 热帖（主持人引述）立场相反："先做好 API，再做好 CLI，agents 自己会搞定。"（`00:47:56–01:01:46`）

Jeremiah 的"强硬观点"是全期的落点：绝大多数 MCP 用例发生在公司内部供自家员工使用；企业内部部署就"绝对不应做成 CLI"，应做紧契约的 MCP server——同时控制服务器与客户端；这占其每天所见用例的 80% 以上。市场感知数据：FastMCP 日下载约 200 万次；公开世界只有约 20-30 个流行的 MCP 服务器（粗估）、长尾 0-1 用户；而合作企业内部有数百个被重度使用的 MCP 服务器、服务约 5000 名员工。社区方面约 200 人贡献过代码。（`00:53:20–01:03:50`）

## 来源与定位

- 原始节目：[FastMCP with Adam Azzam and Jeremiah Lowin](https://softwareengineeringdaily.com/podcasts/fastmcp-with-adam-azzam-and-jeremiah-lowin/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 起源、装饰器与"管家"身份（00:01:35–00:12:07）
  - 增长时间线与 3.0 重构的"巨大错误"（00:14:55–00:21:41）
  - 三大支柱与客户端质量参差（00:21:41–00:31:48）
  - Apps 与 Prefab 生成式 UI（00:24:34–00:36:57）
  - code mode 的演进与 FastMCP 3.1 实现（00:36:57–00:47:56）
  - MCP vs CLI 之争与 OpenClaw 每小时自杀实例（00:47:56–01:01:46）
  - 企业内部用例占 80% 以上的强硬观点（00:53:20–00:55:30）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 下载数、用例占比、效率倍数等数字多为受访者约数或经验估计，未独立验证；两位受访者对巨头支持方名单与重构行数的表述不一致处已如实保留。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
