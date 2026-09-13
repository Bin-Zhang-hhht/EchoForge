---
item_id: software-engineering-daily-4c06df358961
title: '服务端重启：vlt 想把包管理的创新从客户端搬回注册表'
date: '2026-09-14'
published_at: '2026-01-22'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/next-gen-javascript-package-management-with-ruy-adorno-and-darcy-clarke/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/podcasts/next-gen-javascript-package-management-with-ruy-adorno-and-darcy-clarke/'
summary: '前 npm CLI 维护者 Darcy Clarke 与 Ruy Adorno 介绍 vlt：十五年只卷客户端之后重启注册侧创新——可自托管的 VSR 代理注册表、共享依赖图的全球缓存、CSS 式查询语言、默认不跑安装脚本，以及与 Socket 合作的恶意包扫描选择器。'
tags: [开发者工具, 开源, 安全]
---

# 服务端重启：vlt 想把包管理的创新从客户端搬回注册表

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-01-22 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 5143 字 · 阅读约 13 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [开源](/tags/%E5%BC%80%E6%BA%90/) [安全](/tags/%E5%AE%89%E5%85%A8/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/next-gen-javascript-package-management-with-ruy-adorno-and-darcy-clarke/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/podcasts/next-gen-javascript-package-management-with-ruy-adorno-and-darcy-clarke/)

## 速读

两位前 npm CLI 维护者——2019 年加入 npm 公司的 Darcy Clarke 与被他招进团队的 Ruy Adorno（现为 Node.js 技术指导委员会副主席）——经历了 2020 年 npm 卖给 GitHub、GitHub 又被微软收购的全过程，如今一起创办 vlt，重做包管理器与注册表。主持人 Josh Goldberg 的问题覆盖了从 Corepack 弃用到供应链安全的一整条线。

最值得带走的三点：JavaScript 包管理十五年来的创新几乎全在客户端，Yarn、PNPM 乃至 Deno、Bun 仍在对着十五年没变的注册表 API 做优化，vlt 的赌注是把创新搬到服务端（VSR 可自托管代理注册表 + 依赖图的共享全球缓存）；一条 CSS 灵感的查询语言成为客户端的统一原语，从 `:malware` 恶意包检测到跨仓库批量改 package.json 都靠它表达；以及"默认安全"已成共识——vlt、PNPM、Bun 都不再默认执行安装脚本。

## 主题正文

### 背景：从 npm 到 GitHub 再到 vlt

Clarke 做了二十年 JavaScript，2019 年加入 npm 公司、随后把 Adorno 招进团队，两人一起经历被 GitHub 收购、再被微软收购，"支撑着世界最大的包注册表"（`0:02:22`）。Adorno 补充了自己的另一重身份：Node.js 项目技术指导委员会（TSC）成员、现任副主席，主要工作是主持周会与协助贡献者（`0:03:43`）。

包管理器与运行时的关系被讲得很清楚：两边要对"模块放在哪、去哪找"有共识，Node 长期把 npm 随运行时分发是开先例的做法；Bun 与 Deno 正在模糊运行时与包管理器的边界。包管理器的传统价值在于一致性、安全与更新体验——二十年前的 CDN 直链时代，你根本不知道依赖出了新版本，自己打包则永远在发布遗留代码（`0:05:12`）。

### Corepack 之死与"监管俘获"之辩

Corepack 的来龙去脉由两人共同还原：它最初叫 PMM（package manager manager），由 Yarn 作者 Maël 推动进入 Node，动因是不同包管理器各自创新、混用时冲突频出，希望在 package.json 里加一个顶层键来"钦定"项目用的工具；落进 Node 前 npm 团队曾被征询意见（`0:07:57–0:10:04`）。结局是 Node 项目内部围绕它撕裂了很久，今年年初指导委员会投票决定"翻篇"：Node 25 仍随附 Corepack，但官方开始宣布弃用，给生态时间准备替代方案（`0:07:57`）。

Clarke 的批评相当尖锐：Corepack 本质是"监管俘获"——在包管理器之上再造一层需要"准入祝福"的工具注册簿，而包管理器本来就只是一个包，生态早已有约束它的机制（`0:10:04`）。

### vlt 论点：十五年的创新都发生在客户端

vlt 的核心判断是：从 2016 年前后的 Yarn 与 PNPM（PNPM 的想法其实更早）到现在，所有新客户端——包括 Deno 和 Bun——对着的是同一套十五年没变的 npm 注册表 API，性能与创新被锁死在客户端这一侧。于是 vlt 押注服务端：他们做了 VSR（vlt serverless registry），一个既充当 npm 等上游的轻量代理、又提供可自托管私有注册表的服务，与 vlt 客户端配套（`0:14:03`）。

