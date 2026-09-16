---
item_id: software-engineering-radio-dc43913a4d4b
title: iced 作者谈 Rust GUI：Elm 架构、一个按钮的绘制之旅，与"能用文档写清楚就说明库设计对了"
date: '2026-09-17'
published_at: '2026-03-25'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/03/se-radio-713-hector-ramon-jimenez-on-building-a-gui-library-in-rust/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/03/se-radio-713-hector-ramon-jimenez-on-building-a-gui-library-in-rust/'
summary: 'iced GUI 库作者 Héctor Ramón Jiménez 讲述 Rust GUI 全景：Elm Architecture 的消息化状态管理、winit/wgpu/tiny-skia 组件栈、借用检查器如何塑造任务系统，以及 v0.14 的 reactive rendering、Comet 时间旅行调试与端到端测试愿景。'
tags: [Rust, 架构, 开源]
---

# iced 作者谈 Rust GUI：Elm 架构、一个按钮的绘制之旅，与"能用文档写清楚就说明库设计对了"

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-03-25 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 7267 字 · 阅读约 19 分钟
>
> 标签：[Rust](/tags/Rust/) [架构](/tags/%E6%9E%B6%E6%9E%84/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/03/se-radio-713-hector-ramon-jimenez-on-building-a-gui-library-in-rust/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/03/se-radio-713-hector-ramon-jimenez-on-building-a-gui-library-in-rust/)

## 速读

iced——GitHub 约 3 万星、Rust 生态最流行的 GUI 工具箱之一——的诞生纯属"两次跑偏":想做游戏,写了个叫 Coffee 的游戏库,又因为想用 Elm 架构写 UI,拆出了一个独立库。作者 Héctor Ramón Jiménez 与主持人 Gavin Henry 从起源讲到 v0.14 的测试体系:窗口归 winit、绘图归 wgpu、无 GPU 环境靠 tiny-skia;按钮从描述到点亮屏幕要经过布局、渲染记录、GPU 着色的完整旅程;而借用检查器反过来塑造了整个架构。

最值得带走的三点:Elm Architecture 把全部状态变更集中到一处,消息驱动的架构让"时间旅行调试"成为可能(Comet 工具按消息重放出任意历史状态);Rust 的借用检查器不只是防内存错误——它强制框架在状态变更后重新调用视图,这是库正确性的编译期保证;v0.14 的 reactive rendering 让组件自己触发重绘,告别"鼠标一动全屏重画"。

## 主题正文

### 起源:想做游戏,两次跑偏,长出了一个 GUI 库

iced 的诞生史是"两连跑偏"。2019 年 Héctor 想做游戏,选了 Rust(当年 Rust 游戏生态还很简陋,现有图形库不入他的眼),索性自己写了个游戏库,取名 Coffee;后来游戏需要一个 UI,他给库加了个 UI 模块——此前他做 Web 开发、用过 Elm,便尝试"把 Elm 的精神带进 Rust";再后来有人建议把这个小模块独立成库,"也许你不想做游戏,只想做个 UI 应用"——iced 就此诞生。最初的 alpha 版连渲染器都没有,只有布局和窗口管理逻辑,"拉下来还得自己写全部绘制代码"。名字也随意:游戏库叫 Coffee,那这个就叫 iced,"我就是喜欢冰咖啡,没有更深的含义"。（原文锚点：`it happened as I got sidetracked from one project to another, kind of like iced happened as two sidetracks in a row`；`I just called it iced because I don’t know, I just like iced coffee`）

### Elm Architecture:状态、更新、视图与消息

