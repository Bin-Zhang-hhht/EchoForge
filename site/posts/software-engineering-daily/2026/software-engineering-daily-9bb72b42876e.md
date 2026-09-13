---
item_id: software-engineering-daily-9bb72b42876e
title: 'WebAssembly 3.0：GC、形式化规格与"低级但不能更低"的设计哲学'
date: '2026-09-13'
published_at: '2026-01-20'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/webassembly-3-0-with-andreas-rossberg/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/01/SED1890-WASM.txt'
summary: 'WebAssembly 核心设计者 Andreas Rossberg 讲 WASM 3.0：GC 的 opt-in 设计、effect handlers 与 stack switching、形式化规格与设计同步的方法论。'
tags: [开发者工具, 编程语言, 开放标准]
---

# WebAssembly 3.0：GC、形式化规格与"低级但不能更低"的设计哲学

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-01-20 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 5217 字 · 阅读约 14 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [编程语言](/tags/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80/) [开放标准](/tags/%E5%BC%80%E6%94%BE%E6%A0%87%E5%87%86/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/webassembly-3-0-with-andreas-rossberg/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/01/SED1890-WASM.txt)

## 速读

WebAssembly 核心设计者之一 Andreas Rossberg（编程语言研究者、前 Google V8 团队）接受 SED 访谈（本期主持为 Kevin Ball），讲 WASM 3.0 的全貌。3.0 最大的特性"arguably"是 GC——可自定义引用类型及内存布局、由引擎负责分配释放，设计口号是"low-level as possible, but no lower"：只提供 struct 和 array，不提供对象等内置。对关注 WASM 演进、或需要决定"什么该编译到 WASM"的人，这是一期罕见的标准制定者亲述。

最值得记的三点：GC 完全 opt-in、与线性内存分离，不用也无额外成本（Web 引擎只是复用本已为 JS 存在的 GC）；直接从 WASM 访问 DOM 未必更快——调用开销主要被 DOM 自身的工作支配；以及形式化规格与设计同步进行的方法论——"当形式化变得困难时，设计多半有问题"。

## 主题正文

### 起源：从 Native Client 与 asm.js 到"用正确的方式做"

Andreas 从学界（编程语言理论加实现）加入 Google V8 团队，WebAssembly 由此发端。此前 Web 上只有 JavaScript，编译到 JS"远非理想"且性能不可预测；两次前驱尝试：Google Native Client（允许 x86 代码在沙箱中运行）与 asm.js（emscripten 把 C 翻译成 JS 的严格子集）——他称 asm.js 是"非常聪明巧妙的 hack"，但"不会 scale"。发起者主要是 Google 与 Mozilla 的 JS 引擎团队（特别是 Luke Wagner 与 Ben Titzer），时间"back in 2015, I think"（他自述不确定）。（`00:01:50–00:04:11`）

浏览器环境的最高约束是安全："不能容忍任何未定义行为或任何其他非安全行为"——这一条压在一切之上；Web 缺少常规 OS 服务（无文件系统等），许多语言实现编译到 Web 时须换方式实现。（`00:04:35–00:05:38`）

### 1.0 与 2.0：性能、SIMD 与引用类型

WASM 1.0 定位是服务 asm.js 既有客户，特性集完全面向 C/C++/Rust：线性字节数组内存模型加四种基本数值类型，"非常基础的虚拟 CPU"。关于性能，主持人转述社区"快 30 倍"的个案，他的回应很有层次：低级数值计算可"接近原生性能"；若语言运行时需要 GC 等，就要模拟并与 WASM 抽象对抗。一个反直觉的因果观察：JS 有时反超 WASM——JS 引擎为求快做动态 profiling、动态重编译，可构造出胜过 WASM 的运行时；WASM"不试图那么聪明"。基准测试方面他自嘲有"心理阴影"：V8 团队时期的"benchmark war"让他"基本不相信任何 benchmark"。（`00:05:50–00:09:51`）

2.0 的主特性是 SIMD（向量指令），较小的引用类型特性指明了方向：函数指针需一等传递但不能被窥视位模式（否则"完全不安全"）；externref 可承载宿主值往返传递，不能操作但能持有。（`00:10:12–00:12:50`）

