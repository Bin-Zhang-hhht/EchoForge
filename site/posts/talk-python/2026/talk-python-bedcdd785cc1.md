---
item_id: talk-python-bedcdd785cc1
title: 'Cloudflare Python Workers：在边缘节点跑 Python'
date: '2026-11-16'
published_at: '2026-11-03'
transcribed_at: '2026-11-16'
model: 'GLM-5.3 Flash'
source_url: https://talkpython.fm/episodes/show/568/cloudflare-python-workers
source_name: Talk Python To Me
input_type: official_transcript
transcript_url: https://talkpython.fm/episodes/show/568/cloudflare-python-workers.vtt
summary: '这期讲清正式可用的 Cloudflare Python Workers：Pyodide 把 Python 放进浏览器，Cloudflare 把浏览器放进服务器，CPython 以 WebAssembly 跑在 350 多个边缘节点；含 uv 部署、socket 适配、D1/R2/Hyperdrive 与 128 MB 内存、10 毫秒免费 CPU 等限制。'
tags: [Python, 云服务, 开发者工具]
---

# Cloudflare Python Workers：在边缘节点跑 Python

> 节目：[Talk Python To Me](/podcasts/talk-python/)
>
> 节目发布：2026-11-03 · 逐字稿获取：2026-11-16 · 笔记整理：2026-11-16
>
> 全文共 8917 字 · 阅读约 23 分钟
>
> 标签：[Python](/tags/Python/) [云服务](/tags/%E4%BA%91%E6%9C%8D%E5%8A%A1/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://talkpython.fm/episodes/show/568/cloudflare-python-workers) · 📄 [查看官方逐字稿](https://talkpython.fm/episodes/show/568/cloudflare-python-workers.vtt)

## 速读

这期讲清正式可用的 Cloudflare Python Workers：Pyodide 把 Python 放进浏览器，Cloudflare 把浏览器放进服务器，CPython 以 WebAssembly 跑在 350 多个边缘节点；含 uv 部署、socket 适配、D1/R2/Hyperdrive 与 128 MB 内存、10 毫秒免费 CPU 等限制。

本期录制于 2026 年 10 月 9 日，嘉宾是 Cloudflare 的 Hood Chatham、Gyeongjae（Jay）Choi 与 Dominik Picheta：前两位是 Pyodide 维护者，Dominik 最早在 Cloudflare Workers 里让 Python 跑起来（`00:00:10–00:00:40`）。主持人 Kennedy 用一个类比概括这套平台：像 CDN，只是分发的不是静态资源而是程序，并把程序运行在你的数据上（`00:30:51–00:31:03`）。

节目同样保留了嘉宾自己声明的边界：内存 128 MB、免费档每天 10 万次请求、CPU 时间免费档 10 毫秒/付费 5 分钟（`00:48:43–00:49:42`）；不适合数据科学，平台没有 GPU 与 SIMD 算力，SciPy 因体量过大实际无法导入（`00:53:15–00:54:51`）。文中所有数字均为节目中的说法。

## 主题正文

### 从「Python 进浏览器」到「浏览器进服务器」

三位嘉宾的来路都和 Pyodide 有关。Dominik 曾参与 Nim 语言开发，从 Meta 转到 Cloudflare 的 Workers 运行时团队，是最早在 Cloudflare 里试验 Pyodide 并把它跑起来的人，之后一直负责 Python Workers（`00:03:42–00:05:46`）。Choi 从 2021 年起为 Pyodide 做贡献，后来被 Cloudflare 邀请来做 Python Workers（`00:05:20–00:05:46`）。Hood 是数学出身，在国家科学基金会博士后期间把主要精力花在 Pyodide 上，离开博士后岗位时先被 Anaconda 请去做 PyScript，约半年后加入 Cloudflare 促成 Python Workers（`00:10:09–00:10:34`）。

Pyodide 的目标是「在 WebAssembly 能跑的任何地方运行」，主要是浏览器，但不必是浏览器：可以把它当成一种 Docker 式的隔离手段，它不支持纯 WASI 运行时，却能在任何 JavaScript 运行时里工作——Node、Bun 都可以（`00:11:22–00:11:52`）。Cloudflare 的想法是把 Pyodide 这个「迷你 Python 运行时」放到离用户尽可能近的地方执行，省去回源到某个数据中心的延迟；接入点数量按嘉宾现场说法「在 350 以上」（`00:11:59–00:13:05`）。Kennedy 特意澄清：代码并不像 Pyodide 那样跑在用户浏览器里，而是跑在靠近用户的 Cloudflare 边缘节点上，因此能用上数据、队列等整个平台（`00:13:05–00:13:28`）。Hood 的概括是：Pyodide 是「把 Python 放进浏览器」，Cloudflare 是「把浏览器放进服务器」，两件事合起来就是 Python 进了服务器（`00:13:28–00:13:47`）。

与传统 serverless 的对比中，Dominik 认为 Workers 比 AWS Lambda 更「无服务器」：Lambda 要自己选部署区域，Workers 不用操心放置问题，代码自动出现在用户附近（`00:29:08–00:29:52`）。请求的机制按 Kennedy 的复述是：用户连到最近的接入点，那里的 Workers 运行时带着 V8，V8 里跑 WebAssembly 形式的 Pyodide，开发者不参与选址，这是 CDN 式的调度（`00:30:04–00:30:50`）。发布节奏方面，官方公告在 9 月 21 日宣布 Python web workers 正式可用；Dominik 回忆自己 2023 年 10 月入职，约六个月做出 beta，之后用了两年多才走到 GA（`00:41:17–00:41:50`）。

### 打包与部署：PEP 783 之后的 uv 工作流

Pyodide 的底层平台是 Emscripten 编译工具链（Clang 前端，外加 JavaScript 实现的系统调用与文件系统）。Hood 说明，Emscripten 在上游 CPython 只有 tier 3 支持：跑 CI、尽力维护、允许被别人改坏再由他修复，不构成发布阻塞，而且上游不为 Emscripten 出正式版本——因为这个构建缺少 os 模块级别的 IO、发不了请求、收不了用户输入，按他的说法「没人会想用上游构建出的那种可执行文件」（`00:16:00–00:17:30`）。

两个 PEP 构成了这期的标准线。一个是几天前刚提交给指导委员会评审的 PEP 818（标题按 Kennedy 现场读的是「把 Pyodide 外部函数接口的核心加入 Python」），作用类似 ctypes/cffi 之于 C：让 Python 能调用 JavaScript 函数——JavaScript 运行时里几乎所有能力都要经过 JavaScript，正如 Linux 上一切都要经过 C；目前是草案，预计几个月内出决定（`00:17:30–00:18:40`）。另一个是已接受的 PEP 783（Emscripten 打包）（`00:18:41–00:18:48`）。

打包是 Pyodide 多年的老大难。Choi 回顾：纯 Python 包可以直接运行，但 NumPy、SciPy 这类含 C/C++/Rust 代码的包必须交叉编译到 WebAssembly；2025 年之前所有包都要在 Pyodide 自己的 CI 里构建——约 300 个包、每轮三四个小时，改一行代码也得等几小时，而且 Python 打包系统实时执行代码、相当脆弱，CI 经常坏（`00:19:17–00:20:35`）。出路是让上游项目自己构建 Pyodide wheel——这就是 PEP 783，又经过约一年讨论才被接受（他归功于 Hood 的大量工作）；他们还标准化了构建系统，项目用 cibuildwheel 加一个平台参数就能在自己的 CI 里出 wheel（`00:20:48–00:21:42`）。

残留的困难仍在编译器侧。Hood 承认他们有一个「可怕的编译器包装器」，靠改写编译参数兜住各种问题，交叉编译依然不易、只是被抽象进了构建系统（`00:21:57–00:22:18`）。他的担忧是编译器回归：升级 Python 3.15、追平最新 Emscripten 时连跨约 10 个版本，「几乎每个都有某种奇怪回归」，而这类问题往往要等下游包维护者真正使用时才暴露，所以他觉得可能仍需自带一批包的构建来覆盖平台（`00:22:18–00:23:45`）。Dominik 总结打包 PEP 的意义在于让维护者自己为 WebAssembly/Pyodide 构建、把负载分摊出去，长尾包才有机会可用；Kennedy 补充 PyPI 快到 100 万个包；Hood 估计其中只有约 5% 含 C/C++/Rust（`00:24:01–00:25:06`）。另一位 Pyodide 维护者做了网站跟踪哪些包已有 PEP 783 wheel——绿色是已在 PyPI、蓝色是 Pyodide 仍在自建、黄色是尚不支持；Choi 说多数 Python 应用依赖 top 500 包，这是他们的支持目标（`00:25:06–00:25:58`）。

纯 Python 也不等于能用。Kennedy 提醒 Pyodide 缺了运行时的一些部分：Choi 列举 threading、multiprocessing、subprocess 这类依赖平台能力的功能——原生 socket 在浏览器版 Pyodide 里基本不行，在 Cloudflare Workers 或 Node.js 里部分可用，但线程与子进程仍然不行（`00:26:00–00:26:47`）。asyncio 则是 Hood 接手维护初期的重要工程，因为浏览器里一切都是异步，没有好的 asyncio 故事时只能层层回调（`00:26:47–00:27:06`）。

部署侧因此相当轻：用户不构建任何 WebAssembly——产物都是预构建好的。写好 Python 代码，用 uv 把针对 WebAssembly 构建的依赖包安装到本地文件，再把应用与依赖整体压缩上传到 Cloudflare 的服务器分发到全球；运行时下载应用并放进 Pyodide 执行（`00:31:04–00:31:59`）。本地开发依托开源的 workerd（Workers 运行时的开源部分，GitHub 上可得）和 Wrangler CLI（正在向 cf 过渡）：编辑文件自动重载、本地发请求调试；本地与生产是同一个运行时，生产里会发生的事本地都能测——Kennedy 认为这一点与 Lambda 或托管 Kubernetes 上的「近似模拟」截然不同（`00:32:08–00:33:28`）。

### 平台积木：D1、Hyperdrive、R2 与套接字适配

D1 是「给每个 worker 一个本地 SQLite 数据库」：Dominik 说自己写应用早就爱用 SQLite，D1 可以写、全球为你复制、随 worker 扩展，无需操心；Kennedy 补充大约有 300 个数据库节点，并强调 SQLite 不是玩具、速度非常快（`00:34:12–00:35:12`）。两地同时写怎么办？Dominik 直说不知道细节，但平台有保证一致性、避免冲突的机制；Hood 认为这正是 Python Workers 设计的好处——直接消费这些能力，不必了解内部（`00:35:12–00:35:35`，`00:36:07–00:36:15`）。

Hyperdrive 按 Choi 的说法相对较新，本质是边缘代理：源库（PostgreSQL、MySQL 等关系数据库）是事实来源，分布在边缘的约 350 个 Hyperdrive 维护与源库的连接池，让读写更快，还可以对不常变的表开启缓存（`00:36:16–00:37:10`）。Hyperdrive 能工作的前提是 socket：Kennedy 点明这正是 Choi 在做的「让 socket 在 Workers 的 Python 里可用」，Hyperdrive 建立在 TCP socket 之上（`00:37:13–00:37:35`）。浏览器从来没有 socket，Pyodide 原本不支持；GA 前的主要目标之一就是接上它——他们把 Node.js 的 socket API 接进 Pyodide，Python 侧的 socket 系统调用实际落到 Node 的 socket 调用上（`00:37:36–00:38:17`）。Hood 补充了实现难度：Node 的 socket API 全异步，而 Linux 的 socket 系统调用是同步的，于是系统调用要栈切换——挂起、让 JavaScript 事件循环把 IO 跑完再切回来；这一切对使用 libc socket API 的 C 代码透明，C 应用直接就能用（`00:38:18–00:39:01`）。他们还为此维护了叫 WebLoop 的 Python 事件循环，订阅宿主事件循环——因为真正的 IO 只发生在宿主循环上，自建循环做不了 IO 还会阻塞真正干活的循环（`00:39:01–00:39:50`）。

R2 是类 S3 的对象存储：Dominik 说它与 S3 几乎一样，名字就来自 S3（2 等于 3 减 1、R 等于 S 减 1），主要差异是没有出口流量费，因此更便宜（`00:39:50–00:40:19`）。这些平台件不强制搭配 Workers 使用——Kennedy 指出单用 R2 做对象存储也成立（`00:40:20–00:40:31`）。此外还有 Cloudflare Queues 与 Workers AI（边缘 AI 推理），按 Dominik 的说法可以按需组合成全栈应用，平台组件每月都在新增（`00:40:35–00:41:17`）。

### 冷启动、内存快照与运行限额

两年多走向 GA 的工作里，打包是一大块；另一条主线是冷启动，尤其是带依赖包时的启动速度（`00:41:50–00:42:34`）。早期方案只允许使用 Pyodide 内置的少数包，后来发现不够灵活，转向一款基于 uv 的工具（嘉宾口称 PyWrangler），任意包都能装进 worker（`00:42:34–00:42:47`）。内存快照是 Hood 入职后立刻接手的方向，他先花约两个月调研才写出第一行代码（`00:42:52–00:43:03`）。

他在 Python Language Summit 和 EuroPython 讲过快照的核心难点：内存快照强行引入「启动期（顶层执行）」与「运行期」的区分，而 Python 语言本身没有这个概念——解释器启动后自举，然后一直 eval 用户代码，import 语句本身就是代码执行而非链接（`00:43:04–00:44:18`）。快照的理由是：每次冷启动执行的顶层代码完全相同、结果也相同，重复执行纯属浪费，不如把这份工作存下来（`00:44:18–00:44:44`）。他类比说这与 PyPy、GraalPython 这类优化编译器做的部分求值面临同一个根本问题：要给一门没有启动/运行之分、没有预编译概念的语言强加一个模型（`00:44:44–00:45:12`）。有与会开发者当场表示这对 Python 语言而言已行不通、为时已晚，Hood 也认同这个判断（`00:45:12–00:45:27`）。实现层面则相当「可怕」：加载动态库时记下重定位基址，再 patch malloc，恢复快照时强制把库重定位回同一地址，整套把戏才能成立（`00:46:22–00:47:23`）。

编程模型以 API 服务器为主，官方示例大量使用 FastAPI；Kennedy 的体会是会写 FastAPI 就等于会用——只是把 uvicorn.run 换成把 app 对象交出去即可，端点数量没有限制（`00:47:35–00:48:43`）。

限额方面按嘉宾口径：内存 128 MB；免费档每天 10 万次请求；CPU 时间免费档 10 毫秒、付费 5 分钟——他们建议以搜索「workers limits」看到的官方页面为准（`00:48:43–00:49:42`）。一个花了大量心思的细节是 CPU 限额的优雅中断：耗尽 10 毫秒时要给 Python 运行时发信号、体面地中断执行并交还控制权。天真的做法是 JavaScript 抛出不可捕获的异常、强制展开调用栈、不执行 finally 与 catch 块——锁不会释放、文件写一半缓冲没刷，运行时直接坏掉；他们为此做了复杂的处理，让 CPU 限制器把信号正确送达运行时里的 Python/Emscripten「操作系统」，Rust Workers 采用同一方案（`00:49:44–00:50:56`）。Kennedy 感叹每天 10 万免费请求「很多」，许多业余应用远用不满；Dominik 说对爱好者定价宽松，他自己做学生时就受益于免费层，R2 约有 10 GB 免费额度，存储、运行时都能免费用；Kennedy 补充出口流量才是 S3 上常见的开销所在（`00:51:04–00:51:45`）。

### 适用场景与嘉宾给出的边界

框架兼容性走 WSGI/ASGI 适配层：FastAPI、Django、Flask 这类框架原则上都能跑，前提是别起太多线程；官方提供通用的 ASGI 与 WSGI 适配器，已经打磨得相当成熟。这正是框架类应用与 urllib3 这类自己做 IO 的库的区别——urllib3 的常规 IO 路径在 Pyodide 上行不通，要单独适配，而框架靠适配器绕开了这个问题（`00:51:49–00:52:48`）。

场景判断上，Hood 看到的 Workers 多是「一大堆无聊的业务逻辑」；他不建议拿来做数据科学——平台没有 GPU、SIMD 这类算力（`00:53:15–00:53:38`）。小规模数据任务原则上可行：两万行的 pandas 或 parquet 文件做点查询、画个图「看起来能行」，pandas 可以加载；但 SciPy 太大——带 100 多个共享库，实际上没法导入，是 Pyodide 里的老大难（`00:53:53–00:54:51`）。Choi 的建议是 Workers 是内存受限环境，数据处理应走流式而不是把 DataFrame 全塞进内存——「更多 Polars、更少 pandas」；而传统 Python 包对流的优化不足，还需要来回磨合（`00:54:56–00:55:37`）。Kennedy 提出另一条路：把 parquet 和 WebAssembly 产物放到前端，用 JupyterLite 式的浏览器运行时执行，算力由终端用户的设备买单；Hood 说很多人正这么做，这种方案对「不是开发者、不是运维」的研究者尤其友好（`00:55:39–00:56:29`）。

收尾环节再次确认了内存快照的用途——让冷启动不再重复执行启动过程（`00:57:48–00:58:13`）。三位嘉宾的最终建议：Dominik 说 Workers 最适合 IO 密集、搬运大量字节而 CPU 消耗少的应用，免费档能支撑的用户数会让人惊讶；Choi 自己的业余应用已经跑在 Python Workers 上、效果很好；Hood 则推荐开发者关注 WebAssembly 生态——基础计算层面缺的东西很多、从业者很少、有大量空白可以补位（`00:58:14–00:59:47`）。

## 来源与定位

- 原始节目：[#568: Cloudflare Python Workers](https://talkpython.fm/episodes/show/568/cloudflare-python-workers)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 嘉宾身份、Pyodide 维护者与录制日期（00:00:10–00:00:40）
  - Dominik 与 Choi 的背景、Cloudflare 的由来（00:03:42–00:05:46）
  - Hood 的博士后、Anaconda 与加入 Cloudflare（00:10:09–00:10:34）
  - Pyodide 的目标与可运行的运行时（00:11:22–00:11:52）
  - 350 多个接入点与低延迟动机（00:11:59–00:13:05）
  - 不在用户浏览器运行、「浏览器进服务器」类比（00:13:05–00:13:47）
  - Emscripten 平台与上游 tier 3 支持（00:16:00–00:17:30）
  - PEP 818 草案与 PEP 783 已接受（00:17:30–00:18:48）
  - 打包历史：交叉编译、300 包、3–4 小时 CI（00:19:17–00:20:35）
  - 上游自建 wheel 与 cibuildwheel 一行平台（00:20:48–00:21:42）
  - 编译器包装器与版本升级回归担忧（00:21:57–00:23:45）
  - 打包 PEP 分摊负载、PyPI 近百万包、约 5% 含原生代码（00:24:01–00:25:06）
  - wheel 跟踪网站与 top 500 依赖（00:25:06–00:25:58）
  - 纯 Python 不等于可用：线程、子进程、socket 的平台差异（00:26:00–00:26:47）
  - asyncio 的修复（00:26:47–00:27:06）
  - 「比 Lambda 更无服务器」与请求运行机制（00:29:08–00:30:50）
  - 「分发程序并对你的数据运行程序的 CDN」类比（00:30:51–00:31:03）
  - 部署流程：uv 安装 WebAssembly 依赖、无需自建 WASM（00:31:04–00:31:59）
  - 本地开发：开源 workerd、Wrangler 与本地/生产同运行时（00:32:08–00:33:28）
  - D1：worker 本地 SQLite、全球复制与一致性机制（00:34:12–00:35:35；00:36:07–00:36:15）
  - Hyperdrive：边缘连接池代理与缓存（00:36:16–00:37:10）
  - socket 支持如何让 Hyperdrive 工作（00:37:13–00:38:17）
  - 栈切换、对 C 代码透明与 WebLoop 事件循环（00:38:18–00:39:50）
  - R2 与无出口费、平台件可独立使用（00:39:50–00:40:31）
  - Queues 与 Workers AI 等平台件（00:40:35–00:41:17）
  - GA 公告与两年多的开发历程（00:41:17–00:41:50）
  - 冷启动与 uv 工具的转向（00:41:50–00:42:47）
  - 内存快照调研（00:42:52–00:43:03）
  - Language Summit：启动/运行区分、部分求值类比与「行不通」评价（00:43:04–00:45:27）
  - 动态库重定位与 malloc 回放（00:46:22–00:47:23）
  - 编程模型：FastAPI 交接与端点无限制（00:47:35–00:48:43）
  - 限额数字：128 MB 内存、10 万请求/天、10 毫秒/5 分钟 CPU（00:48:43–00:49:42）
  - CPU 限额的优雅中断与 finally 块问题（00:49:44–00:50:56）
  - 免费额度与出口流量对比（00:51:04–00:51:45）
  - ASGI/WSGI 适配器与 urllib3 的对照（00:51:49–00:52:48）
  - 业务逻辑为主、不建议数据科学（00:53:15–00:53:38）
  - 小规模 pandas/parquet 可行、SciPy 过大（00:53:53–00:54:51）
  - 流式处理建议：更多 Polars、更少 pandas（00:54:56–00:55:37）
  - JupyterLite 式浏览器运行时替代路径（00:55:39–00:56:29）
  - 内存快照用于冷启动的收尾确认（00:57:48–00:58:13）
  - 最终建议：IO 密集应用、业余实践与 WebAssembly 生态（00:58:14–00:59:47）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
