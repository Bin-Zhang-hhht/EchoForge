---
item_id: software-engineering-radio-426ae4277d12
title: Will Sentance 谈 JavaScript 现代化："不破坏 Web"的代价、单态形状，与两层抽象下的手艺
date: '2026-09-17'
published_at: '2026-04-29'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/04/se-radio-718-will-sentance-on-js-modernization/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/04/se-radio-718-will-sentance-on-js-modernization/'
summary: 'Codesmith 联创 Will Sentance 谈 JavaScript 现代化："不破坏 Web"约束如何催生 Symbol 与 SmooshGate、V8 单态形状优化、语法糖的危险,以及 AI 时代工程师的两层抽象——运行时底层理解与系统级 agent 编排,缺一不可。'
tags: [JavaScript, 软件工程, 性能]
---

# Will Sentance 谈 JavaScript 现代化："不破坏 Web"的代价、单态形状，与两层抽象下的手艺

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-04-29 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6193 字 · 阅读约 16 分钟
>
> 标签：[JavaScript](/tags/JavaScript/) [软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) [性能](/tags/%E6%80%A7%E8%83%BD/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/04/se-radio-718-will-sentance-on-js-modernization/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/04/se-radio-718-will-sentance-on-js-modernization/)

## 速读

Codesmith 联合创始人、《The Hard Parts of JavaScript》课程作者 Will Sentance 与主持人 Adi Narayan 回顾 JavaScript 的现代化:这门 1995 年十天写成的脚本语言,在"不破坏 Web"的宪法性约束下如何演化——SmooshGate 的妥协、Symbol 原语的诞生、user-land 作为 TC39 的过滤系统。

最值得带走的三点:V8 的即时编译器只为"单态形状"优化,运行中途给对象加属性会打破蓝图、切回慢速通道;TC39 把社区库当作研发过滤系统,证明了的通用需求才会被吸收(Temporal 即将终结 moment.js);而 AI 时代的工程师需要同时在两层抽象下工作——运行时的底层机制与系统级的 agent 编排,任何一层没有底层理解都会"盲飞"。

## 主题正文

### 简史与"不破坏 Web":SmooshGate 与 Symbol 的诞生

Sentance 的 JS 史从 1995 年"十天写成"讲起:Java applet 与 Flash 之外的轻量交互脚本,直到 Google Maps 与 2004 年 Netvibes 的可拖拽主页让人们意识到浏览器的潜力。此后的演化是两股力量的合力:TC39 委员会对社区需求的响应,以及浏览器厂商在架构底层的持续进化;还要分清 JavaScript 本身与浏览器 API(fetch、摄像头、localStorage 属于后者,并非 Ecma 委员会的产品)。这门语言的宪法是"追加式演化":Python 或 Java 可以在某个版本废弃旧特性,而运行在浏览器里的 JavaScript 必须在合理范围内向后兼容到 1995 年。（原文锚点：`needs to be backwards compatible within reason all the way back to 1995`）

这个约束最著名的战例是 2018 年的 SmooshGate:社区渴望内建的数组扁平化方法,但古老的 MooTools 库仍在原型上占用着 flatten 属性,语言原生方法一旦加入就会破坏数千个应用——委员会甚至讨论过把方法命名为 smoosh。最终妥协为 flat。Symbol 原语则是同一约束的产物:为内核新增对象属性可能与既有库或用户自定义属性撞名(比如遍历对象公开属性的代码会突然多显示一堆东西),Symbol 让新特性"只能通过特定入口访问",行为的改变必须经过开发者的显式选择。（原文锚点：`it would now be overridden if a flatten method was added at the language primitive level`；`there was a mood tools library`；`designed essentially as a workaround for not adding new properties to objects`）

### 吸收 user-land 的过滤系统,与 await 的陷阱

TC39 把社区生态当作研发过滤系统:"让它在 user-land 里先打出来,证明是普遍需求后我们再吸收"。JS 标准库之薄是有名的——深拷贝长期靠 JSON.parse/stringify 的性能损耗来凑合,直到 structuredClone 出现;时间处理上 moment.js 过重,内建的 Temporal(计划 2026 年)将是"不可谈判"的替换理由。2015 年起的年度发布节奏也终结了此前"等太久"的问题。开发者对性能升级类特性(structuredClone、Temporal)确实 eager,但他同时泼冷水:真实代码库中更大的性能杀手往往在别处——他举例某体育数据公司的 API,请求"单个球员"却返回整队历史、整季比赛与全部交互数据,"修复 fetch 的压力远大于从 Lodash 切到原生方法"。await 则是"被采纳最广的新特性",因为它把控制流还原成线性的样子;但这个诱人的抽象掩盖了真实执行:async 函数里的 await 并不会阻塞外层代码——不理解事件循环的人会在这里踩坑。（原文锚点：`a filtration system`；`structured clone`；`does not reflect the actual execution pattern`）

