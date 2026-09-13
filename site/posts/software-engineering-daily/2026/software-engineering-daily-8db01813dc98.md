---
item_id: software-engineering-daily-8db01813dc98
title: 'Web 原生游戏复兴：Poki 的竖屏优先、即时上手与文件体积经济学'
date: '2026-09-13'
published_at: '2026-06-04'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/web-native-game-development/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/05/SED1934-Erik-Dubbelboer.txt'
summary: 'Poki 首席工程师 Erik Dubbelboer 讲 Web 游戏复兴：WebGPU 与 Wasm 的技术栈、竖屏优先与"最初几秒"抓眼球、文件体积直接决定留存。'
tags: [开发者工具, 产品指标]
---

# Web 原生游戏复兴：Poki 的竖屏优先、即时上手与文件体积经济学

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-06-04 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 5094 字 · 阅读约 13 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [产品指标](/tags/%E4%BA%A7%E5%93%81%E6%8C%87%E6%A0%87/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/web-native-game-development/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/05/SED1934-Erik-Dubbelboer.txt)

## 速读

Software Engineering Daily 邀请 Poki 首席工程师 Erik Dubbelboer（Silly Skies、Village Builder 作者），讲 Web 原生游戏开发的现状。Poki 是最大的 Web 游戏平台之一、服务超过 1 亿月活用户。这期的价值在于把"Web 游戏"从技术名词讲成一套完整的产品逻辑：WebAssembly/WebGPU 让浏览器游戏接近原生性能，而 Web 玩家的行为特征（无下载投入、几秒内离开）反过来塑造了竖屏优先、即时上手、文件体积控制的开发原则。

最值得记住的三个具体结论：WebGPU 已被 68% 的玩家支持（Poki Player Device Report），引擎从 WebGL 迁移后骨骼动画与粒子显著变快；"每多 1 MB 下载量，就会损失几个百分点的玩家"，这是 Unity 大 blob 方案在 Web 上吃亏的根源；以及 Poki 的玩法测试（10-20 个真实玩家、几分钟拿到试玩视频）如何支撑快速迭代。文中有几处受访者自述不确定的数据。

## 主题正文

### 从 Half-Life bot 到 Poki：为什么 Web 游戏会复兴

Erik 约 16 岁开始对游戏开发感兴趣，编程入门是给《Half-Life》第一代写 C++ 机器人 bot，因逻辑缺陷反而产生意外的"涌现行为"而觉得有趣；大学软件工程第一天失望于"同学们连指针是什么都不知道"，此后多年没做游戏。他曾与朋友用 Unreal Engine 做独立游戏上架 Steam 页面，但最终放弃。一个重要判断：Steam 纯多人游戏"永远不会成功"——若首发没有足够大受众做匹配，即使每天有 1000 玩家、但分散在不同时段，也开不了局、玩家会流失。约七年前他加入 Poki，先做后端工程师，后与同一朋友在 Poki 发布两款自家游戏（"dog food"）。他的背景让"Web 游戏复兴"的判断格外可信。（`00:01:46–00:07:01`）

历史脉络：iPhone"杀死 Flash"，大量 Flash 游戏丢失、经验流失；少数公司做 Flash→Web 转译回收了一部分。常有开发者怀念 Flash 时代，但 Erik 判断"那不会回来"，即使重推，观众期望已变。Unreal 曾支持 Web 导出但移除了，因为"太难与正常渲染管线保持同步"。真正带回复兴的是 WebAssembly（及 OpenGL）：Unity、Godot 等几乎所有引擎都用 Emscripten 编译到 WebAssembly；现在有 WebGL、WebGL2，WebGPU"让更多成为可能"。（`00:07:01–00:10:15`）

### WebAssembly 与 WebGPU：技术基础

WebAssembly 的动机：JavaScript 需经"文本→字节码→中间层→机器码"且运行时不断重优化、不完美；游戏引擎代码量大、需要更快更小。WebAssembly 几乎直接就是中间层/接近机器指令，翻译开销极小，通常比同等 JS 快；有静态缓冲数组堆内存、指令集很有限。Emscripten 是 C++→WebAssembly 的编译器后端。一个重要澄清：Wasm 没有浏览器 API 访问权，要建 DOM 节点必须经 JS 中转；曾讨论过让 Wasm 直接调用 DOM 的规范但"至今未实现"，原因之一是 Wasm 也被用于其他安全执行环境、只有你定义的接口能通向外界。（`00:10:34–00:14:15`）

