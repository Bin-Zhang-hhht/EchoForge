---
item_id: software-engineering-daily-6ec8b2d45a59
title: 'Skate Story：玻璃恶魔、自研滑板物理与"Boss 战花了五年"'
date: '2026-09-13'
published_at: '2026-03-17'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/skate-story-with-sam-eng/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1900-Skate-Story.txt'
summary: '独立开发者 Sam Eng 详解 Skate Story：自研滑板物理、warble shader 的玩法锚定、stomp 连招系统，以及"玩家玩完想去玩真滑板就是成功"。'
tags: [开发者工具, 产品指标]
---

# Skate Story：玻璃恶魔、自研滑板物理与"Boss 战花了五年"

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-03-17 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 2404 字 · 阅读约 7 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [产品指标](/tags/%E4%BA%A7%E5%93%81%E6%8C%87%E6%A0%87/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/skate-story-with-sam-eng/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1900-Skate-Story.txt)

## 速读

独立开发者 Sam Eng 做客 SED（主持为 Joe Nash），讲被多家媒体列入 2025 年度最佳的 Skate Story——玩家扮演玻璃恶魔、在地下世界滑板、试图吃掉月亮。这期对游戏开发者最有价值的是把"手感"拆成可迁移的工程决策：滑板物理从零手写（不用 Unity 物理）、时机指示器绑定移动速度、stomp 连招系统源自"滑手自己宣告连招结束"的现实观察。

最动人的是成功标准："如果玩家玩完想去玩真滑板，那就是成功的度量。"文中未涉及销量数字。

## 主题正文

### 叙事起源与滑板手感设计

游戏的因果链：最初设定"滑向地下世界"→ 玩法需要"一个玩家能轻易看见的巨大目标"→ 天上巨大的球体最合适 → 月亮；随后才补出"因为月亮看起来好吃所以想吃"。操作方案是全游戏最大的设计挑战：起点想做"最真实的模拟器"，后自我修正——这是叙事冒险，必须简化操作、目标是"不看教程也能大致上手"；部分硬核滑板游戏玩家认为"太简单"，他当作夸奖。（`00:04:32–00:08:16`）

两个有原创性的设计决策。其一，时机指示器绑定移动速度：现实中滑板的速度影响动作难度（慢速学 kickflip 容易，20 mph 下坡时非常难），而这在游戏中几乎没被表现过——借鉴《Gears of War》的 Active Reload；指示器现在完全可选、只影响跳得更高得分更高。其二，动作基于脚的位置、借鉴 FromSoftware 式动画驱动——动作不可随意打断（约 0.1 秒过渡）。难度取舍有真实的分歧记录：早期 playtest 反馈"太难"，他回应"这就是滑板"，玩家回应"但这是电子游戏"，最终妥协——ollie 几乎随时可按、脚会快速归位。（`00:08:16–00:19:59`）

摔倒系统没有"死亡"（"恶魔不会死，它们本来就不算活着"）；创新是摔倒时相机滚动——相机即"物理身体"，灵感来自滑板视频里滑手踢翻摄像机与亲身体验，且提供关闭选项。（`00:19:59–00:23:16`）

### Boss 战："整整花了五年"

他认为"没有滑板游戏做过传统血条式 boss 战"；自己的设计原则是招式本身就是伤害手段、连招必须有意义——这个问题花了整个开发期。迭代史：过门关 → 追逐月亮用 kickflip 伤害 → 竞技场版被发行商批评"可以躲在角落刷 kickflips 磨死 boss"（他承认"确实 suck"）。关键顿悟：现实中连招不是"四轮着地即结束"（Tony Hawk 的规则），而是滑手自己宣告结束——由此数月迭代出 stomp 系统：招与招之间有几秒推板缓冲，空中按一次键 stomp 即结束连招、把积累的动量作为伤害释放。发售前最后一年打磨的 "cosmic light systems"：月亮投影是弱点，玩家需连招并在投影月光中以 stomp 收尾造成伤害。（`00:23:16–00:32:35`）

### 视觉风格、warble shader 与自研物理

内部设计准则是"复古视觉的现代演绎"——"不是 PS1 画面，而是某种 PS1 游戏的写实版本"（4K、HDR、tone mapping、shader 全用上）。重点讲的 warble shader：tone mapping 之前的后处理，将 3D 纹理平铺于世界空间、经深度缓冲重投影后采样偏移屏幕空间 UV；效果空间锚定——近处与屏幕中央的物体趋近变直，为了玩法（让玩家看清直边以便 grind），越远越靠边缘 warble 越强。该 shader 想明白如何实现花了"好几天"。性能：非常 low poly 是为了在大量机器上流畅运行（Steam Deck 流畅；未登陆 Switch 1 但能锁 30fps）。（`00:36:30–00:43:25`）

引擎与物理的重要事实：游戏用 Unity 但完全不用 Unity 物理——滑板物理从零手写、玩家没有物理刚体，仅与 Unity 物理场景交互。他自评实现是"gigantic pain in the ass"、至今不完美——wall riding 是最大问题源，但发生频率不高；主持人的观点是成熟物理引擎同样有怪异交互。（`00:43:25–00:46:03`）

### GUMBO 与成功标准

GUMBO 是纽约的游戏开发者联合办公非营利集体（DUMBO = Down Under the Manhattan Bridge Overpass → GUMBO = Games Under the Manhattan Bridge）：从 Green Desk 两人办公室塞 5 个人、每人月付约 200 美元起步，疫情后在街对面找到旧工厂改建的大空间、约 20 人加入并持续增长。成功指标（他明确的主要 metric）："如果玩家玩完想去玩真滑板，那就是成功的度量"——游戏核心信息是回应"如何坚持做这件又难又傻的事"。收尾自评："整个游戏就是谈论我 special interest 的借口。"（`00:47:41–00:55:50`）

## 来源与定位

- 原始节目：[Skate Story with Sam Eng](https://softwareengineeringdaily.com/podcasts/skate-story-with-sam-eng/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 叙事起源与因果链（00:04:32–00:08:16）
  - 滑板手感设计：时机指示器绑定速度、脚位与动画驱动（00:08:16–00:19:59）
  - 摔倒相机与"恶魔不会死"（00:19:59–00:23:16）
  - Boss 战五年迭代与 stomp 系统（00:23:16–00:32:35）
  - warble shader 与性能取舍（00:36:30–00:43:25）
  - 自研滑板物理（00:43:25–00:46:03）
  - GUMBO 社区与成功标准（00:47:41–00:55:50）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 未涉及销量与音乐授权话题（逐字稿内未出现）；开发周期约 5 年来自主持人表述。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
