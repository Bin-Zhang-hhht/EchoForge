---
item_id: software-engineering-daily-84ff67512b56
title: 'Biome 的取舍哲学：从 Rome 倒闭到"插件有代价"的工具链设计'
date: '2026-09-13'
published_at: '2026-06-18'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/biome-and-the-future-of-javascript-tooling/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/06/SED1935-Biome.txt'
summary: 'Biome 首席维护者 Emanuele Stoppa 谈工具链设计：Rust 重写的 8GB 内存动因、module graph 与类型推断、GritQL 插件，以及"插件有代价"的强观点。'
tags: [Rust, 开发者工具, 开源]
---

# Biome 的取舍哲学：从 Rome 倒闭到"插件有代价"的工具链设计

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-06-18 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3994 字 · 阅读约 10 分钟
>
> 标签：[Rust](/tags/Rust/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/biome-and-the-future-of-javascript-tooling/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/06/SED1935-Biome.txt)

## 速读

Biome（前 Rome）创作者兼首席维护者 Emanuele Stoppa 接受 SED 访谈（本期主持人为 typescript-eslint 维护者 Josh Goldberg），讲这个 Rust 编写的 JS 工具链的设计哲学。核心是贯穿全期的取舍观：插件扩展性有代价、性能与维护负担"由用户买单"；能力应该内置于工具以便正确实现并监控性能；配置应当静态、可预测、易调试。

最有信息量的部分：转向 Rust 的直接动因（Rome 的 TypeScript 版打包自身内存达 8GB，"感觉到了 Node.js 的极限"）；Biome 的 module graph 加类型推断如何做到不依赖 TypeScript 编译器的 type-aware 规则；以及从 Rome 倒闭到被迫改名的开源治理故事。受访者多处明确自述"没有答案"或"我不全了解"，文中如实标注。

## 主题正文

### 从 Webpack 到 Rome：工具链即产品

Ema 的入行经历绕了远路：想做游戏开发，大学那年的游戏设计课没有教授，转学 Web（PHP、Postgres、jQuery 直到 React）。他有个值得记录的观点：如今 SSR 回潮就是 PHP 时代的老做法，只是语言换了——"我们没有发明任何新东西，只是用不同工具重复同样的模式"。他因工作中反复与 Webpack"斗争"成为熟手而加入 Webpack CLI 团队，后认同 Rome 的 all-in-one 使命（格式化、lint、打包、测试全在一个二进制里）而加入。（`00:02:04–00:09:11`）

对 bundler 的定义：本质是"链接器"，把散落在应用与依赖中的 JS 文件连成浏览器可用的产物；现代 bundler 要处理 HTML、CSS、Sass、TypeScript、WASM、source maps，"是最难也最有回报的软件之一"。单文件组件（Vue/Svelte/Astro）带来打包难点：一个文件同时含 JS/HTML/样式，bundler 必须决定样式合并顺序。被问打包实现细节时，他明确说"我没有清晰的答案"。（`00:09:11–00:17:34`）

### 插件的代价：ESLint 的教训与 flat config

全期最强的立场：插件扩展性有代价，性能与维护负担最终"由用户买单"，工具链膨胀会退化到"Webpack 打包约 30 分钟"的程度。ESLint 的案例被他用来论证配置设计：旧配置是递归式的，"无法搞清哪个插件在捣乱、难以调试"，所以 V9 转向 flat config——"破坏了生态"，很多用户不满，但他认为"从长远看会划算"。更深一层的因果是：ESLint 的力量来自插件系统，但也因此"现在无法创新"——改任何东西都可能让存量插件在不知情的情况下损坏。对 Rolldown 的预测他也不乐观："我认为它不会解决所有问题"，应用会更大更复杂，"3、4 年、5 年后会再遇到同样的问题"。被追问如何在"用户能力"与"内建完整度"之间划界，他直接回答"说实话我没有答案……我真的不知道"。（`00:17:34–00:23:32`）

### 为什么用 Rust 重写：8GB 内存的直接动因

三个理由。其一，Rust 语言非常严格，重大变更在编译期就能暴露。其二（直接原因）：Rome 的 TypeScript 版能把自身打包成二进制，但打包过程中内存消耗达 8GB，"不可持续，感觉到了 Node.js 的极限"；JS 的 GC 工具很有限，Rust 允许更细的内存管理。其三，通过 wasm-bindgen 很容易编译到 WASM、利于 playground。他补充 TypeScript 也有类型、类型不是问题所在，Rust 的卖点还包括内存安全。（`00:23:32–00:26:51`）

### 从 Rome 到 Biome：倒闭、改名与使命收缩

Rome 公司因融资断裂倒闭；Ema 离职后以志愿者身份继续贡献，后来形成志愿者团队持续发版。改名是被动的：NPM 令牌过期，无法再发布新版本，"被迫"完成迁移（logo、名字、域名等本不想做的工作）；名字出自时任 Rome CTO 的 James 提议的"Second Rome"→ Biome。Rome 于 12 月倒下，次年 8 月宣布 Biome 为新的 Rome。使命也随之收缩：资源变少、无专职人员，不再做 bundler，改为"垂直"深耕 formatter 与 linter。（`00:26:51–00:29:25`）