WebGL 是 OpenGL 的 Web 包装，可向 canvas 绘制 3D 图元；WebGPU 可比作 Web 版 Vulkan。技术对比：OpenGL/WebGL 是"发出命令→按序执行→等待结果"，WebGPU/Vulkan 是"先批量排队命令再一次性提交给 GPU、不等结果"，省等待时间、快得多，但 API 复杂得多。引擎接入 WebGPU 也不容易，因为渲染管线差异大、需要改造。（`00:14:34–00:16:55`）

引擎现状：Unity 使用最广（尤其手游），Unity 与 Godot 都有成熟的 Web 导出；Web 原生引擎谱系从 PlayCanvas（像 Unity 但 Web 原生、纯 JS、不编译 Wasm、有点击式编辑器）到 Cocos（中国引擎）、Construct、Phaser（基于 PixiJS），PixiJS 更像框架而非引擎。大部分 Unity 内容都能在 Web 上用、"超级简单"，但 Erik 坦诚"不知道 Unity 编辑器具体哪些特性不支持 Web 导出"。Unity 近几个版本有实验性 WebGPU 导出；WebGPU 在浏览器中更稳定"也就最近几个月"。关键性能点：桌面端骨骼网格动画用 compute shaders 在 GPU 上算，WebGL 没有 compute shader（只有渲染 shader）、WebGPU 有——所以大量动画时骨骼网格在 WebGPU 上"快得多"，粒子效果也更快。（`00:17:19–00:21:25`）

### 浏览器支持与 WebGPU 覆盖率

WebGL 在很老的 Android 手机上也可用；WebAssembly"到处都支持"，仅部分新指令可能不支持，但可以运行时检测并做条件代码。WebGPU 需要显卡驱动支持，很多老手机不支持；Chrome 正做"极简版 WebGPU"用降级方式在老手机上运行；Safari 直到最近约半年（某个最新 iOS 版本）才可用，Erik 不确定 Safari 移动端是否已默认启用；Firefox 仍在做但默认未启用。Poki 的 Player Device Report 显示 WebGPU 已被 68% 的玩家支持。他预测可能 2026 年底前 WebGPU 普及到几乎人人都有（带不确定性）。（`00:21:47–00:23:57`）

### Poki 平台与开发模式

Poki 是最大的 Web 游戏平台，Flash 时代就以别的名字存在。Flash 濒死时其他站点纷纷转做移动，Poki 创始人反其道专注 HTML5 游戏（JS/canvas/WebGL），"这真的获得了回报"——其他网站难以为继而消失，Poki 活了下来。现有约 1 亿月活用户，Erik 估测"大概排全球前 50 网站"（不确定）。三方平台模式：玩家 + 开发者 + 广告商；Poki 做策展（"非常精选，不是谁都能发布"）、广告、屏蔽恶意内容，并与开发者收入分成。Poki for Developers 平台：提交 zip（含 index.html + 资源）→ 托管到 Poki CDN，有洞察数据、账单、版本管理；支持联网多人游戏，但 Poki 不托管多人游戏后端，交给开发者自管。（`00:24:04–00:27:32`）

Erik 做自家游戏的动机是"dog food"：从开发者视角审视 Poki for Developers，发现 UI 低效问题；用自己的游戏测试新特性、不怕弄坏。他还提到一个个人选择："这些天我本可以用 AI 做美术，但我不愿意。"（`00:27:45–00:30:22`）

### 竖屏优先、即时上手与 Web 玩家行为

Poki 现在"移动优先"，因为移动玩家增长很多；Web 游戏最佳实践是做竖屏（portrait）——Web 上玩家换游戏频繁，"不想让玩家不断旋转手机"。不同手机刘海/挖孔遮挡 UI 是痛点，引擎的动态 UI 缩放方案与 Poki 的 inspector 工具可缓解；他补充 Netflix 视频也在改竖屏、Instagram/YouTube Shorts 全是竖屏，竖屏在移动端全面胜出。（`00:30:55–00:35:25`）

Web 玩家行为的关键差异：Web 玩家没有"下载投入"，不喜欢立刻点走；App 玩家已付出下载成本、有动力多试一会。因此 Web 上文字 onboarding 行不通，"必须在最初几秒抓住观众"；onboarding 应"不像教程"，自然逐个引入机制、不用读文字——他举例做 Web 版吸血鬼幸存者类游戏，会先给玩家最疯狂的能力约 10 秒展示上限，再收回、再快速重建。Web 开发周期短、易更新（无需下载新版本），Web 原生工作室先做好"前几分钟"再后续加内容。（`00:34:33–00:38:18`）