渲染器定义清楚:把 UI 的布局与状态(按钮、文字、颜色)真正画到窗口的像素上。而 iced 的灵魂是 Elm Architecture——把应用强制拆成边界清晰的三部分:状态(state)、更新逻辑(update)与视图逻辑(view),外加贯穿其间的消息(message)。待办事项的例子:状态是字符串列表加完成与否的布尔;视图逻辑把状态变成 UI 描述;关键在于没有回调——按钮不会持有"点我之后改那个"的处理器,而是产生一条消息,消息喂给更新逻辑,"所有状态变更集中在一个地方"。他的入坑动机是前端之痛:当年用 Angular,重构极其痛苦、运行时错误遍地,"我清晰地记得自己在 Google 搜 JavaScript without runtime errors",第一个结果就是 Elm;两周内把整个应用重写为 Elm,"如释重负",于是想把这套架构带回 Rust。主持人(正用 iced 给儿子做辅助沟通应用)补充了使用者视角:加新功能时"不用思考架构",接一条消息、在处理处行动即可,一周后回来依然一目了然。视图逻辑还带来灵活性:一条消息可以改变整个 UI,从一个屏幕跳到另一个,"不需要告诉框架每一步怎么做,你只描述新的 UI,iced 搞定剩下的"。（原文锚点：`all the state mutation centralized in a single place`；`searching on Google JavaScript without runtime errors`；`one message can potentially change the entire UI`）

### Rust 之选、生态对照与"多样性让社区更强"

从 Elm/Haskell 转到原生平台,他选 Rust 因为它是"最成熟、最现代的选择,不会让你感觉退回石器时代";C/C++ 连像样的枚举都没有,"用 Rust 写过 enum 和 union type 之后就真的回不去了"。对比生态:egui 是即时模式(把更新与视图逻辑混在一起),更适合游戏与快速集成;iced 的 Elm 架构则在复杂应用的条理性上更占优——但"归根结底是偏好,多样性是好事,每个社区不必把想法不同的人硬塞在一起"。与 React 的渊源也被点到:React 的 state+view 哲学类似但没有消息这一环,Redux 则是把消息与更新逻辑带给 React 的尝试。（原文锚点：`they don’t even have a proper way to describe Enums`；`I think the main selling point is the Elm Architecture`；`having diversity and different choices is always good`）

### 核心组件与"一个按钮的绘制之旅"

iced 站在两个巨人肩上:winit 负责跨平台建窗("窗口管理是疯狂的活儿"——Windows、macOS 之外,Linux 有 X11 与 Wayland,后者还只是协议、上面各有 compositor 与扩展),wgpu 则是 WebGPU 标准的原生实现,抽象 Vulkan、Metal、DirectX 12 为统一绘图 API;没有 GPU 的环境(虚拟机、嵌入式)退回 tiny-skia 软件渲染(Rust 化的 Skia 子集),未来或迁往采用全新思路的 Vello CPU。一个按钮的旅程被他讲成了教科书:winit 开窗并拿到 surface(允许绘制的屏幕区域)→ wgpu 建渲染器与纹理 → 启动 Elm 循环,boot 函数创建初始状态 → 视图函数把状态变成元素(element,可嵌套的 UI 描述)→ 布局逻辑递归算出各元素的位置与尺寸 → 渲染器依据布局与状态(悬停/按下时换色)记录 wgpu 命令,转为三角形几何交给 GPU,着色器在纹理上完成绘制 → present 上屏。而用户只需关心两件事:状态到元素描述的视图逻辑,以及交互发生时如何变更状态。Rust 在这里的妙处:"借用检查器在编译期强制我们在状态变更后重新调用视图——不先放下旧的控件树,就无法调用你的更新逻辑",库的正确性由编译器保证。（原文锚点：`it abstracts over the different graphics APIs like Vulkan, Metal, DirectX 12`；`a surface is like the actual region on screen that you are allowed to draw into`；`the borrow checker forces you statically at compilation time to call view logic`）

### 借用检查器塑造的任务系统,与组件化的权衡

