---
item_id: software-engineering-daily-12692deda714
title: 'Prettier 的历史与哲学：确定性格式化、注释难题与"完成后"的开源'
date: '2026-09-13'
published_at: '2026-03-19'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/prettier-and-opinionated-code-formatting-with-james-long/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1906-Pretter.txt'
summary: 'Prettier 早期贡献者 James Long 谈确定性格式化的哲学：为什么 gofmt 路线在 JS 失败、注释是"最难的"、以及九个月 24.3 万美元的开源资金现实。'
tags: [开源, 开发者工具, 编程语言]
---

# Prettier 的历史与哲学：确定性格式化、注释难题与"完成后"的开源

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-03-19 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3314 字 · 阅读约 9 分钟
>
> 标签：[开源](/tags/%E5%BC%80%E6%BA%90/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [编程语言](/tags/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/prettier-and-opinionated-code-formatting-with-james-long/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1906-Pretter.txt)

## 速读

Prettier 早期贡献者 James Long（前 Mozilla/Stripe）接受 SED 访谈（主持为 typescript-eslint 维护者 Josh Goldberg），讲 opinionated code formatting 的起源与哲学。Prettier 的核心是确定性：无论输入里有多少空格、换行、个人风格，输出格式完全相同——主要只有一个参数（打印宽度）。起因是消除团队内关于格式的争执与 PR review 里的格式 nit。

最有价值的部分是三段：为什么此前照搬 gofmt 哲学的工具在 JavaScript 上失败（需要打印宽度的概念）；Prettier 的技术核心——AST 之后的"扁平描述数组"中间表示、以及注释处理是"最难的"；还有开源资金的现实——opencollective 上九年累计约 24.3 万美元，他的评价是"少得离谱，不够"。逐字稿有数处转写误差与说话人标签错位，文中已标注。

## 主题正文

### 起因：格式之争与"社会认同"式采纳

James 的动机很朴素：消除团队内（甚至特定成员之间）关于格式的小争执和 PR review 里来回的格式 nit——他在 Mozilla 工作时觉得为此来回评审"纯粹浪费时间"。格式争论是一种"奇怪的情绪化"的东西，对最终用户"零差异"。意外收获是编辑器集成带来的快速书写：可以随便写、一次按键就得到可提交的格式——"出奇地有效"，且他原本做 Prettier 并不是为此。（`00:05:39–00:07:46`）

推行阻力与应对：主持人在微软团队听到的典型反对是"我在格式里注入了意图和含义"；James 回应这种声音现在少多了，他认为该论点"已被证伪"——那是对自己代码的执念。他当年的应对是请对方"给它五分钟"试用；确有需要可用 prettier ignore 跳过；如果仍不同意，"他们可以不用 Prettier"。后续采纳很大程度上靠"社会认同"——用的人多了，反对者会去试并发现事实。初期最难的舆论工作是"一页又一页的 GitHub issue"：某些格式问题"花了好几年"，第一年像"永远在往山上推石头"。（`00:09:40–00:17:43`）

### 为什么出现得晚：gofmt 路线在 JS 上失败

Christopher Chedeau 是 Prettier 的共同创造者（"他和我们都各自说是我们创造了 Prettier，我对此没有意见"）；James 技术上写了第一个实现。此前尝试的格式化工具失败的原因：它们照搬了 gofmt 的哲学——gofmt"比 Prettier 更加 opinionated"、没有 print width 概念；JavaScript 需要打印宽度，因为大量嵌套内联函数等模式，同一结构在顶层与作为函数实参时格式不同，gofmt 式做法"在真实世界模式上过快失败"、效果"太丑"——工具要成功就不能"看起来糟糕"。（`00:11:41–00:15:25`）

### 与 ESLint 的关系：为什么 lint 规则不够

Mozilla 曾用 ESLint 的格式规则加自动修复，"我发誓配置里有一百条规则"。他给出 ESLint 不够的两个原因：数百条可定制规则让不同团队保留了过多控制权、且规则"覆盖不了所有情况"，PR nit 依旧存在；有些模式无法用 lint 规则表达——例如函数调用的断行缩进需要"能推断函数位置及其父节点的整体性格式化器"。工具链拼接慢的根源是每个工具都要各自 parse 再生成 JavaScript；他从来不喜欢 eslint-plugin-prettier 这类方案（显著更慢）；主持人证实：带类型信息的慢规则与 Prettier 自动修复会反复互踩，"ESLint 在修复冲突时最多把规则重跑 10 次"。正因如此，把工具捆绑为单一套件（Oxfmt、Biome 的方向）很有吸引力——parse 一次、都在 AST 上进行。（`00:08:03–00:09:40`，`00:35:03–00:36:40`）

### 开源资金的现实

opencollective 上九年多累计筹款"约 243,000 美元"——他的回应是"少得离谱，不够"。整个项目生命周期里 Chedeau 付出的工作"远多于我"，并搭建了向维护者分配的结构；没有任何人在全职做 Prettier、也不存在"Prettier 公司"——典型的少数人兼职开源模式，有报酬但"不够"。个人轶事：2018 年投入大量时间时，妻子质问"这要怎么赚钱"。（`00:17:43–00:21:16`）

### 创造阶段 vs 维护阶段、"完成态"与 Rust 重写

两者的关系是波浪式而非"开头有趣、之后十年无聊维护"：有趣的高峰 → 维护低谷 → 新的创造高峰（当前的例证是 Prettier 的 Rust 重写 Oxfmt）。关于"完成态"：与必须随浏览器/CSS 不断演进的 Tailwind 不同，Prettier"更有可能被做完"——根本性的新 JavaScript 语法相对罕见；"对我而言它是完成的。我每天都用它"。对 Rust 重写他毫无情感包袱："如果它同样好用且稍微快一点，我会乐意切换"；现有的兼职维护者更适合改进当前代码库，若另一群人有资金全职做一两年，"很棒，确实解决痛点，我完全支持"。（`00:21:16–00:29:42`）

### 技术原理：解析、AST、扁平描述数组与注释难题

给新手的解释：解析器把代码字符串变成 AST——"带语义信息的树"。Prettier 的独特之处是在 AST 之后再生成一层中间表示——不是 AST，而是"扁平的描述数组"：文本片段加断行信息（break information）；最后一遍生成字符串。他总结"Prettier 基本上就是个编译器……字符串进、字符串出"。三个难点：性能与缓存（AST 约 100 种节点类型、每种都要实现）；错误处理（源位置必须穿透整个编译过程）；以及他称"Prettier 里最难的"——注释：与编译器不同，格式化器必须保留全部注释，而注释不是 AST 节点、无语义，代码重排后要决定它放哪；边缘案例包括代码折叠到一行后行注释会注释掉整行剩余部分——"一大桶边缘情况，很难"。（`00:38:36–00:45:24`）

### 生态评价与个人方向

"工具太多、难配置"的批评有其真实痛点根源，但要分开看：这类抱怨"五年前成立"，如今生态已大为改善（Bun 解决了后端环境与脚本运行、Vite 解决了打包）。他明确不喜欢 React Server Components、对 Next.js"非常犹豫"；更关注更好的 SSR 与 hydration 方案。离开 Stripe 后他在重新评估技术观点：喜欢 SolidJS 的方向、Remix 3"可能最契合我近期的想法"。（`00:29:42–00:33:47`）

## 来源与定位

- 原始节目：[Prettier and Opinionated Code Formatting with James Long](https://softwareengineeringdaily.com/podcasts/prettier-and-opinionated-code-formatting-with-james-long/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 起因、确定性与社会认同式采纳（00:05:39–00:17:43）
  - gofmt 路线在 JS 失败的原因（00:11:41–00:15:25）
  - 与 ESLint 的关系及单套件的吸引力（00:08:03–00:09:40）（00:35:03–00:36:40）
  - 开源资金现实：九个月 24.3 万美元（00:17:43–00:21:16）
  - 创造与维护的波浪式、"完成态"（00:21:16–00:29:42）
  - 扁平描述数组与注释难题（00:38:36–00:45:24）
  - 生态评价与个人方向（00:29:42–00:33:47）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。逐字稿有数处转写误差与说话人标签错位（async away→async/await、button→Bun 等），已按上下文校正并标注。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 资金数字、ESLint 规则数等为受访者口述（多处自述记不清），未独立验证；"Prettier 创建者"（片头）与"共同创造者"（受访者）的表述张力已如实保留。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