### WASM 3.0 核心：GC 的 opt-in 设计

3.0 最大的特性"arguably"是 GC：可自定义引用类型及内存布局，由引擎负责分配与释放。该特性"有些争议"——不再只是抽象 CPU 能力，偏高级。他的设计口号："low-level as possible, but no lower"。为保持低级：只提供 struct 和 array、不提供对象等内置（对比 JVM）；类型只向引擎描述内存布局，语言运行时仍需自己把数据结构映射到低级表示，区别仅在让引擎代为释放。类型系统因此"显著更复杂"——要避免大量运行时检查，需要始终知道自己引用的是什么。关键工程决策：GC 与线性内存完全分离、opt-in；不用 GC 也无额外成本——Web 引擎里只是复用本已为 JS 存在的同一个 GC。主持人类比 Rust"零成本抽象"，他确认 WASM 也遵循 pay-as-you-go。（`00:13:17–00:16:59`）

其他特性：多重内存（"更多是技术性修正"——此前单模块不能有多个内存造成"性能悬崖"、使静态链接失效）；tail calls（对高效支持函数式语言很重要，GC 与 tail calls 共同使函数式语言及 Java、C# 等 GC 语言得以定位 WASM——条件是"以语言自身实现为前提"，他对谁有 WASM 后端没有完整了解）；异常处理（"in the making for very long"）；Relaxed SIMD——他坦承"not a feature I'm particularly happy about"；确定性 profile——若要完全确定性，规范明确定义其含义。（`00:17:09–00:18:36`，`00:22:49–00:27:55`，`00:39:46–00:43:19`）

### MVP 方法论与标准制定

1.0 有三个主要"泛化缺口"：多返回值（栈机只能返回一个结果"很傻"）、多表格、多内存，最后才补上。1.0 特性集选取原则：覆盖 asm.js 全部功能加当时所有常见 CPU 的交集，保证每条指令到硬件有一一对应。SIMD 是例外："硬件厂商无法就指令、corner case、特性矩阵达成一致"，留下 random gaps，他"really personally hate"。MVP 方法论：先发布能用的东西再扩展——1.0 整体是 MVP，3.0 的 GC 是"GC MVP"，他自嘲"即使它仍可能要花八年"。（`00:18:36–00:22:23`）

标准制定完全公开：委员会对所有人开放，但须走"非常 elaborate 的流程"，最终要说服委员会其他成员。目前仍缺的最大缺口是某种 continuation 机制。（`00:22:49–00:26:15`）

### WASM vs JS 选型：DOM 与 glue code

3.0 后编译到 WASM"对大多数应用都合理"，两个例外：纯粹做 DOM 交互——"probably won't get much value…Definitely not in terms of performance"，且要写 glue code；与 JS 深度集成的语言，target JS 更好。一个反直觉的因果判断：直接从 WASM 访问 DOM 未必更快——调用开销主要被 DOM 自身的工作支配；JS 引擎为优化对象/DOM 访问做了海量工作，要在 WASM 代码生成器里复制这些"很傻，没人愿意做，大概也拿不到多少性能"。进行中的替代是在 component model 语境下定义 DOM/接口层，成熟后"maybe"标准化；阻碍是 Web API"巨大且是移动目标"——主持人称之为 "a fool's errand"。（`00:27:55–00:33:22`）

### 语言互操作与 Component Model

设计公理：语言间不做自动互操作是"非常有意的"——实践中从不成功，最小的不匹配"基本会破坏一切"，该问题在这一层面"本质上不可解"。Component Model 是 WASM 之上的独立层：更高级的模块系统加语言无关的类型语言；WASI 基于其上定义"标准"接口（OS 抽象）。有主见的设计选择：跨语言模块通信采用 shared-nothing 并发模型、不能跨边界传指针——他承认"可能因此不解决所有人的问题"。在 bare WASM 层面互操作需要 ABI；几周前的 face-to-face 会议上他在推动定义 WASM 的 C ABI；component model 可视为"ABI on steroids"。（`00:33:39–00:39:17`）

### 非 Web 用例与确定性