为什么长任务(比如按钮触发下载)不能直接写在更新逻辑里?因为更新跑在主线程、可以变更状态,在那里下载会阻塞整个 UI——用户看到的将是转圈(主持人补刀:Linux 上还会弹"应用已冻结,强制退出或等待")。而视图逻辑被允许直接借用应用状态(长列表不用克隆就能高效展示),代价是展示期间不允许变更——这正是任务系统的由来:更新逻辑返回一个"任务",它什么也不执行,只是对未来动作的描述,运行时放到别的线程跑,完成后产生一条新消息回到更新循环。状态本身不神秘:通常是个 struct,常见模式是用枚举区分"加载中/已加载"。他自嘲对"设计模式"一词有 PTSD——OOP 年代把依赖注入、观察者模式用到到处都是,"制造了很多混乱";iced 生态里自然浮现的有加载枚举与组件模式(把消息嵌套成子消息,做出可复用的迷你 Elm 架构),但组件化意味着状态同时被切分——确定这块状态不需要被应用其他部分访问,否则会掉进多组件同步的坑。（原文锚点：`if you do the download there, you’re going to block the entire UI`；`the task system is just update logic can return... a future in Rust`；`ended up creating a lot of chaos`）

### 冷门宝藏与"文档写得顺,说明库设计对了"

被低估的部分:shader 组件(3D 演示的来源,已有图表库依赖它)、以及 sensor 组件——当控件进入或离开视野时发出通知,做无限滚动列表的利器;主持人现场分享了自己给儿子应用里 4000 个 SVG 符号选择器做分页加载的实践。文档则是他呼吁更多 appreciation 的部分:"没真正维护过开源项目的文档,你不知道光画那些讲解图就要花多少功夫;而且写文档本身就是对库的测试——如果你能把它简单地解释清楚,说明这个库大概率是易用的;如果写不下去,那你就有麻烦了。"（原文锚点：`there’s a sensor widget that you can use to be notified when certain things are displayed or hidden from view`；`if you can do it, it means that probably the library is easy to use`）

### v0.14:reactive rendering、Comet 时间旅行与端到端测试愿景

v0.14 的主亮点是响应式渲染:此前 iced 几乎时刻重绘——"鼠标每动一下,整个应用完整重画一次";现在组件知道自己何时被交互,自己触发重绘,不再悲观地全量重画。另一个落地的多年心愿是时间旅行:Elm 架构的消息驱动意味着"从初始状态重放全部消息,就能重建应用在任意时刻的状态"——配套的姊妹应用 Comet(F12 唤出)可以回溯应用自启动以来的任意历史帧,调试动画时能看到每一帧。测试则是 v0.14 起的重头戏。headless 模式让应用在没有窗口、没有 winit、甚至没有渲染器的环境中运行——"应用不知道自己没在显示",因为 Elm 架构部分(update/message/view)与实际的窗口和绘制是解耦的,插上真渲染还是插上"假装在显示"的东西由运行时决定。在此基础上是"一等公民的端到端测试"愿景:用一门小 DSL 描述用户交互——"点击这个按钮,然后检查这段文字出现了"。测试录制器把你与应用的交互记录下来,但不存坐标——存的是"点击包含这段文字的那个控件"这类可稳定定位的指令(坐标在布局变化后就会失灵),鼠标移动也会被合并成最终位置;运行时模拟器则在 headless 沙箱里回放这些测试;program presets 允许预置初始状态("一个已登录的新用户停在这个屏幕"),iced test syntax 就是录制产物——一份极简的指令列表,精神上与 Selenium、Gherkin 一脉相承。整个测试体系是他为自己公司新招的 QA 工程师打造的:"目标是让他们能用它重重地测试我们的 iced 应用。"(尚未完全就绪)（原文锚点：`the widgets now know when they’re being interacted with and they’re triggering the redraws themselves`；`recreate the state of the app at any point in time`；`it’s as if it’s being displayed. The app doesn’t know that it’s not`；`instead of clicking in this coordinates, we say click this, the widget that contains this text`）

### 版本哲学、无障碍的未来与"专注桌面"