更深一层的论点是冗余计算：你、我、Ruy 各自安装同一个包时，每一台机器都在边缘重复解析同一张依赖图——"这在对缓存与集中理解依赖图的机会上显得非常浪费"。vlt 正在后台做依赖图的索引与爬取，目标是让"解析后的依赖图"成为大家可以共享的全球缓存。他们特别点出：在正在到来的 AI agentic 浪潮里，只会出现更多机器在边缘做这种解析（`0:14:03`）。

自托管注册表并非没有先例——Verdaccio 是多年来唯一的选择——但 Clarke 强调 npm 注册表本身在 2013、14 年闭源后，代码层面的改进全被私有化了，vlt 想把这部分基础设施重新开放（`0:17:35`）。性能上，Adorno 写了高效的图解析算法，锁文件格式被刻意设计成服务端与客户端之间的交换格式；官网新发布的基准测试里，vlt 是"除 Bun 之外最快的包管理器"——而他们连编译都没做，还背着所有 JavaScript 系包管理器共有的冷启动负担（`0:18:50`）。锁文件的多重身份也被拆解：锁定安装（防止新版本夹带恶意软件）、加速安装（图已预先解析）、以及给人类审计依赖演化的账本（`0:19:52`）。

### 依赖解析：一个没有规范的"规范"

节目里最涨知识的一段是版本解析的真相：大家挂在嘴边的 SemVer 规范只定义了"什么是版本"，从未定义"范围"（ranges）——每组包管理器都在按自己的语法解释 `^1.1.0` 这类说明符（`0:22:14`）。钻石依赖问题（两个直接依赖各自传递依赖同一个包的不同版本）在 Java 一类生态里只能二选一，而 JavaScript 生态的答案是 npm 创造者 Isaac Schleuter 当年设计的嵌套方案：允许同一依赖的多个版本共存。不追求去重就是最朴素的嵌套策略；一旦要做去重，就得有"贪婪的"语法，允许解析到今天还不存在、但未来可能存在的版本——在不破坏软件的前提下取到最新的常青版本（`0:22:14`）。Adorno 补了一个哲学问题：他常问别人"什么是包？能代表一个包的最小字符串长什么样？"——答案五花八门（`0:25:55`）。

### CSS 式查询语言：一个原语，多种用途

vlt 客户端最有辨识度的设计是一条 CSS 灵感的查询语言。Clarke 对 CSS 有感情，认为它是"表达力与威力之间的完美折中"——比 PNPM 那套需要记住点点杠杠的过滤语法好记，而且元数据越丰富越好用（`0:31:21`）。具体解锁了几件事：

- **默认安全**：`vlt install` 不执行任何安装脚本，并打印提示；确有合法需求（如挂载原生二进制）时，可用查询语言写出精细的白名单。新的 `build` 命令接受查询选择器来运行这些受信包的构建。他很高兴"默认不跑安装脚本"已成风潮——PNPM 与 Bun 也一样（`0:27:11`）。
- **主机选择器（host selector）**：一条选择器可以查询整台机器上所有用 vlt 配置的项目。monorepo 内选项目早就不难，难的是跨 monorepo、跨仓库共享依赖、配置与查询——这以前做不到（`0:27:11`）。
- **pkg 命令与 scope 旗标**：`pkg`（他们当年在 npm 就引入了，Bun 最近也加了）像内置的 jq，对 package.json 取值、赋值、删除；几乎所有 vlt 命令都支持 `--scope` 旗标，让 install、version、pack、publish、run、exec 都能对着选择器选出的包集执行（`0:31:21`）。Adorno 给了个具体场景：维护上千个包的作者从 Twitter 迁到 Bluesky，一条 `vlt pkg` 命令配合主机选择器，再叠加"资助字段指向 Open Collective"之类的条件，就能把全部元数据一次改齐（`0:34:48`）。
- **浏览器 UI**：实时可视化一条查询到底选中了哪些包，图遍历不再靠想象（`0:30:38`）。

### 供应链安全：`:malware` 与"扫描后安装"

查询语言最令人警醒的用法是博客示例里的 `:malware` 选择器——跑一下查询、万一有结果，说明你已经装了恶意包。它的机制是与 Socket 一类的安全情报商合作，用供应商元数据持续丰富依赖图；这是个"可变选择器"，随情报实时更新（`0:36:54`）。vlt 同时做主动与被动扫描：可以显式选择 `scanned` 选择器，"没被扫描过的包拒绝安装"；即将推出的供应商专属选择器还能指定"必须由 Socket 扫过才装"（`0:36:54`）。

