---
item_id: talk-python-8886ed288731
title: Python 开发者的 Rust 上手地图：三种相遇方式与编译期纪律
date: '2026-09-17'
published_at: '2026-09-16'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://talkpython.fm/episodes/show/563/getting-started-with-rust-as-python-devs'
source_name: 'Talk Python To Me'
input_type: official_transcript
transcript_url: 'https://talkpython.fm/episodes/show/563/getting-started-with-rust-as-python-devs.vtt'
summary: 'Christopher Trudeau 面向 Python 开发者讲 Rust 入门：Ruff/Pydantic/Granian 三种相遇方式、所有权与借用检查的编译期纪律、cargo 与 PyO3 工具链，以及「先测量再优化」的 Amdahl 定律提醒。'
tags: [Rust, Python, 编程语言]
---

# Python 开发者的 Rust 上手地图：三种相遇方式与编译期纪律

> 节目：[Talk Python To Me](/podcasts/talk-python/)
>
> 节目发布：2026-09-16 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 4624 字 · 阅读约 12 分钟
>
> 标签：[Rust](/tags/Rust/) [Python](/tags/Python/) [编程语言](/tags/编程语言/)
>
> 🎧 [收听原节目](https://talkpython.fm/episodes/show/563/getting-started-with-rust-as-python-devs) · 📄 [查看官方逐字稿](https://talkpython.fm/episodes/show/563/getting-started-with-rust-as-python-devs.vtt)

## 速读

Christopher Trudeau 面向 Python 开发者讲 Rust 入门：Ruff/Pydantic/Granian 三种相遇方式、所有权与借用检查的编译期纪律、cargo 与 PyO3 工具链，以及「先测量再优化」的 Amdahl 定律提醒。这期不是把听众培养成 Rust 专家，而是让你在读 Pydantic 源码、给热点路径换 Rust 库、或者评估要不要写点 Rust 时心里有数。嘉宾是顾问兼 Real Python 播客联合主持 Christopher Trudeau（`00:04:03–00:04:42`），他在 Talk Python 出了课程 Up and Running with Rust（`00:00:27–00:00:34`）。适合被 Rust 生态「包围」但还没动手的 Python 开发者。

## 主题正文

### Rust 与 Python 的三种相遇

Trudeau 把 Rust 与 Python 的交集分成三类。第一类是「碰巧用 Rust 写的 Python 工具」，比如 linter 和 uv：它们并不真正与 Python 集成，换成 C 写也一样，价值在速度——当工具从「慢一个数量级」变成「快几个数量级」，工作方式就变了（`00:19:01–00:20:10`）。主持人 Michael Kennedy 的体感是 Ruff「快得不讲道理」：他在约 17 万行的培训应用上跑 Ruff，结果瞬间返回，他一度以为是配置错了（`00:20:24–00:21:17`）；「从零 lint 整个 CPython 代码库只要 0.3 秒」（`00:22:33–00:22:45`）。

第二类最常见：Pydantic、Polars 这类库用 Rust 写核心，再通过 Python 的 C 扩展接口暴露一层「很薄的表皮」，Python 侧把它当普通模块用（`00:22:46–00:25:31`）。Trudeau 认为这里 Rust 相对 C 的优势是语言本身更干净、脚枪更少，同时保留了迭代器、集合这些现代语言设施（`00:24:45–00:25:31`）。第三类是 Granian 这样的反向操作：Rust 写的应用服务器内嵌 Python 解释器，Python 代码照常跑，但外壳是 Rust（`00:27:06–00:27:51`）。两人用焦糖苹果打了一串比方——Python 裹着 Rust 核、Rust 壳包着 Python 芯、工具是蘸焦糖的苹果片——比方未必严谨，但三种结构关系是清晰的（`00:26:05–00:27:05`）。

### 编译期纪律：所有权与消失的一类 bug

两人约定只讲最小必需的 Rust。核心规则是「同一时刻只有一个所有者」：Python 里随手传引用、交给垃圾回收；Rust 里同样的写法直接编译不过（`00:07:11–00:07:48`）。社区的老笑话是「Rust 没有 bug，你的时间都花在让它编译上」（`00:07:35–00:07:48`）。Trudeau 强调编译器的报错质量：错误信息非常明确，常常直接给出修复建议，而且「八九成的时候是对的」，学会它的「词汇」之后就会意识到「哦，又是借用检查器」（`00:08:05–00:08:34`）。

代价换到的是一整类 bug 的消失。Trudeau 用 C 字符串举例：以 null 结尾的缓冲区一旦写越界，或者指针指向已释放的内存，程序可能不崩但读到脏数据，也可能直接倒下（`00:10:25–00:11:35`）。Rust 不是没有 bug，「但有一类 bug 它根本不让你制造出来」（`00:11:35–00:11:43`）。Kennedy 补充了另一个角度：Python 靠动态性换启动速度，类型不匹配要等运行时才暴露；Rust 把这些全部提前到编译期（`00:11:54–00:12:19`）。

### 硬件视角的语言：整数、栈堆与真编译产物

对从 Python 过来的开发者，冲击最大的是数字。Python 的整数无上限，做位运算、超大数运算都很自在（`00:12:42–00:13:08`）；Rust 更贴近机器，8 位整数塞不进 9 位，有没有符号都要自己选（`00:13:08–00:13:55`）。Trudeau 点破取舍：Python 无界整数的灵活性背后是运行时机器，这也是 Python 慢的原因之一；Rust 直接优化到 CPU 的行为，快就快在这里（`00:14:35–00:15:12`）。严格的类型系统同样来自硬件：CPU 对整数、浮点各有明确的大小与解释方式，Rust 要求你在设计时就决定（`00:36:05–00:37:42`）。

栈与堆在 Rust 里是显式概念：函数调用与参数在栈上，长生命周期、跨函数传递的东西在堆上（`00:38:35–00:40:11`）。Kennedy 给出一个反直觉的对照：Python 让你完全不用管指针，恰恰因为「一切都是指针、一切都在堆上」，连数字 1 都是；CPython 还对小区间整数做了预分配（Kennedy 口径「大概是 −5 到 255」），所有字面量 72 都指向同一个不可变对象（`00:40:17–00:41:56`）。此外 Rust 编译出的是平台相关的机器码，分发极简单但必须逐平台编译；没有真正的 REPL，社区那些「类 REPL」工具本质上是在后台反复重编译（`00:31:19–00:34:18`）。

语法表层对 Python 开发者相当友好：声明长得像带类型标注的 Python，循环和条件几乎可以平移（`00:28:03–00:30:12`）。分歧从缩进开始：Rust 用花括号，Trudeau 给 Python 的缩进设计打了「八成赞成、两成保留」——结构即可读性很好，但复制粘贴和重排版可能悄悄改变语义（`00:42:04–00:43:54`）。版本策略则值得羡慕：Rust 六周一版，但引入「edition」概念，三年一个 edition、内部保持兼容，编译器还能指定面向旧 edition 编译；Trudeau 一边喜欢这份「永远向后兼容」，一边担心「要是有 35 个 edition 怎么办」（`00:46:44–00:47:53`）。

### 工具链与包管理：cargo/uv、crates 信任与一场旧争论

上手路径很短：rustup 负责安装并管理 rustc 与 cargo，cargo 才是你天天用的工具，「很像 uv」；cargo new 会生成 cargo.toml（对应 pyproject.toml）、src 目录和可编译的 stub（Trudeau 顺手关掉了它自动建 git 仓库的行为）（`00:48:30–00:49:58`）。cargo run 一键构建并运行，调试构建大约大 30%（`00:49:58–00:50:35`）。crates.io 对应 PyPI：节目里现场报数，crates 约 33 万、PyPI 约 89 万（`00:51:36–00:52:18`）。

更值得留意的是生态感受的差异。Rust 标准库刻意保持小，「随机数都是一个 crate」；Trudeau 自认偏执，习惯用「标准库 = 安全，标准库之外要有人背书」的方式建立信任，而在 Rust 世界他还没找到等价的信息来源（`00:52:29–00:53:47`）。由此引出一场争论：Kennedy 指出 uv 等工具的许多灵感来自 cargo，而 Python 的包管理生态是「 PyPI 和 npm 已存在之后」才长出来的；Trudeau 直说 PSF 当年「包管理不属于语言」的决定是个错误，Rust 把 cargo 内置进来干净得多，不过他也承认 wheels 已经让 Python 好了很多，「batteries included」其实是没有 PyPI 的 1991 年的历史产物（`00:53:59–00:56:45`）。

### 回到 Python：PyO3 混合开发与 Amdahl 定律的冷水

从 Rust 回 Python 的桥是 PyO3：用宏把普通 Rust 函数或类暴露给 Python，PyInt 这类类型与 Python 对象互映射，编译成动态库后用 maturin 打包进虚拟环境，Python 侧 import 即用（`00:57:15–00:59:48`）。混合项目不必「全有或全无」：Polars 安装时就带两个 wheel——一个纯 Python 的 universal wheel、一个平台相关的编译 wheel（`00:59:48–01:00:47`）。

但 Trudeau 反复强调跨界有成本：如果设计成频繁来回穿越边界，Rust 可能反而更慢；合适的形态是「把大批量计算整块交给 Rust」，比如 Polars 的数值 crunch、Pydantic 的 JSON 转换（`01:01:23–01:02:21`）。他给出的通用建议是「先别优化，先测量」：直觉在瓶颈问题上经常错得离谱（`01:03:08–01:03:48`）；再用 Amdahl 定律泼冷水——占 10% 时间的代码提速 2 倍，整体只快 10%；Kennedy 推到极端：占 20% 时间的代码就算优化到无穷快，整个程序也只快 20%（`01:03:48–01:05:09`）。想深入的话，两人推荐 The Rust Book 和 Awesome Python RS 清单；很多「Python 库」其实只是成熟 Rust 库的薄封装，背后是数千 star 和双社区的使用量（`01:05:52–01:08:55`）。

## 来源与定位

- 原始节目：[#563: Getting Started with Rust as Python Devs](https://talkpython.fm/episodes/show/563/getting-started-with-rust-as-python-devs)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Rust 与 Python 的三种相遇方式：工具、薄封装库、内嵌 Python 的服务器（00:19:01–00:27:51）
  - Ruff 的速度观感：17 万行应用近乎瞬时、CPython 全库 0.3 秒（00:20:24–00:22:45）
  - 所有权规则、借用检查、报错质量与消失的 C 内存 bug 一族（00:07:11–00:11:54）
  - 整数宽度与有无符号、性能来源（00:12:42–00:15:12、00:36:05–00:37:42）
  - 栈与堆、「Python 万物皆指针」与小区间整数缓存（00:38:35–00:41:56）
  - 平台相关机器码、分发与 REPL 的代价（00:31:19–00:34:18）
  - 语法表层、花括号对缩进的八二开与 edition 策略（00:28:03–00:30:12、00:42:04–00:47:53）
  - rustup/cargo/crates.io 工具链与「随机数都是一个 crate」的信任难题（00:48:30–00:53:47）
  - PSF 不做包管理的争论、uv 与 cargo 的相互启发、wheels 的进步（00:53:59–00:56:45）
  - PyO3 与 maturin、Polars 双 wheel、跨界成本与批量计算形态（00:57:15–01:02:21）
  - 先测量再优化、Amdahl 定律与学习资源（01:03:08–01:05:09、01:05:52–01:08:55）

## 整理说明

- 本文基于节目内容与出版方公开的官方 WebVTT 逐字稿整理。
- 定位采用逐字稿自带的 cue 时间戳；开场字幕「Lent the entire CPython code base」应为「Lint」，结尾一行俄语占位字幕为出版方字幕的收尾噪声，均不影响正文。
- 「约 17 万行」「33 万 crates / 89 万 PyPI 包」「0.3 秒」「−5 到 255」等数字均为对话口径，本文未独立验证；Kennedy 对小区间整数范围明确使用了「大概」的措辞。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