版本号 0.x 是有意为之的沟通:"这是实验性软件、我的宠物项目,目前不附带任何稳定性承诺";等真正到 1.0,他要能说"这基本实现了 iced 的完整愿景"。v0.15 已加入文本省略号,主攻方向是无障碍:支持屏幕阅读器、接入各平台无障碍 API(计划借助跨平台的 Access Kit crate),System76 在其 iced 分支上为 COSMIC 桌面实现过无障碍可作灵感,随之而来的还有集中的焦点管理与键盘导航。System76 的 COSMIC(Pop!_OS 新桌面)采用 iced 分支本身就是"一个大大的背书",他们贡献的 cosmic-text 文本布局库更是改变了 Rust 生态——"我起步时这块什么都没有,只能依赖 C++ 或系统 API"。iced 将坚持只做桌面:他无法承诺维护移动端(没有自己的用例、难以正确测试),且"用一套统一 API 同时服务好移动与桌面是不可能的"——移动端要电池与性能,而 Elm 架构的重绘特性并不契合,未来或许有增量渲染,但"再叠加 iOS 和 Android 会非常疯狂"。国际化则可以在库之上用 fluent 之类的方案解决,他需要被说服它值得一等公民支持。收尾的推荐:iced.rs 的展示页,Pop!_OS 的 COSMIC,以及 Halloy——"一个很棒的极简 IRC 客户端;既然 Discord 全面进入监控模式,IRC 正在回潮"。（原文锚点：`it’s a bit about messaging and communicating the state that the library is in`；`accessibility is the main thing that I want to look into`；`I think that’s a big stamp of approval`；`IRC is making a comeback`）

## 来源与定位

- 原始节目：[SE Radio 713: Héctor Ramón Jiménez on Building a GUI Library in Rust](https://se-radio.net/2026/03/se-radio-713-hector-ramon-jimenez-on-building-a-gui-library-in-rust/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 两次跑偏的起源、Coffee 游戏库与 iced 之名（`iced happened as two sidetracks in a row`；`I just called it iced because I don’t know, I just like iced coffee`）
  - Elm Architecture：状态/更新/视图与集中式状态变更（`all the state mutation centralized in a single place`；`one message can potentially change the entire UI`）
  - Angular 之痛与"JavaScript without runtime errors"的搜索（`searching on Google JavaScript without runtime errors`）
  - Rust 之选与枚举论证（`they don’t even have a proper way to describe Enums`）
  - winit/wgpu/tiny-skia 组件栈与窗口管理的疯狂（`windowing is craziness`；`it abstracts over the different graphics APIs like Vulkan, Metal, DirectX 12`）
  - 一个按钮的绘制旅程：surface→element→layout→wgpu 命令→着色器（`it starts the Elm Architecture loop`；`shaders are like little programs that the GPU can run`）
  - 借用检查器强制视图重调与任务系统（`the borrow checker forces you statically at compilation time to call view logic`；`the task system is just update logic can return`）
  - 组件模式与状态切分的权衡（`ended up creating a lot of chaos`）
  - sensor 组件、shader 组件与文档的价值（`there’s a sensor widget`；`if you can do it, it means that probably the library is easy to use`）
  - v0.14 reactive rendering、Comet 时间旅行（`the widgets now know when they’re being interacted with`；`recreate the state of the app at any point in time`）
  - headless 模式与一等公民端到端测试（`it’s as if it’s being displayed. The app doesn’t know that it’s not`；`instead of clicking in this coordinates, we say click this, the widget that contains this text`）
  - 0.x 版本哲学、无障碍路线与 COSMIC/System76（`it’s a bit about messaging and communicating the state that the library is in`；`accessibility is the main thing that I want to look into`）
  - 桌面专注论与 Halloy/IRC 收尾（`I plan on keeping iced desktop only`；`IRC is making a comeback`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 嘉宾姓名（Héctor Ramón Jiménez）与主持人（Gavin Henry）按节目出版方元数据核正；iced 约 3 万 GitHub 星、System76/COSMIC 采用等均为节目口述口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