### Biome 的差异化：module graph 与类型推断

DX 目标是错误信息更好、可操作、承担教学使命——规则必须解释"为什么错"，否则"就不是一个错误"（举例：针对 .reduce 的规则，返回 accumulator 时不要用 spread 操作符，因为是性能问题）。配置对比：几年前配 ESLint+Prettier 要装"三四个包"、约 10 分钟配置；Biome 一个依赖、一份配置、合理默认值。（`00:29:25–00:34:37`）

架构上最有差异化的能力是 type-aware rules 与 project rules——不依赖 TypeScript 编译器。Biome 在 lint 前先扫描全项目收集信息，从而支持 no-import-cycles（遍历整个 import 树）、检测 package.json 中未安装却被使用的依赖，甚至检测"使用了项目中任何地方都未定义的 CSS class"。这些能力来自 Biome 的 module graph，它是"语言无关"的（同时收集 HTML、CSS、JavaScript 等多种语言）。概念区分（他纠正主持人的说法）：module graph 是通用数据结构，只记录"谁导入谁"；semantic model 是单文件、语言特化的——JS 下理解作用域、CSS 下计算选择器 specificity。类型推断由另一位核心贡献者主导、Vercel 雇佣其完成；Ema 坦承"细节我不全了解"，但修过其中几个 bug（如通过把 semantic model 集成进推断系统，解决无法推断 Lodash 导入函数是否为 promise 的问题）。（`00:34:37–00:43:17`）

### 插件系统：GritQL 与 codemod

插件基于 GritQL DSL，动机是"原生代码速度快但多数用户不是原生语言开发者"；适用场景是项目/雇主特有的规则、涉及敏感数据的检查——"工具不可能也不应该知道你代码库的怪癖，那是敏感信息"。现状：截至目前插件只能报诊断、不能提供代码修复；code fix 的 PR"可能在下一个 minor"合并。他自我修正：插件能提供 fix 这件事"推翻了我'插件不好'的论点"，但在这种场景下插件是合理的；lint 规则的 code fix 也可充当 codemod 工具（他确认）。据他所知有用户写了"70 个甚至更多"GritQL 插件，GritQL 诞生之初目标就是做 code mod。（`00:43:17–00:46:55`）

### 未来方向与迁移建议

路线图：`biome lint --watch`（内部本来实现了 watcher，现在只是通过 CLI 暴露）；Markdown 支持内部已对 CommonMark 达到 100% 覆盖、formatter 正在搭建；Vue lint 规则在做的路上、Svelte"大概会开始"、Astro"我还需要调研"；LSP 一次开发服务所有编辑器，Biome 的使命是业务逻辑只实现一处。利用 module graph 实现 go-to-definition 是"潜在可做、而其他工具做不到"的事——"我们拥有整条栈、拥有全部信息"；他自述想法很多、缺的是时间，现在靠 AI 代理快速写代码并 review。社区归因："Biome 本质是社区的努力，核心团队只是协调者"——markdown parser、CSS/Sass 支持多为社区贡献。（`00:46:55–00:55:14`）

迁移路径实用：一是 Biome 提供读取 ESLint 与 Prettier 配置、生成对应 Biome 配置的命令（"我们不可能有全部 ESLint 规则"）；二是先用 `biome lint --suppress --suppress-reason` 压制全部存量违规，之后渐进处理。与 Prettier 的格式化兼容度："我们匹配了 Prettier 格式化的 97%"。大规模格式化变更的技巧：单独一个格式化 PR 先合并，再配 git revision ignore，这样 git blame 历史不会被格式化改动污染。（`00:55:14–00:58:42`）

## 来源与定位

- 原始节目：[Biome and the Future of JavaScript Tooling](https://softwareengineeringdaily.com/podcasts/biome-and-the-future-of-javascript-tooling/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 入行经历与 SSR 回潮观点（00:02:04–00:09:11）
  - bundler 定义与单文件组件难点（00:09:11–00:17:34）
  - 插件的代价与 ESLint flat config（00:17:34–00:23:32）
  - Rust 重写的三个理由与 8GB 动因（00:23:32–00:26:51）
  - Rome 倒闭、改名与使命收缩（00:26:51–00:29:25）
  - DX、教学使命与配置对比（00:29:25–00:34:37）
  - module graph、类型推断与 semantic model（00:34:37–00:43:17）
  - GritQL 插件与 codemod（00:43:17–00:46:55）
  - 路线图与社区归因（00:46:55–00:55:14）
  - 迁移建议与 97% 兼容（00:55:14–00:58:42）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 内存数字、兼容度与插件数量均为受访者口径，未作独立验证；受访者多处自述"没有答案""我不全了解"，正文如实标注。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
