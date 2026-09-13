---
item_id: software-engineering-daily-03e46f886968
title: 'Mina the Hollower：Yacht Club 的自研引擎、位置学战斗与七轮 NG+'
date: '2026-09-13'
published_at: '2026-06-25'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/mina-the-hollower/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/06/SED1940-Mina-the-Hollower.txt'
summary: 'Yacht Club 首席程序员 David D''Angelo 详解 Mina the Hollower：自研 C++ 引擎 Propeller、GBC 自设限制、Castlevania 式位置学战斗与内置随机化的七轮 NG+。'
tags: [开发者工具, 产品指标]
---

# Mina the Hollower：Yacht Club 的自研引擎、位置学战斗与七轮 NG+

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-06-25 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 4249 字 · 阅读约 11 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [产品指标](/tags/%E4%BA%A7%E5%93%81%E6%8C%87%E6%A0%87/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/mina-the-hollower/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/06/SED1940-Mina-the-Hollower.txt)

## 速读

Software Engineering Daily 邀请 Yacht Club Games 首席程序员 David D'Angelo（主持为 Joe Nash），聊刚发售的《Mina the Hollower》——Shovel Knight 工作室对 Game Boy Color 时代的诠释（俯视角 Zelda 风动作 RPG）。这期对游戏开发者最有价值的是工程与设计两条线：自研 C++ 引擎 Propeller 的架构选择，以及"Castlevania 位置学战斗"的设计哲学。

最值得记的三点：GBC 风格是"假装的限制"（不真跑在真机约束上，但遵守调色板与 sprite 限色）；禁止斜向攻击让站位变得重要（Shovel Knight 测试期玩家的愤怒反而证明了这个设计）；以及内置 item shuffler 的七轮 New Game Plus。文中"开发六年"等数字出自主持人提问，受访者未确认。

## 主题正文

### 背景与 GB 风格的由来

David D'Angelo 的专业是计算机科学与音乐，毕业后写广告配乐，恰逢金融危机、工作室倒闭，转向游戏编程；申请 WayForward 后离开并共同创立 Yacht Club 做 Shovel Knight。他明确表示游戏原声的声誉"与我无关，全是 Jake，他是天才"，自己只负责音效置入与多音轨叠加；音乐背景的用处体现在把握游戏节奏一致性。Mina 定位为对 Game Boy Color 时代的诠释（Shovel Knight 是对 NES 的诠释）；GB 风格是意外——Alec 最初把 Mina 当业余项目练编程和美术，自评"只能驾驭 Game Boy 风格的美术"故定型。（`00:01:15–00:05:58`）

关于年代感与招聘：主持人给出"开发六年、GBC 发售 28 年"两个数字（出自提问、DD 未确认）。DD 说招聘时会问对方玩过什么游戏，但年代不是硬门槛——新程序员 Eli 二十多岁却最爱 Gargoyle's Quest；他也承认并非人人融入，程序员 Bridget 入职时喜欢的游戏不被认可、被反复安利后"我甚至不再喜欢那些游戏了"（半玩笑）。（`00:05:58–00:07:16`）

### 技术挑战：伪俯视与自研引擎 Propeller

技术上最怪的是"伪俯视"视角：渲染顺序、前后遮挡判定、两个战斗判定盒相撞时玩家是否"读得懂"。他坦白大型怪物占多少 3D 空间"是我们在编"，只能假设玩家会按一致规则自行推断；主持人确实在 boss 战中困惑过"离它背后多远"。开放世界无读盘、每个 screen 都存档；发售后本周正在紧急修复"玩家被存进奇怪位置"的 bug。除此之外整体实现"与 Shovel Knight 非常接近"。（`00:07:38–00:09:44`）

引擎名 Propeller，全部自研、全部 C++，负责渲染、输入/手柄、声音输出、文件处理；没有把 GBC 约束建进引擎——限制都在内容与设计层面。工具链包括调色板生成与调色板动画工具、美术导入/序列/动画/碰撞盒工具；其上还有"玩法引擎"（碰撞、动画、战斗等），新敌人复用既有系统。从 Shovel Knight 沿用的只有关卡编辑器和动画导入器，其余从零开始。引擎定位上，Shovel Knight 引擎是"一次性、赶紧出货"，这次目标是"做能长久用的东西"；他自评"不是世界上最新潮的引擎，风格像 90 年代"，比 Shovel Knight 风格"更好更强"，并希望"更有面向未来的韧性"。每台主机一个分支，实现渲染函数到该平台 API 的映射。视差按 2D 平面组织：每层带 parallax 值（随相机移动的百分比）。（`00:12:38–00:17:01`）

### "画纹理三角形，不画 sprite"

一个精彩的技术细节：旧主机 sprite 是固定尺寸、固定格式的绘制单位，不能画三角形；现代 API 的基本绘制单位是三角形——Mina 底层就是画带纹理的三角形。但组织方式模仿旧游戏：Mega Man 角色因头部与身体配色不同、且两 tile 高，需拆成两个 sprite；Mina 导入大图时同样拆头/身两个 draw box，每 box 画两个三角形。（`00:17:24–00:19:13`）

### GBC 美术：假装的限制

对标 Link's Awakening、Oracle of Ages/Seasons，也参考 Final Fantasy Adventure、Pokemon、Dragon Quest Monsters。他自述记不准 NES 调色板"大概 54 色"、颜色由任天堂指定不可改；GBC 可自选调色板但每 sprite 仍限色——团队逐个研究 GBC 游戏实际用色。自设限制是"假装的"：不真跑在真机约束上，但控制屏上 sprite 数量、遵守全局调色板、每 sprite 3 色；音乐用"非常先进的 GB 时代芯片"写，可能超出真机能力，但波形通道运作方式与真 GB 一致。克制现代表现：不做海量粒子特效、对话保持短小——他开玩笑说光游戏脚本字量"就会撑爆 Game Boy"。（`00:10:02–00:12:54`）