更细腻的是噪音治理：CVE 有类型体系（CWE），比如 ReDoS（正则拒绝服务，CWE-1333）。如果你是开发者工具、不在乎低效正则这类告警——他顺势调侃了"紫色公司"Snyk 的低效通告——可以用选择器按类型把噪音过滤掉（`0:36:54`）。文件系统访问、网络访问、环境变量访问都有快捷选择器（`fs`、`http` 等），配合 CSS 的 `:not` 取反与 vlt 的 modifiers（override 机制），可以"凡有文件系统访问权的包一律禁止安装"（`0:36:54`）。

向前看，他们多年前就提过 distributions RFC：让一个包在同一作用域下提供条件变体——带测试与文档的全量版与裁剪编译的生产版并存、老 Node 自动选 polyfill 变体、新运行时直接用原生实现——并且他们与一些维护着"本可内置进运行时"的遗留库的作者关系很近，对方也希望推动现代化（`0:41:59`）。客户端侧对应的机制是已发布的 graph modifier：在图构建阶段把某个包的定义替换掉，经典 overrides 已支持，package extensions 在计划中（`0:44:30`）。

### 细节与彩蛋

两个值得记录的生态观察：其一，vlt 在 docs.vlt.sh 提供了可能是唯一的 npm 注册表 API 系统文档——npm CLI 当年文档尚可，注册表从来没被好好记档；VSR 实例还自带交互式文档（Scalar 体验），可以直接试调 API；vlt 承诺对 npm 注册表保持向后兼容（`0:45:44`）。其二，Adorno 强调客户端的"小确幸"：查询命令默认输出 npm ls 那样的树形结构而非 JSON 团块，`vlt ls` 与 `vlt query` 支持 JSON 与 mermaid 输出——后者可以直接贴进 HackMD、Notion 或 GitHub issue 渲染成图（`0:48:14`）。

收尾的技术预告是他们正在做的"全局依赖图爬取"——在用户行动之前先理解整张图，他顺带挖苦了"高度理论化"的 SBOM（`0:50:27`）。彩蛋环节：Adorno 练巴西柔术，"每次去都被按在地上摩擦，但对久坐的开发者是极好的锻炼"；Clarke 回忆少年时收到的 Kurt Cobain 日记出版品，建议大家"把副本都烧了，让逝者安息"，但保留《Donnie Darko》的 VHS（`0:51:26–0:55:12`）。

## 来源与定位

- 原始节目：[Next-Gen JavaScript Package Management with Ruy Adorno and Darcy Clarke](https://softwareengineeringdaily.com/podcasts/next-gen-javascript-package-management-with-ruy-adorno-and-darcy-clarke/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 两人背景与 npm/GitHub/微软收购经历（0:02:22–0:03:43）
  - 包管理器与运行时的分界、CDN 直链时代（0:05:12）
  - Corepack 的投票结局与 Node 25 随附现状（0:07:57）
  - PMM 起源与"监管俘获"批评（0:10:04–0:13:32）
  - 十五年客户端创新论与 VSR（0:14:03）
  - 边缘重复解析与共享依赖图缓存、AI 浪潮（0:14:03）
  - npm 注册表闭源史与 Verdaccio（0:17:35）
  - 性能基准与锁文件作为交换格式（0:18:50）
  - 锁文件的多重目的（0:19:52）
  - SemVer 不定义范围与钻石依赖、嵌套方案（0:22:14）
  - "什么是包"之问（0:25:55）
  - 默认安全与 build 命令（0:27:11）
  - 主机选择器（0:27:11）
  - 浏览器 UI（0:30:38）
  - CSS 式查询语言、pkg 与 scope（0:31:21）
  - 千包迁移元数据示例（0:34:48）
  - `:malware` 选择器与 Socket 合作（0:36:54）
  - CWE 类型过滤与 fs/http 选择器（0:36:54）
  - distributions RFC 与条件变体（0:41:59）
  - graph modifier 与 package extensions（0:44:30）
  - npm 注册表文档与交互式 docs（0:45:44）
  - 树形默认输出与 mermaid 输出（0:48:14）
  - 全局图爬取预告与 SBOM 评价（0:50:27）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 逐字稿为出版方提供的官方转写，个别词形按上下文校订（如 "Isaac Schleuter" 通常拼写为 Isaac Schlueter、"SOMs" 当为 SBOMs、Scalar 在逐字稿中写作 "Scalr"）；性能基准数字为受访者口径，无法独立验证。
- 访谈结尾的巴西柔术与 Kurt Cobain 日记属闲聊环节，仅作简要记录。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
