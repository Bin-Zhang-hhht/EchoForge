---
item_id: talk-python-6626e25c5e80
title: '2026 年 Python 工具栈盘点：AI 重开每一道选择题'
date: '2026-11-01'
published_at: '2026-10-17'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: https://talkpython.fm/episodes/show/566/state-of-the-art-in-python-2026
source_name: Talk Python To Me
input_type: official_transcript
transcript_url: https://talkpython.fm/episodes/show/566/state-of-the-art-in-python-2026.vtt
summary: '这期圆桌盘点 2026 年的 Python 工具栈：AI 重开了编辑器、终端、打包、类型检查、数据库、文档与托管几乎每一道选择题——四位嘉宾聊在 Slack 里派活写代码、uv 一统打包与装 Python、ty 极速类型检查与嵌入式数据库抬头，也谈到 AI 把服务器价格推高到近四倍。'
tags: [Python, 开发者工具, 编程语言]
---

# 2026 年 Python 工具栈盘点：AI 重开每一道选择题

> 节目：[Talk Python To Me](/podcasts/talk-python/)
>
> 节目发布：2026-10-17 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 10610 字 · 阅读约 27 分钟
>
> 标签：[Python](/tags/Python/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [编程语言](/tags/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80/)
>
> 🎧 [收听原节目](https://talkpython.fm/episodes/show/566/state-of-the-art-in-python-2026) · 📄 [查看官方逐字稿](https://talkpython.fm/episodes/show/566/state-of-the-art-in-python-2026.vtt)

## 速读

这期圆桌盘点 2026 年的 Python 工具栈：AI 重开了编辑器、终端、打包、类型检查、数据库、文档与托管几乎每一道选择题——四位嘉宾聊在 Slack 里派活写代码、uv 一统打包与装 Python、ty 极速类型检查与嵌入式数据库抬头，也谈到 AI 把服务器价格推高到近四倍。

嘉宾是 Six Feet Up 联合创始人兼 CTO Calvin Hendryx-Parker（Python 1.5.2 时代入坑）、Hibu 的 DevOps 工程师 Pat Decker、做了 15 年 Python 培训的 Reuven Lerner，以及在 LangChain 负责开源产品、此前维护 Pydantic core 的 Sydney Runkle。主持人 Michael Kennedy 把题眼定为：如果今天重来，你还会选现在这套 Python 工具吗——工具栈曾长期稳定，AI 重新打开了几乎每一道选择，有的变快，有的被整个换掉（`00:00:00–00:00:20`）；他还预告其中一位嘉宾"几乎不再打开编辑器"（`00:00:34–00:00:37`）。节目录于 2026 年 10 月 1 日（`00:00:40–00:00:45`），适合想逐项对照自家工具栈的 Python 开发者与团队。

## 主题正文

### 编辑器：从 VS Code、PyCharm 二选一到「在 Slack 里派活」

Michael 回忆，做播客早期他会在节目结尾问嘉宾"你用什么编辑器"，答案五花八门；最近六七年只剩 VS Code 和 PyCharm 轮流出现，他干脆不再问——但 AI 把这件事重新搅动了（`00:10:58–00:11:33`）。

Sydney 的路径是从 VS Code 转到 Cursor——因为后者更早把 agent 卷进 IDE——而如今她大部分编码发生在 Slack：团队本来就在 Slack 里讨论想法和问题，她直接在 Slack 里 @ 编码 agent 派活，再去 GitHub 看结果、必要时拉到本地细改；她估计自己约 90% 的工作已在 Slack 里完成（`00:11:44–00:12:44`）。Reuven 的轨迹是 Emacs、少量 PyCharm、大量 Jupyter，最近一年则大部分时间在 Claude Code 里——他本以为这已经"够时髦"，结果被 Sydney 抢尽风头（`00:13:17–00:13:37`）。

Calvin 电脑上没装 VS Code 或任何变体，编码全在 Pi 和 Claude Code 里；看文件用他要的"替代 cat"——bat，需要更重的体验才退回 PyCharm；而多数时间他其实花在读 Markdown 的规格与计划上，看完才让 agent 去实现（`00:14:06–00:14:55`）。Michael 是终身的 Vim/NeoVim 用户，还讲过一个 PyCon 事故：上台做 lightning talk 时 PyCharm 的 VI 模式被关掉，他"吓坏了"（`00:14:55–00:15:31`）。

Pat 的编辑器史最长：大学在 Iowa State 用穿孔卡片上 Pascal 课，大型机时代用 IBM 的编辑器，后来转向模仿大型机 X-Edit 的 K-Edit 并用到今天；现在多数时间用 VS Code 远连 AWS 实例，要 AI 协助时用 AWS 的 Kiro，最后的运行时小改动用 Vim，偶尔掉回 Nano（`00:15:31–00:16:41`）。

### 终端：2026 年还在爆发的新品类

Pat 在 Windows 上用 CMD 和 WSL，shell 就是 Bash；运维场景里他用 Royal TS 管理成组的服务器连接（SSH、RDP、HTTP、SFTP、VNC 都覆盖，可存凭据，Mac/Windows 双端），再用 TMUX 保证长时间测试在凭据过期、连接断掉后继续跑（`00:17:55–00:18:54`）。

Calvin 用 GPU 加速的跨平台终端 Kitty，称其滚动文本"比任何终端都快"；他曾因苹果坚持在键盘上塞 Touch Bar 而全职用了三年 Linux 桌面，回到 Mac 后把 Kitty 留了下来。会话管理上，他从 TMUX 换到一款逐字稿记作 herdr 的工具，称它是"AI 原生多路复用器"，管窗口、远程会话也管 AI agent，并搭配 Mosh 加 VPN，让自己随时连上散布在各服务器上的 agent（`00:18:54–00:20:16`）。

Reuven 最近常用 Marimo 做笔记式开发，还怀念 Jupyter 里叹号直跑 shell 命令的顺手；他用了很多年 iTerm2 后意识到自己只用到一成功能，几个月前换到 Ghostty，非常满意。他把 Claude Code 切到 TUI 全屏模式，解决了此前的滚动回溯和闪烁问题，还顺带获得全程可搜索的历史和终端右侧的 diff 窗口（`00:21:20–00:22:28`）。Michael 用了很久 Warp，但不喜欢它转向 agent 产品的路数；朋友 Mark 推荐他 CMUX：多窗口分屏、workspace 记住布局、重启后恢复 SSH 连接，还有 iPhone 版（`00:22:28–00:23:25`）。

Reuven 感叹：2026 年居然还有人在开发新终端，这本该是个早就"功能完结"的品类——全是 AI 在驱动这波创造，"还得用 Rust 重写一遍"（`00:23:25–00:23:44`）。Calvin 收束成一个结构性观察：终端 UI 和随之涌现的高质量 CLI 正在成为 LLM 与 agent 的富接口——他的邮件客户端 Spark 现在自带 CLI，自己和 agent 都能用，比 MCP 更贴合他本地的工作流（`00:24:14–00:24:55`）。

### 打包与装 Python：uv 拿下全票

Michael 顺势安利 Talk Python 自家的 CLI：`uv tool install` 一条命令装好、无需认证，可以问"Sydney 第一次上节目聊了什么"这类问题；他更推崇 `uvx`——直接跑包，别的什么都不用想（`00:24:55–00:25:23`）。作为对照，Reuven 回忆起没有 pip 的年代：Python 很长时间没有包管理器，标准库之所以塞得那么满，部分原因就在这里；当年他在入门课上花大量时间帮学生装 pip，"简直是疯狂"（`00:25:32–00:25:50`）。

Calvin 的全票理由是 uv 收编了他既有的全部习惯：用版本管理器管 Python 版本、用 pip 加锁文件保证可复现、用 pipx 装工具——uv 把这套偏好原样打包，他就 all in 了；他还不忘提起当年 Slack 里讽刺 Poetry 的俳句机器人，补一句公道话："如果你全押 Poetry，Poetry 是好工具"（`00:26:12–00:27:38`）。Sydney 则说 uv 给包管理带来的提速"可以比肩 AI agent 给编码带来的改变"，并自称是 Astral 工具链的粉丝——Astral 已并入 OpenAI，这些工具也正在为 agent 原生使用做适配（`00:27:38–00:28:35`）。Michael 补充：他几个月前刚请 Charlie Marsh 聊过并入 OpenAI 后的近况，实际使用一切照旧（`00:29:51–00:30:16`）。

Reuven 的版本最直白：多年来 Python 会议动辄两三场演讲都在解释打包之乱，讲者感叹"要是有人能解决就好"，核心开发者则说"别提建议，除非你来解决"；uv 一来就把版本管理、打包、上传 PyPI、安装 Python 版本全解决了，而且极快。Astral 被 OpenAI 收购一度让一些人担心，但开源接受企业赞助多年，Astral 目前证明自己是可靠的管家（`00:30:16–00:31:30`）。

Michael 点出真正的杀手锏：uv 活在 Python 之外，可以成为进入 Python 的入口——机器上根本不用预装 Python，这一点此前没有别的打包工具做到（`00:32:08–00:32:40`）。Pat 印证：几年前装 Python、装依赖的痛苦让他认真考虑"全部塞进容器"，uv 让他回到了一行命令的便利（`00:32:40–00:32:58`）。Reuven 补刀：人人都恨过的 venv activate/deactivate 被 uv 直接藏起来，"像魔法"；这一团乱惨到连 XKCD 都画过"我的笔记本成了超级污染场地"的漫画（`00:32:58–00:33:32`）。

Sydney 给出 AI 视角的解释：模型擅长写代码，一是因为训练语料里的代码可验证——能跑还是不能跑、测试过没过；二是它们又在代码语法上被后训练过。uv 在 AI 爆发前已经是领先的包管理器，模型因此能用它有效控制代码运行的环境；通用 agent 也把写代码当作达成其他目标的手段——"OpenAI 收购 Astral 是有原因的"（`00:33:32–00:34:55`）。

还有一个时间胶囊式的细节：录制当天早上，嘉宾们还在猜 Python 3.15 发了没有，有人当场查了下载页——"还是 3.14.8"（`00:25:55–00:26:12`）；而 `uv python install 3.15` 走 Python Builds Channel 本周已能装到 RC——Calvin 在 Python Bytes 演示里刚用过，Michael 更是几个月前就在"准备好 3.15"视频系列里让 uv 代劳安装，一次成功（`00:31:36–00:32:07`）。

### Web 框架：语料厚度成了新的选型变量

Sebastian Ramirez 本该到场而缺席，Michael 提议从他的 FastAPI 聊起（`00:37:57–00:38:06`）。Calvin 刚在 DjangoCon 上和 Frank Wiles 同台对比 Django（配 Django Ninja）与 FastAPI：FastAPI 确实仍更快，但差距不再悬殊；他们的实践是两者都用、按任务挑——可能长成大项目的东西从 Django 起步，要快速交付高质量 API 的场景用 FastAPI（`00:38:06–00:38:41`）。Michael 补充他对 FastAPI 的理解：卖点不在性能，而在"把事情做对"的开发速度——Pydantic、OpenAPI、校验一条龙；想要这类体验又想留在 Django，Django Ninja 只需换一个 import，代码看起来几乎一样（`00:39:39–00:40:03`）。节目里还有人介绍了 Sebastian 的另一个仓库：为开源包批量生成技能文件，让 agent 写 FastAPI 时代码自带最佳实践（`00:38:41–00:39:29`）。

Sydney 的开源起点就是在 Django 里想办法让 Pydantic 好用。她把 Pydantic 的定位概括为：Python 不是强类型语言，Pydantic 给想选择更强类型的人一个入口，做数据建模与校验；它是 FastAPI 的骨架——请求和响应本来就需要结构化数据。她还记得它的两个走红阶段：先靠 FastAPI 流行起来，又在 LLM 时代被进一步带火，因为模型产出的是文本，Pydantic 正是把文本校验回可预测结构的那座桥（`00:40:09–00:41:44`）。

选型的 AI 逻辑在 Pat 那里说得最明白：工作上他用 Flask，因为训练语料里 Flask 代码海量，LLM 一吐就能跑；个人项目用 Rust 写、类 Flask、主打多线程的 Robyn，但它语料少，得"驯"着 agent 写对代码。他的土办法是把整个仓库（含文档）下载下来，开一个 Claude Code 会话，让 agent 基于源码和快速上手文档生成一份技能文件，再喂给真正干活的会话——对冷门框架屡试不爽（`00:41:44–00:43:21`）。Reuven 对框架保持中立——Web 在他的应用里戏份不大——但同意语料逻辑：Flask、FastAPI、Django 的存量代码都足够多，LLM 写起来都得心应手（`00:43:21–00:44:03`）。Michael 自认 Flask 阵营，多数 Web 应用用 Flask、也有些 FastAPI；Calvin 和他都惋惜 Pyramid 没能走得更远（`00:44:03–00:44:25`）。

### 类型标注与检查器：给 AI 拴上短绳

这个话题从一个插曲开始：ty 怎么读？Michael 说他专门问了 Charlie Marsh，得到的答案是"就念 ty"（`00:44:32–00:44:54`）。Sydney 是"能用类型就用"派：Python 核心团队这些年让类型的表达清晰容易了很多（哪怕不用 Pydantic），ty 又让类型检查快到可以随手跑；过去开发者嫌类型是负担和样板，如今这些重活可以交给 agent——能多上类型就多上（`00:44:54–00:45:30`）。

Calvin 的出发点相反，结论却相近：他当初为 Python"不打扰、快速把事办成"的气质而来，手写代码通常不加类型；但只要代码交给 AI 和测试流水线，他就要求加类型，为的是确定性——在代码运行之前就接住一整类 bug。他庆幸这仍是可选项（`00:45:33–00:46:50`）。Pat 的 DevOps 单文件脚本不标类型，但 AI 深度参与、将来可能开源的项目会标（`00:46:50–00:47:05`）。

Reuven 讲了自己的转变：从"酷人不需要类型"的动态语言老派立场，到发现团队里总有人会犯错、静态语言出身的人需要那张安全网，于是全押——尤其在 LLM 时代，类型是"给它们拴上短绳的好办法"。他还"后知后觉"地发现类型标注好、Pydantic 更妙：就像 Postgres 的列不只标类型、还带 check 约束，能把可接受的值扎得更紧；他也夸核心开发者让这条类型之路可以按自己的节奏滑入（`00:47:09–00:48:29`）。

Michael 在 C++ 和 C# 里长大，觉得带类型的 Python 反而干净；他的原则是分场合——包的公开函数标类型，让调用方可以验证自己用得对，内部不必铺满，因为"类型是用来沟通的"。类型让编辑器的波浪线变得有意义，也让 agent 规矩起来：他要求 agent 必须跑 ty、跑 ruff、跑测试，全部零警告才算完工（`00:48:30–00:49:28`）。Reuven 的总结更犀利：我们对 agent 提的这些要求，若对人肉团队提足以被投诉"虐待员工"；但 agent 不抱怨，事后还叫你天才（`00:49:28–00:49:49`）。

检查器快速轮里 mypy 与 ty 各有人用：Reuven 还在用 mypy 并自嘲老派，说光是准备这期节目就可能让他改主意；Pat 说项目里的 mypy 是 LLM 自己带进来的，Michael 则会纠正 agent"必须也跑 ty"；Calvin 猜 Six Feet Up 内部经脚手架工具沉淀下来的已是 ty；Michael 顺手穿着 Pyrefly 的 T 恤出场——这款同为 Rust 实现的检查器一样快、扩展也不错（`00:50:01–00:51:07`）。

### 数据库：Postgres 是默认答案，嵌入式在抬头

Sydney 多数事情从 Postgres 起步；她观察到 agent 产出的工件很大，Postgres 加 blob 存储的组合对她的场景往往合适。她还提出：数据建模正在重新时髦——要把数据组织好，让 agent 或其他东西能大规模地查询（`00:51:20–00:51:56`）。Calvin 同样选 Postgres，顺带致敬服务了他几十年的 ZODB（`00:51:56–00:52:01`）。

Pat 的生产环境几乎全是 Postgres，也用 SQLite 和一些 DuckDB；一个副业项目用了轻量内存映射数据库 LMDB——"听起来很酷，也够用"（`00:52:01–00:52:15`）。

Michael 自认 Team Mongo：MongoDB 在运维上就是方便，大多数"迁移"只是加个字段，代码和数据库一起生长；但他同时迷上小型嵌入式数据库——SQLite 经过 write-ahead log 和特定连接模式的打磨，有了持久性与跨进程锁，如果负载就住在一台机器上，嵌入式数据库大多数时候都够用（`00:52:15–00:52:57`）。Pat 补充 DuckDB 的 JSON 特性适合快速攒小工具和 CLI，速度飞快（`00:52:57–00:53:08`）；Reuven 没把 DuckDB 当数据库，而是当 pandas 之上的查询层——在 pandas 自己的数据上跑，居然"惊人地比 pandas 本身还快"（`00:53:08–00:53:22`）。Michael 又提了他刚做过节目的 Duck Lake：把一堆 Parquet 文件放上 S3，拿 DuckDB、SQLite 甚至 Postgres 当元数据前端，就是超可扩展的玩法（`00:53:23–00:53:39`）。

### 文档：同一套页面，给人看也给 agent 看

Calvin 说他们用 MkDocs 且喜欢它；这个生态的新动向是 Material for MkDocs 团队的新一代项目 Zensical——他记得是 Rust 写的、自带速度——FastAPI 的文档已经用上了它（`00:53:58–00:54:40`）。Michael 推荐了 Posit 出品的 Great Docs，说它得到的关注远远不够；他把自己所有小项目从 README 迁了过去（`00:54:40–00:55:11`）。Reuven 指出它与 Great Tables 同出 Posit 之手（`00:55:15–00:55:25`）。

Sydney 介绍了 Mintlify 的 agent 原生方向：LangChain 文档每个页面都有"复制 MCP URL""按 Markdown 复制给 LLM"的入口，还有"复制这条提示词"的组件，让 LLM 直接用上这一页；Pydantic 的文档也已从 MkDocs 搬到 Mintlify（`00:55:32–00:56:05`）。Michael 演示 Great Docs 有类似甚至更进一步的设施：每个库页面自带可安装的技能（不写就自动生成）、把 URL 里的 html 换成 md 就得到 Markdown 版、整页可按 Markdown 复制，还会生成给 LLM 用的 llms.txt 与全文版（`00:56:07–00:57:04`）。

### 托管：容器为主，AI 把服务器价格顶了上去

Reuven 的需求简单：DigitalOcean 的小 droplet 足矣。Michael 帮他"正名"：只要把东西装进 Docker、开一台大服务器，DigitalOcean 能走得很远，控制台也比 AWS、Azure 清爽得多（`00:57:21–00:57:49`）。

Calvin 全押容器：DigitalOcean 的 App Platform 适合把容器连上数据库快速起一个小应用；重项目两条路——要么 Talos Linux 上的大型 Kubernetes 集群，要么单节点 K3S。他眼中 Kubernetes 的杀手锏是拿控制台 URL 发布代码，不必 SSH 进机器去 clone 或 pull。轻量场景他用 Cloudflare Workers 和 API 网关——Python 在 Workers 上已是一等公民，他正用它逐个替换自己的 Zapier 自动化（`00:57:49–00:58:49`）。Michael 顺势预告：几周后请 Cloudflare 的 Python Workers 团队上节目（`00:58:49–00:58:57`）。

Pat 的公司九成以上在 AWS：多个 EKS 集群加一个 ECS 集群；少量负载和身份验证在 Azure；又因 Oracle 收购 Zenedge 而顺带用上 Oracle Cloud，当 CDN 和 WAF（`00:58:57–00:59:26`）。

最扎眼的数字来自 Michael：他在 Hetzner 的一台 8 核 16 GB 服务器月付 35 美元，新价格涨到 130 美元——他把这归因于 AI 对硬件价格的推高，并说现在按美元算，DigitalOcean 反而更划算（`00:59:26–01:00:08`）。

### AI 工具快速轮：各家的搭配与自托管的现实

讨论中段其实已埋了伏笔：最新模型在编码会话里更多是连续调用 bash、跑复杂脚本，而不是简单的读写文件（`00:34:58–00:35:31`）。Calvin 因此用 Agents View 复盘自己的 agent 会话——看到 85% 的会话都是 bash 调用时，他希望工具粒度能一眼可辨（`00:35:49–00:36:08`）。Michael 和他差不多同时在 Python Bytes 上发现这个工具：他把几台 Mac 的会话都推进一个中央 Postgres Docker 容器，得到所有机器 AI 使用情况的总览——最吓人的是它按真实价格显示 token 成本（`00:37:01–00:37:44`）。

收尾的快速轮按人过一遍。Calvin：Pi 和 Claude Code，以 Pi 为主，配 superpowers 技能；模型多数时候用 Sonnet 5.5，也会用 OpenAI 刚发布的那个（他记作 6.1），并抱怨被默认切到最新 Opus 后 token"哗哗地流"（`01:00:38–01:01:05`）。Sydney：一个趁手的编码 agent，加上 Slack 里的 agent 和 Notion（她放文档的地方）里的 agent；她看好 MCP 和技能——前者连接数据，后者沉淀领域知识；最期待用记忆让 agent 随时间变好，比如编码 agent 记住她的偏好、改博客的 agent 吸收人类审稿人的意见（`01:01:05–01:02:02`）。

Pat 说他们已经定了常用的工具，后端模型先让它自动选，但要盯着 token 开销；他本地用 VS Code、也用 Kiro，并感慨公开模型太能打，本地跑的模型"有点拿不出手"（`01:02:02–01:02:34`）。Reuven 把约 95% 的活交给 Claude Code；试过 OpenCode 后他给出一个类比——Claude Code 像 Mac，OpenCode 像 Linux："即刻可扩展，但要花时间配置"；Pi 在他的待试清单上（`01:02:34–01:03:01`）。

Michael 同样是 Claude Code 加 VS Code；个人小自动化里他用了很多 GLM 5.3 Flash——还不能自托管，但跑在别处每月 5 到 10 美元，不算贵（`01:03:02–01:03:19`）。节目随后给出内存门槛：GLM 5.3 Flash 估计要 750 GB 内存，非 Flash 版约 1.5 TB，"所以不自己托管"；想自托管，则有人推荐千问（Qwen）系模型，称其能力惊人、多数 32 GB 以上内存的机器就能跑（逐字稿对型号的音记不全，此处不展开型号）（`01:03:23–01:03:40`）。

## 来源与定位

- 原始节目：[#566: State of the art in Python 2026](https://talkpython.fm/episodes/show/566/state-of-the-art-in-python-2026)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 开场题眼、嘉宾名单与录制日期（00:00:00–00:00:45）
  - 四位嘉宾自我介绍与背景（00:06:23–00:10:39）
  - 编辑器话题：历史之问与 AI 搅局（00:10:58–00:11:33）
  - Sydney 在 Slack 里派活、Reuven 与 Calvin 的 agent 编辑器（00:11:44–00:15:31）
  - Pat：穿孔卡片到 K-Edit、VS Code 远连与 Vim/Nano（00:15:31–00:16:41）
  - 终端话题：Royal TS、Kitty、herdr、Ghostty、CMUX（00:17:55–00:23:44）
  - CLI 作为 LLM 接口与 Spark CLI（00:24:14–00:24:55）
  - Talk Python CLI 与 uvx（00:24:55–00:25:23）
  - 无 pip 年代与 uv 补课（00:25:32–00:25:50）
  - 3.15 发布悬念与 uv 安装 3.15（00:25:55–00:26:12；00:31:36–00:32:07）
  - Poetry 俳句机器人与 uv 收编既有习惯（00:26:12–00:27:38）
  - uv 提速比肩 AI、Astral 并入 OpenAI（00:27:38–00:28:35；00:29:51–00:30:16）
  - Reuven：打包之乱被 uv 解决（00:30:16–00:31:30）
  - uv 活在 Python 之外、容器弯路与 venv 之恨（00:32:08–00:33:32）
  - Sydney：模型为何偏爱 uv（00:33:32–00:34:55）
  - bash 调用观察与 Agents View 复盘（00:34:58–00:37:44）
  - Web 框架：Sebastian 缺席、DjangoCon 对比与按任务选型（00:37:57–00:38:41）
  - Sebastian 的库技能仓库（00:38:41–00:39:29）
  - FastAPI 的真实卖点与 Django Ninja（00:39:39–00:40:03）
  - Pydantic 的定位与两个走红阶段（00:40:09–00:41:44）
  - Flask/Robyn 的语料逻辑与仓库生成技能法（00:41:44–00:44:03）
  - Pyramid 的遗憾（00:44:03–00:44:25）
  - ty 的读法与 Sydney 的类型立场（00:44:32–00:45:30）
  - Calvin：手写不标、给 AI 标（00:45:33–00:46:50）
  - Reuven 从怀疑到全押与 Pydantic 类比（00:47:09–00:48:29）
  - Michael：公开接口标类型、agent 零警告（00:48:30–00:49:49）
  - 类型检查器快速轮：mypy、ty 与 Pyrefly（00:50:01–00:51:07）
  - 数据库：Postgres 默认与嵌入式抬头（00:51:20–00:53:39）
  - 文档：MkDocs、Zensical、Great Docs 与 Mintlify（00:53:58–00:57:04）
  - 托管：DigitalOcean、Kubernetes 与 Cloudflare Workers（00:57:21–00:58:57）
  - AWS、Azure 与 Oracle 布局（00:58:57–00:59:26）
  - Hetzner 35 美元涨到 130 美元（00:59:26–01:00:08）
  - AI 工具快速轮与自托管现实（01:00:38–01:03:40）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