### 语法糖的危险:new 关键字与原型链

JavaScript 的灵活性有其历史根源:定位是给"想着页面像素的人"加一点动态的脚本语言,而且运行环境——各浏览器实现不一的 DOM 与网络接口——充满异构性,自动类型强转本是出于好意。但"语法糖是危险的,它会制造一种人工的理解感":OOP 就是最大的例子——class、new 这些关键词看起来与原生面向对象语言一模一样,底下的机制却是原型链而非类继承;不用 new 调用构造函数,属性会全部挂到全局对象上。他引用 Google 面试工程师的最爱问题:"new 关键字在底层到底做了什么?"——连同"闭包是如何工作的",这是检验你是否真正理解这套系统的试金石。他的核心论点一以贯之:不理解底层机制时,灵活性是诅咒;理解之后,灵活性是资产——同一个 JS 既能模拟面向对象,也能一路实现到 monad 的函数式特性。（原文锚点：`syntactic sugar is really dangerous because it can create this artificial sense of understanding`；`what’s the new keyword doing under the hood`；`only once you have a clear mental model`）

### 引擎、单态形状与"给引擎写提示"

"引擎"这个词很难精确定义:它不是整个浏览器,V8 既是 Chrome 的一部分也能独立驱动 node 与 Bun;而且引擎与宿主共同演化——从 XMLHttpRequest 到 fetch 的迁移就是浏览器特性与 V8 团队协作的产物。对资深工程师冲击最大的是 JIT 编译器的最新取向:只为"单态形状"(monomorphic shapes)优化——对象在生命周期中保持同一形状,执行中途添加属性会打破 JIT 构建的内部蓝图,访问从快轨切回慢轨。因此 V8 团队给出的主要建议是:定义对象时就声明全部属性(哪怕是 null),之后不要动态增删;更新鲜的是可以元编程式地用注释给引擎传递优化提示——"开发者显式指导引擎"正在取代"引擎挽救糟糕代码"的旧范式。Symbol 的元编程能力同样给了库作者权力:从给日志写出更好的对象描述,到手动改写迭代器的行为。他观察到 TC39 的关注点正悄然转移:很多人写的是 React,"React 是最后一个框架吗?"——TC39 的部分新特性与其说服务大众开发者,不如说服务于 React、TypeScript、Bun 这些"几乎成了标准库的抽象层"的建造者,而库作者的核心约束与 JS 一样:"别破坏使用我们库的代码库"。（原文锚点：`the engine now optimizes for what’s called monomorphic shapes`；`consistent monomorphic objects`；`is React the last framework`）

### LLM、两层抽象与 BBC iPlayer 案例

对"LLM 会不会加速迁移"的问答很平衡:最新模型对 React 这类近年的主流代码库已经很拿手(他引 Karpathy 对新模型能力的判断,并附上"仅限绿地项目"的限定),对私有内部模式与架构决策则无能为力;真正的风险不是模型强化了旧模式,"而是人们失去了深入底层的肌肉"。他提出的框架是工程师必须同时在两层抽象下工作:运行时层——理解每行代码真实的执行方式(事件循环、闭包让函数返回后内存仍然存续、垃圾收集机制,不理解就会内存泄漏,任何 agent 提示都救不了性能问题);系统层——跨多个运行时与网络设备编排 agent、写评测。他类比四十年前从手工内存管理到动态语言的过渡:当时的人也要同时思考两层。agent 层同样有"底层":上下文指针、内存、IO——Ralph 循环跑两小时突然退出,原因往往是 compaction 阶段把任务从上下文里裁掉了。两层都有底层理解,"你就能解决任何问题"。（原文锚点：`do they discourage, or people lose the muscle to go under the hood`；`under the hood on both`；`the compaction stage has cut the loop from your task`）