设计上不绑定 Web/JS："web"只是"marketing"，定位是 "universal VM"。边缘计算：Fastly 是最大实践者；嵌入式动机是可移植性——工作组中有 Siemens 的人：嵌入式设备处理器更新频繁，每次重建整个工具链很痛苦；嵌入式需求不同（更精简运行时、要 AOT 不要 JIT），WASM 从设计起就考虑 AOT。区块链作为执行平台特别看重定义良好的确定性语义——复制计算依赖副本间共识。（`00:39:46–00:43:19`）

确定性辨析：此处 determinism 指语义层面——spec 若允许多种行为即"非确定"。1.0 唯一的非确定来源是浮点 NaN 位模式（IEEE 未定义 NaN 位模式、硬件厂商互不一致）；曾尝试强制归一化 NaN 但"非常昂贵"而放弃——区块链实现恰恰会这么做。非确定性分类：threads 是"intentional non-determinism"，其余是"accidental non-determinism"、"越少越好"。（`00:43:19–00:46:15`）

### 与 JVM 对比

JVM 本质是"为 Java 设计的 VM"——"基本是 Java 的抽象语法"，内置完整 Java 对象模型（含反射）；与 Java 不够像的语言编译到 JVM 通常不会快。WASM GC 独有的是 tagged pointers 内置——GC 需知道什么是指针，运行时常用指针低位打标记表示 unbox 整数以避免装箱，WASM 直接内置该能力，"其他 VM 没有这个"；大量小分配的语言（许多函数式语言的特征）在 JVM 上不理想，闭包在 JVM 上也"非常昂贵"。（`00:47:21–00:50:04`）

### 未来方向：threads、stack switching 与形式化

core WASM 仍缺两大特性：threads（"接近终点线了, finally, I hope"）与 stack switching（建模为 delimited continuations）。stack switching 的重要性：使现代语言的各类控制抽象（async/await、generators、green threads）得以高效编译。提案核心来自学术界近 15-20 年的 effect handlers——异常处理器的推广，允许在抛出点之后任意时间 resume；关键优势是可组合、模块化。现有替代技术的问题：CPS 全程序变换"pretty expensive"；经 JavaScript 的 trampolining——这正是 3.0 之前 C++ 异常的实现方式（调进 JS 建异常处理器再调回 WASM，"crazy"），共同问题是"brittle and costly…not very modular"。（`00:50:26–00:55:11`）

形式化规格是他深度参与的部分：完全没有 undefined behavior；一切形式化、数学化规定并验证，有机器验证的证明。方法论主张：形式化与设计同步进行——"当形式化变得困难时，设计多半有问题"；形式化与实现一样是反哺设计的反馈回路。终极图景：已验证硬件、已验证引擎（WASM），若再有已验证编译器，"整个软件栈终将可验证"。LLM 时代的尾注：主持人提出在非确定机器生成代码的时代，事后确定性验证愈发重要；他认同但强调这是"open research area…very hard problem"，并转述当天读到的研究：结对编程中人们对人类伙伴处处质疑、对 AI 却不，尽管 AI "at least as failable"。（`00:57:17–01:00:55`）

## 来源与定位

- 原始节目：[WebAssembly 3.0 with Andreas Rossberg](https://softwareengineeringdaily.com/podcasts/webassembly-3-0-with-andreas-rossberg/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 起源与浏览器安全约束（00:01:50–00:05:38）
  - 1.0/2.0、基准测试心理阴影（00:05:50–00:12:50）
  - GC 的 opt-in 设计与 pay-as-you-go（00:13:17–00:16:59）
  - MVP 方法论与 SIMD 遗憾（00:18:36–00:22:23）
  - 标准制定过程（00:22:49–00:26:15）
  - WASM vs JS 选型与 DOM 反直觉判断（00:27:55–00:33:22）
  - 语言互操作公理与 component model（00:33:39–00:39:17）
  - 非 Web 用例与确定性分类（00:39:46–00:46:15）
  - 与 JVM 对比、tagged pointers（00:47:21–00:50:04）
  - threads、effect handlers 与形式化方法论（00:50:26–01:00:55）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。逐字稿个别术语有转写误差（emscript、Exactions、Threats 等），已按上下文校正。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 版本时间、性能倍数与提案状态为受访者口径（多处自述记不清），未独立验证；Relaxed SIMD、GC 争议等为受访者个人立场。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