### Poki Play Testing 与获客优势

Poki Play Testing：上传新版本后请求测试，随机匹配 10-20 个真实玩家试玩，用 canvas captureStream API 录制视频，"几分钟内拿到 10 个试玩视频"；一天可上传多版本反复请求测试。为什么不用朋友/家人：不是目标受众、会客气不说差；且同一人第二次玩就已完成 onboarding，"onboarding 无法在同一人身上测第二次"——而 onboarding 正是 Web 游戏最重要的部分。案例：一个横版自行车游戏要按空格翻转，测试视频里年轻玩家"不知道空格键是什么"，各种乱按键；这类反馈在 Steam/App Store 的专业测试（知道空格键是什么、不是目标受众）中拿不到。（`00:38:31–00:42:14`）

获客上，Steam/App Store 不做推广，开发者不做营销就没人玩；App 商店"每天有超过 100 款游戏发布"。Poki 用游戏页旁边展示其他游戏做交叉推广，等于替开发者完成全部用户获取；"想做成成功的 App/Steam 游戏，至少一半时间要花在获客上；在 Poki 则 100% 时间都花在开发和改进游戏上"，也因此产出更好的游戏。（`00:43:08–00:44:58`）

### 账户系统、云端存档与文件体积经济学

Poki 账户系统约去年年底（2025 年底）推出，用 cookie 与游戏分类可定向投放测试受众；未登录玩满一小时后会提示注册；存档默认存 localStorage，Poki 会"定期读 localStorage 同步到服务器"，开发者无需实现专属 API。技术细节：游戏跑在与主站不同域的 iframe 里以保护 cookie；Safari 智能防追踪"很有名地丢弃 cookie"，尤其移动端，Erik 见过"Safari 移动端在我们游玩途中就删掉 localStorage 条目"的极端案例。（`00:45:32–00:47:44`）

最值得开发者记住的经济学：Web 分享 API 仍很受限（navigator.share 只能调起系统分享菜单，"不能从 Web 直接把内容推给 Instagram app"）；而"每多 1 MB 下载量，就会损失几个百分点的玩家"——要让玩家以最少字节进入游戏/菜单。Web 原生引擎（PlayCanvas 等）易做延迟加载（先加载第 1 关、后续关卡后载）；Unity 的劣势是 WebAssembly 单一 blob、必须整包下载才能开始执行，多数 Unity 游戏不用 addressables、把全部资源载入内存后才可玩，"转换到可玩的转化率总是更低"；后期再引入 addressables 很难，他希望 Unity 改进。Godot 同样是大 blob，其 Web 负责人正在做"稍后加载"系统，"这会大幅提升 Godot 的吸引力"。Wasm 侧可能仍是单一 blob，但关卡/资源作为数据可以后加载。（`00:47:59–00:51:44`）

## 来源与定位

- 原始节目：[Web Native Game Development](https://softwareengineeringdaily.com/podcasts/web-native-game-development/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 嘉宾背景与 Steam 纯多人判断（00:01:46–00:07:01）
  - Flash 消亡、Wasm 复兴（00:07:01–00:10:15）
  - WebAssembly 原理与 DOM 澄清（00:10:34–00:14:15）
  - WebGL vs WebGPU（00:14:34–00:16:55）
  - 引擎谱系与 WebGPU 导出（00:17:19–00:21:25）
  - 浏览器支持与 68% 覆盖率（00:21:47–00:23:57）
  - Poki 平台模式与开发流程（00:24:04–00:27:32）
  - dog food 与自有游戏（00:27:45–00:30:22）
  - 竖屏优先与移动玩家（00:30:55–00:35:25）
  - Web 玩家行为与最初几秒（00:34:33–00:38:18）
  - Poki Play Testing（00:38:31–00:42:14）
  - 获客与分发优势（00:43:08–00:44:58）
  - 账户系统与 localStorage 同步（00:45:32–00:47:44）
  - 文件体积经济学与 Unity blob 问题（00:47:59–00:51:44）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 用户数、覆盖率、下载量与转化率等数字均为受访者口径，未作独立验证；受访者自述记不清的数据已尽量标注。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