### 战斗哲学：Castlevania 位置学

DD 的目标是做"有点不同、有点没体验过的东西"，同时保证一致与公平。战斗主灵感是初代 NES Castlevania：以屏上位置为核心、动作 deliberate。他观察现代游戏（Souls、Zelda、Hades 等）"战斗循环基本相同"：攻击—将被打—按闪避脱身—再接近，"我们不想做那种"。老式 rigid 战斗式微的原因（他的观点）：太僵硬、不能实时响应输入——跳跃是固定弧线（约 30 帧，期间基本无法逃脱），玩家必须预判、规划攻击站位，而非临场反应。为不适应者留了装备路线：trinket "dodging pendulum"——被击中瞬间跳起可获得一段时间无敌，可"baby step"进入这种玩法。burrow 类似 Castlevania 的下蹲：分地面、地里、空中三层攻击；游戏前期钻地可躲一切，中后期出现砸地/地面攻击，迫使玩家改用跳跃。（`00:19:13–00:24:10`）

武器设计上禁止斜向攻击：若任何方向都能安全攻击，"位置就毫无意义"。Shovel Knight 先例：测试期只能下劈加侧劈，敌人从上方飞来时玩家非常愤怒"我想往上打"；团队立场是若能往上打"就不有趣了"，必须走位。Battery Buster 是唯一可斜向攻击的武器，但需先攻击敌人蓄能切换使用、子弹小、火力有限，"仍相当受限"。（`00:24:38–00:26:27`）

### 数值与平衡：14-15 个 sidearm、60 个 trinket

sidearm 放置"做数学"：计划 14-15 个 sidearm、6-7 个核心关卡，每个区域一组约 4 个；按"这区域飞行敌人多 → 附近放对空道具"式推理放置。后期补偿机制：trick 可同时持有 2 个 sidearm，underlab（基地/检查点系统）每个检查点可寄存一个 sidearm；主持人 20 小时才误触发过一次 sidearm 重生——说明这套系统低调到常被忽略。trinket 共 60 个，设计目标是避免 Zelda 式"四分之一心"鸡肋感，每件针对一类痛点、"填补 move set 的洞"。治疗系统特殊：必须先攻击敌人蓄槽，之后用药水才把槽转化为血量。游戏后期可同时装备 6 个 trinket，他称可组合出"百万种 build"；开放世界"开局就能把游戏玩崩"，平衡极难——团队"把游戏玩了成千上万遍"逐个调整。（`00:27:14–00:33:41`）

速通与 build：游戏开始 30 秒拿到 wall burrowing，速通潜力大；combo capacitor 使攻击倍率升至 2.5 或 3.0 倍（依连击数）、受击清零，playtest 速通者数秒内打空 boss 血条。正篇约 20-30 小时，当前最佳速通约 1 小时 20 分（feat 为 4 小时）；他坦白发售后还没怎么关注速通圈进展。（`00:34:11–00:35:36`）

### 无感教学与七轮 NG+

新手引导被主持人赞为"令人惊叹地无感"：除序章外全开放，序章每个房间精心设计只教一个概念。教学链是因果式的：先教"钻地可穿栅栏"，之后出现"栅栏 + 两格缺口"场景，玩家自然尝试"边钻边跳"→ 自己发现跳得更远；"你没学会也会被逼着做过一次"。（`00:35:36–00:37:36`）

NG+ 共 7 轮、每轮改变玩法：第 1 轮标准（保留装备、更难、检查点更少）；第 2 轮世界左右镜像加清空全部物品；第 3 轮启用内置 item shuffler——开局给治疗瓶的 NPC 可能给出极好或极烂的东西。randomizer 5-10 年前流行，但"想不出多少游戏把它正经内建进游戏"，他们是"试了一把"（自评不确定是否先例）。后期 NG+ 区域等级互换，迫使重新规划练级与装备。他最爱的 trinket 现场答不出、需查表，最终给出 vascular syrup：致敬 Mother 系列的滚动血条——被打后血量滚动下降，滚动归零前治愈则存活；"在 NG+7 它变得至关重要"。（`00:38:17–00:43:30`）

## 来源与定位

- 原始节目：[Mina the Hollower](https://softwareengineeringdaily.com/podcasts/mina-the-hollower/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 嘉宾背景与 GB 风格由来（00:01:15–00:05:58）
  - 招聘与年代感（00:05:58–00:07:16）
  - 伪俯视挑战与存档 bug（00:07:38–00:09:44）
  - Propeller 引擎架构（00:12:38–00:17:01）
  - 纹理三角形 vs sprite（00:17:24–00:19:13）
  - GBC 假装的限制（00:10:02–00:12:54）
  - Castlevania 位置学战斗（00:19:13–00:24:10）
  - 禁止斜向攻击的立场（00:24:38–00:26:27）
  - sidearm/trinket 数值与平衡（00:27:14–00:33:41）
  - 速通与 build 数字（00:34:11–00:35:36）
  - 无感教学（00:35:36–00:37:36）
  - 七轮 NG+ 与 item shuffler（00:38:17–00:43:30）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- "开发六年""GBC 28 年"为主持人提问中的数字，受访者未确认；调色板色数、时长等受访者自述记不准的数字已尽量标注；本期未涉及众筹金额、团队规模与销量。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
