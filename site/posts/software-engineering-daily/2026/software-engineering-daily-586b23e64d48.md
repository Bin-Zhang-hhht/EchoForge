---
item_id: software-engineering-daily-586b23e64d48
title: '供应链攻击日常化之后：Chainguard 的从源构建、SBOM 覆盖率与机器速度补丁'
date: '2026-09-13'
published_at: '2026-08-04'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/ai-powered-threats-to-the-software-supply-chain/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1948-Matt-Moore.txt'
summary: 'Chainguard CTO 复盘 XZ Utils 与 CI/CD 攻击案例：从源构建消除整类漏洞、SBOM 要看覆盖率而非有无，以及 AI 加速漏洞发现后"以机器速度打补丁"的紧迫性。'
tags: [开源, 供应链安全, 企业 AI]
---

# 供应链攻击日常化之后：Chainguard 的从源构建、SBOM 覆盖率与机器速度补丁

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-08-04 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 4237 字 · 阅读约 11 分钟
>
> 标签：[开源](/tags/%E5%BC%80%E6%BA%90/) [供应链安全](/tags/%E4%BE%9B%E5%BA%94%E9%93%BE%E5%AE%89%E5%85%A8/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/ai-powered-threats-to-the-software-supply-chain/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1948-Matt-Moore.txt)

## 速读

这是 Chainguard 联合创始人兼 CTO Matt Moore 时隔两年的回访。两年前这期节目还在讲"加固容器镜像"，如今公司已扩展到 VM、语言库、GitHub Actions 乃至 Agent skills，而访谈的真正主线是：开源供应链攻击从偶发事件变成日常，防御思路必须从"修 CVE"转向"消除整类漏洞"。适合所有依赖公共镜像源与包管理器的团队。

最有信息量的三段：XZ Utils 攻击的复盘（为什么从源构建恰好防住了它，以及为什么不能指望它每次都防住）、对 SLSA 框架"没强制短时效凭证"这一缺失的批评，以及把 SBOM 从"有没有"改造成"覆盖率"问题（WordPress 测试）。结尾关于 AI 模型加速漏洞发现与武器化的判断，是全期最紧迫的提醒。文中攻击数字与效果声明均为受访者说法。

## 主题正文

### 从加固镜像到"安全供应链即服务"：消除整类漏洞，而不是追着 CVE 跑

Matt 把 Chainguard 的起点归因于 SolarWinds 事件带来的行业觉醒，而产品演进是一条清晰的扩展线：容器之后是 VM 与语言库，最近一次用户大会上宣布进入加固 GitHub Actions 与 Agent skills。他用来解释问题的类比是数字音乐史：从公共镜像源取用开源软件"就像从 Napster 下载歌，有时是歌，有时是恶意软件"，而 Chainguard 想做的是 iTunes 到 Spotify 的角色转变——早期按镜像计费，现在更多是开发者席位订阅整个目录。（`00:04:00–00:08:07`）

方法论上，他把 CISA"Secure by Design"中"消除整类漏洞"的思路作为公司北极星：从源码构建让上游补丁必然被应用，同时绕开了公共制品仓库——他引用的数据是，近年恶意软件攻击的来源里 98% 到 99% 可以靠从源构建消除。行业背景在恶化：CVE 数量爆炸（节目提到 Firefox 某次发布修补了约 150 个 CVE，是以往版本的 10 到 20 倍），恶意软件攻击从每月一次加速到每天一次。但他表示两年来没有任何客户在使用其产品时被这些攻击波及——这是公司口径，不是独立验证。（`00:08:51–00:12:06`）

运营节奏上，规模是每季度新增 200 到 300 个镜像，自动化优先、人只在异常时介入，Agent 最早被用于扩充镜像目录的回归测试；补丁时效方面，主持人引述的关键漏洞平均修补时间低于 20 小时（受访者口径），Matt 另宣布对已知被利用漏洞（KEV 清单）提供 24 小时修补 SLA。（`00:25:49–00:28:55`）

### 案例复盘：XZ Utils 与 CI/CD 为什么成为首选攻击面

XZ Utils 复盘是全期技术密度最高的段落。Matt 强调该攻击的耐心与手法至今"仍是独一档"：攻击者"Jia Tan"（他特意给 person 加了引号）用约两年半时间以正常贡献积累社区信任，获得维护者级权限后篡改了发布分发包——下游发行版构建时才触发恶意代码。Chainguard 从源构建恰好防住了这次攻击：他们构建的是被污染的分发包，但构建方式没有激活攻击代码，且攻击修改专门针对生产 deb/RPM 的系统，而他们不构建这两类包。他随即补上边界：如果攻击者选了另一条路径，从源构建未必挡得住，所以必须纵深防御（瑞士奶酪模型），"任何声称单层防御 100% 的人都在撒谎"。（`00:12:06–00:19:23`）

这引出两类互补的工程实践。其一是他称之为"灰件"（grayware）的准入思路：不只匹配恶意软件签名，还标记"你想跑的程序不会做"的行为——建立远程访问终端、把凭证传到不该去的地方；这类软件未必被入侵，但关键是要明确什么允许进入生产环境。（`00:15:24–00:16:37`）其二是构建期行为扫描：Chainguard 对比补丁版本之间（x.1 对 x.2）的构建行为差异并标记新增网络连接，他举了一次真实拦截——某个 Python 库的源码被植入 .pth 文件、让解释器在运行时自动加载，扫描在重建前拦下该版本，干净的上一版和后续修复版照常发布。他同时承认透明度悖论：开源的扫描器会被攻击者拿来测试规避，因此部分检测手段必须保持隐秘；配套手段还包括编译器加固与内存安全组件替换（sudo-rs、uutils 等）。（`00:19:34–00:22:07`）