他最喜欢的故事印证了底层模型的价值:在 BBC 工程团队讲完异步编程的底层原理后,一位 iPlayer(英国的 Netflix,峰值 500 万并发,构建在 node 上)工程师来找他——团队长期搞不定多机环境下的队列顺序;而当 node 里五到七个不同优先级的异步队列(微任务队列、回调队列等)被逐一讲透,那位工程师当场对照代码库发现团队一直在用 setTimeout 当延迟技巧,而现在"可以从零正确实现我们想要的异步执行顺序"。治理数百万并发用户的代码库,被一个底层心智模型打开了优化空间。（原文锚点：`it has something like six, seven different queues for asynchronous function execution`）

### 重构 ROI、Bun 与"新抽象层上的手艺"

对大规模 JS 代码库重构的 ROI,他的排序是维护收益优先:换掉 moment 之类的"依赖定时炸弹"(Temporal 落地后尤其如此),收益不是那 60KB 的下载量,而是移除不可预测的第三方依赖;但要具体问题具体分析——如果团队已全面遵循 Lodash 模式,而 JS 并未提供 Lodash 的全部工具函数,那么"全员统一用 Lodash"可能比"一半原生一半 Lodash"的混搭维护成本更低。新项目则毫无疑问应该从 Temporal 这类原生特性起步。展望 2026,他兴奋的点还有:原生的对象克隆特性(structuredClone)出乎他的意料;React 在服务端与客户端渲染间走向更平衡的取向;以及 Bun——一个从零构建的完整 JS 运行时,自带包管理器、打包器与测试运行器,在 agentic 工作流里"可能比 Python 还易读";他即将开一门"从零构建 agent"的工作坊(从零实现一个 OpenClaw 式的实现)就选 Bun 当运行时。最后的展望把格局拉开:抽象层上移并不意味着底层手艺贬值——具身智能(embodied AI)与物理智能领域的关键工作流(VLA、模仿学习)恰恰是软件工程师熟悉的心智模型;他提醒听众,诺贝尔化学奖得主 Demis Hassabis 的第一份工作是游戏开发者。"底层推理与复杂系统的能力,将适用于我们过去不敢认为是软件工程领域的新天地——这是我个人的兴奋点所在。"（原文锚点：`it comes down to dependency time bombs`；`you might default to using Python. With BUN, you might actually get a more readable interface than you would with Python`；`the Nobel Prize for chemistry won by Sir Demis Hassabis a software engineer`）

## 来源与定位

- 原始节目：[SE Radio 718: Will Sentance on JS Modernization](https://se-radio.net/2026/04/se-radio-718-will-sentance-on-js-modernization/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - JS 简史、TC39 与"追加式演化"（`needs to be backwards compatible within reason all the way back to 1995`）
  - SmooshGate、MooTools 冲突与 flat 的妥协（`it would now be overridden if a flatten method was added at the language primitive level`；`there was a mood tools library`）
  - Symbol 作为反撞名原语（`designed essentially as a workaround for not adding new properties to objects`）
  - moment.js、Temporal 与薄标准库（`the JSON parse stringify step`；`a filtration system`）
  - await 的线性假象与执行真相（`does not reflect the actual execution pattern`）
  - 语法糖的危险、new 关键字与全局对象（`syntactic sugar is really dangerous because it can create this artificial sense of understanding`；`what’s the new keyword doing under the hood`）
  - 引擎与宿主的共同演化、JIT 单态形状（`the engine now optimizes for what’s called monomorphic shapes`；`consistent monomorphic objects`）
  - "React 是最后一个框架吗"与 TC39 服务库作者（`is React the last framework`）
  - LLM 的边界与"失去深入底层的肌肉"（`do they discourage, or people lose the muscle to go under the hood`）
  - 两层抽象、Ralph 循环与 compaction 裁剪（`under the hood on both`；`the compaction stage has cut the loop from your task`）
  - BBC iPlayer 的五百万并发与 node 队列（`it has something like six, seven different queues for asynchronous function execution`）
  - 重构 ROI：依赖定时炸弹优先、Lodash 的保留逻辑（`it comes down to dependency time bombs`）
  - Bun 运行时与具身智能展望（`you might default to using Python. With BUN, you might actually get a more readable interface than you would with Python`；`the Nobel Prize for chemistry won by Sir Demis Hassabis a software engineer`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 嘉宾姓名（Will Sentance）与主持人（Adi Narayan）按节目出版方元数据核正；ASR 的 "mood tools" 按公开史实校正为 MooTools，"Cloud Code" 校正为 Claude Code；Temporal 的发布时间以节目口述为准。
- "500 万并发用户"等数字均为嘉宾口述口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