CI/CD 是另一条主线：tj-actions 事件中被入侵的 GitHub Action 抽取了 CI 密钥。Matt 的口号是"把构建系统当生产系统对待"——CI 拥有推送生产的极高权限，却常是防护最弱的环节。他直言 SLSA 框架最大的缺失是没有强制短时效凭证，因为 tj-actions、Shai-Hulud 等攻击外泄的都是长期凭证；Chainguard 为此做了 Octo STS 凭证联邦服务并以公共品运营。他还介绍了"冒名提交"（impostor commits）技术：把 Action 固定到的提交可以实际来自一个 fork 而非表面上的仓库——该技术三年半前由其工程师披露给 GitHub，并被用于入侵 Trivy。（`00:22:07–00:25:49`）

### SBOM 的"暗物质"：覆盖率、WordPress 测试与监管

面对欧盟《网络弹性法案》（2027 年底生效、强制 SBOM、24 小时漏洞上报），Matt 认为这是顺风，但立即把矛头指向 SBOM 话语的空洞化：监管只说"必须有 SBOM"，却不谈覆盖率、格式、最小元素与解析深度——"一份空的 JSON 也能通过 schema 校验，覆盖率为 0%"。他主张把 SBOM 当代码覆盖率看待，目标是逼近 100%。（`00:36:07–00:41:33`）

可操作的标准是他转述 CEO Dan 的"WordPress 测试"：SCA 工具能否告诉你官方 WordPress 镜像里真的有 WordPress？官方镜像在构建时下载源码编译，元数据里根本没有 WordPress；而 Chainguard 的镜像中一切内容都来自自己的包数据库，任何 SCA 工具都能列全。他顺带讨论了 CycloneDX 与 SPDX 双格式、发行版包数据库实质上就是 SBOM，以及 Rust 需要 auditable 模式才会输出依赖元数据（并点名 AWS 的镜像没有默认开启）。（`00:41:33–00:45:32`）

### 竞争、维护弃子项目与迁移的真实成本

Docker 推出硬化镜像（DHI）后的竞争话题，Matt 的回应是指控其自相矛盾：既声称基于 Alpine/Debian 构建，又声称一切从源构建——两者不可兼得。他复盘了自己与 CEO 在 Google 时代做 Distroless 镜像的历史（当时基于 Debian 包），结论是要做到零未修补 CVE 就不能站在发行版之上；对比扫描中，最新 Debian 镜像仍有未修补 CVE，而 Chainguard 等价镜像没有。（`00:29:33–00:31:43`）

EmeritOSS 计划针对"停止维护但仍承载关键负载"的项目：起因是 Google 的 Kaniko 停止合并 PR 并在约半年后归档，而大量机构依赖它构建镜像。Chainguard 接手的模式是只修安全问题、不做功能开发，把功能演进留给社区 fork——他还讲了 Jenkins 从 Hudson fork 出来的历史作为注脚。（`00:31:43–00:36:07`）

迁移焦虑被逐一拆解：Chainguard 用 apk 包管理器但刻意以 glibc 而非 musl 引导，换取与主流发行版的兼容；apt-get/yum 换成 apk add 即可，新的 gardener 工具借助 Agent 做包名映射；应用镜像通常即换即用，库类产品可以挂在 Artifactory/Nexus 代理后面切换上游，"开发者可能都没察觉"。作为滚动发行版，他们的销售话术是"最后一次迁移"。（`00:45:53–00:50:54`）

### Mythos 与 Fable：漏洞发现进入机器速度

录制前 24–48 小时 Anthropic 刚发布 Mythos 及其衍生模型 Fable。Matt 的判断很明确："这不只是营销"——Firefox 等项目用它找到了其他 Agent 工具找不到的大量漏洞，其最值得警惕的能力是把多个漏洞串联利用，正在实时拉低"发现并武器化漏洞"的技能门槛。他现场测试 Fable 时被自身的安全控制拦下并降级到 Opus 4.8，但他提醒控制总会被绕过。结论是防御侧必须具备"以机器速度打补丁"的能力——这恰是 Chainguard 多年构建的方向——并预期首批 Mythos 漏洞公开后的 6 到 12 个月会相当痛苦。（`00:50:54–00:54:11`）

## 来源与定位

- 原始节目：[AI-Powered Threats to the Software Supply Chain](https://softwareengineeringdaily.com/podcasts/ai-powered-threats-to-the-software-supply-chain/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Napster/Spotify 类比与产品模式演进（00:04:00–00:08:07）
  - 从源构建消除 98–99% 攻击来源与 CVE 爆炸（00:08:51–00:12:06）
  - XZ Utils 攻击复盘与纵深防御（00:12:06–00:17:17）
  - 灰件（grayware）准入思路（00:15:24–00:16:37）
  - .pth 拦截案例与内存安全组件替换（00:19:34–00:22:07）
  - CI/CD 攻击面、SLSA 缺失与 Octo STS（00:22:07–00:25:49）
  - 镜像规模、Agent 辅助测试与 KEV 24 小时 SLA（00:25:49–00:28:55）
  - 对 Docker DHI 自相矛盾主张的质疑（00:29:33–00:31:43）
  - EmeritOSS 与 Kaniko 故事（00:31:43–00:36:07）
  - SBOM 覆盖率、WordPress 测试与监管缺口（00:36:07–00:41:33）
  - 格式、深度与 Rust auditable 模式（00:41:33–00:45:32）
  - 迁移 FUD、gardener 工具与滚动发行（00:45:53–00:50:54）
  - Mythos/Fable 的真实能力与机器速度补丁（00:50:54–00:54:11）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 攻击案例细节、防御效果声明与竞争对比均保留为受访者说法，未作独立验证；"供应链安全"为本期新引入标签，预期用于后续同类节目。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
