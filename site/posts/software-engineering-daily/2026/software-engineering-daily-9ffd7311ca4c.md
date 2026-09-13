---
item_id: software-engineering-daily-9ffd7311ca4c
title: '限量发布的"安全模型"与 7000 亿资本开支：SED News 五月刊'
date: '2026-09-14'
published_at: '2026-05-07'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/sednews-anthropics-mythos-supply-chain-hacks-and-the-ai-spending-surge/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/podcasts/sednews-anthropics-mythos-supply-chain-hacks-and-the-ai-spending-surge/'
summary: 'Gregor Vand 与 Sean Falconer 的半月新闻：Mythos 限量发布与 Project Glasswing 的稀缺营销、Roblox 外挂引发的 Vercel 供应链渗透、Snap 与 Meta 裁员的两种叙事、7000 亿美元 AI 资本开支下的芯片锁定，以及"安全默认"为何总欠账。'
tags: [企业 AI, 安全, 开发者工具]
---

# 限量发布的"安全模型"与 7000 亿资本开支：SED News 五月刊

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-05-07 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-14
>
> 全文共 4019 字 · 阅读约 11 分钟
>
> 标签：[企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/) [安全](/tags/%E5%AE%89%E5%85%A8/) [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/sednews-anthropics-mythos-supply-chain-hacks-and-the-ai-spending-surge/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/podcasts/sednews-anthropics-mythos-supply-chain-hacks-and-the-ai-spending-surge/)

## 速读

SED News 五月刊的三条主线：Anthropic 的 Mythos 安全模型以 Project Glasswing 名义只向少数大公司开放、声称能自主发现各大操作系统与浏览器里的历史漏洞；context.ai 员工因下载 Roblox 游戏外挂中招窃密木马、攻击链一路渗透进 Vercel 内部系统；以及 6500–7000 亿美元的年度 AI 资本开支盘点与"芯片路线锁定"。

最值得带走的三点：稀缺本身就是营销——"AI 界的爱马仕铂金包"效应让限制发布反而制造需求；安全工程的老毛病是"没有把安全设为默认值"，Snowflake 与 Vercel 的补救都是事后补课；以及一个年轻人会关心的数据——软件工程开放职位同比翻倍，IBM 还在扩大初级工程师招聘。

## 主题正文

### Mythos 与 Project Glasswing：安全模型的稀缺营销

头条是 Anthropic 的 Mythos：一个以安全为核心定位的大模型，宣称能自主发现各大操作系统与浏览器中此前未知的漏洞——尤其擅长挖掘深藏在遗留软件里几十年的老 bug，节目里举的招牌案例是 OpenBSD 一个存在 27 年的缺陷；它还能执行人类需要数天到数周的多步网络攻击。正因如此，发布方式被设计得极其克制：只向 Amazon、Apple、Microsoft、JPMorgan Chase 等主要科技与金融公司开放，项目代号 Glasswing，逻辑是"在坏家伙之前修补关键漏洞"（`00:04:20–00:06:11`）。Sean 给这个策略起了个精辟的类比：这是"AI 界的爱马仕铂金包"——稀缺制造需求。"就算不是精心设计的营销，当你告诉所有人这东西太危险不能随便用、只有最大的公司能用时，需求反而被点燃了。"关于有承包商把模型访问权流出到暗网的传言，Anthropic 断然否认、称没有任何证据；两位主持人也提醒这类"未经验证的声明"本身可能就是骗局——收了钱跑路的生意（`00:08:41–00:09:24`）。

技术上真正令人震撼的是那个 27 年的 OpenBSD 漏洞。Sean 的感慨是这属于"人类被 AI 击败的又一座里程碑"——从 Kasparov 输给深蓝、DeepMind 击败围棋世界冠军，到现在一个模型找到了数千名顶尖工程师几十年间亲手维护却始终视而不见的缺陷（`00:09:24–00:10:24`）。Gregor 的补充同样扎心：遗留软件之所以是遗留软件，就是因为再聪明的工程师也不会回去逐行翻 27 年前的代码——"你默认它能工作，也默认如果有问题早被发现了。显然并非如此"。后续值得追踪的是 Glasswing 的准入名单怎么扩展。

### 供应链渗透：Roblox 外挂、Vercel 与"安全默认"的老毛病

第二条线是 context.ai 数据泄露事件，攻击链堪称教科书级社工：一名员工下载了伪装成 Roblox 游戏外挂的 Luma stealer 木马， harvested 的凭据包括 Google Workspace、Datadog 等；攻击者随后用失窃的认证令牌跳板进入一名 Vercel 员工的 Workspace 账号，再渗入 Vercel 内部系统。Gregor 所在的 Supabase 仪表板正托管在 Vercel 上，团队连夜做了一整轮凭据轮换（`00:10:24–00:12:38`）。Sean 把这类攻击归为经典的人类漏洞——从 2000 年代的 Anna Kournikova 病毒到 Roblox 外挂，"总会有一部分人去点那个东西"。Vercel 的事后整改是把新环境变量默认标记为敏感并自动静态加密，Sean 借此发问：为什么这不是从一开始的默认值？他连到了 Snowflake 事件的同一模式——承包商本就有合法访问权、只是没有强制 2FA，事后 Snowflake 把 2FA 设为强制——"公司一次次没能把 secure by default 变成真正的默认"。原因大概是从不缺"以后再处理"的理由：安全功能不产生收入，等它成为新闻头条时已经太晚（`00:12:38–00:15:56`）。还有一个耐人寻味的插曲：为 context.ai 出合规认证的 Delve 此前被举报伪造合规证书，而如今两个月内两家被攻破的公司都是 Delve 的客户——Sean 拒绝戴锡纸帽："样本太小。如果五个月后每个月都有 Delve 相关的泄露，我来加入你的阴谋论圈。"

### Snap 与 Meta：两种裁员叙事与 AI 资本开支的宏观盘点

宏观面上，Snap 裁员约 1000 人（约 16% 员工），Evan Spiegel 的口径是"到了必须盈利的关键时刻"，将加倍投入 AI 与 Specs 眼镜这一 moonshot；Meta 裁员约 10%（约 8000 人）并冻结 6000 个开放岗位，叙事则直白得多——"为 AI 投资让路"。Gregor 表示欣赏后一种诚实："这就是大家一直想听的：你在 AI 基础设施上亏的钱总要找地方补。"Sean 则分析了上市公司在转型期的两难：既要在生存级的范式转变上下大注，又要在财报的放大镜下保住利润——有 Google 那样印钞主业的公司可以养创新分支，小一点的公司就得有所取舍（`00:17:30–00:24:01`）。他顺带抛出了那 个越来越现实的问题：当社交平台的喂料由 AI 生成、排序由 AI 策展、广告由 AI 优化、而内容审核的人力也正被 AI 替代时——"这个循环里还剩下谁是人类？用户注册的到底是什么？"

主话题是 AI 资本开支的全景盘点：据摩根士丹利报告，2026 年 Amazon、Google、Meta、Microsoft 四家的 capex 合计约 6500–7000 亿美元；单周内 Google 承诺向 Anthropic 投入至多 400 亿美元、Amazon 承诺 50 亿并附十年约 1000 亿美元的 AWS 支出、NVIDIA 市值突破 5 万亿。Gregor 用"垂直整合"概括格局：模型实验室正在变成基础设施租户——Anthropic 的千亿 AWS 承诺意味着训练与推理可能与 Amazon 的芯片路线（Graviton）结构性绑定；OpenAI 深度绑定 Azure；Google 自家 TPU；Meta 确认将使用数十万颗 AWS Graviton 芯片。这些绑定像当年 Apple 从 Intel 迁移到自研芯片一样难以掉头。Sean 的总结是"这个行业已经大到没有任何一家能完全自包含"——竞争者之间同时互相依赖，从芯片、云、模型到应用（`00:24:53–00:30:04`）。人才侧的数字则反直觉：TrueUp 统计 9000 家科技公司有 6.7 万个软件工程开放职位，自 2023 年中的低点翻倍；IBM 把初级工程师招聘扩大两倍，理由是"AI 原生一代上手这些工具最快"——Sean 担心的是如果人人都只招 senior，"未来的 senior 从哪来"（`00:30:29–00:33:38`）。

安全面的收尾数据来自 Cisco 的 2026 AI 安全状态报告：83% 的组织计划部署 agentic AI，但只有 29% 表示有信心保护它。Gregor 的观察是领导层普遍在"说 yes"的压力下放宽工具权限——"如果 CTO 说工具不能碰邮箱不能碰 Slack，那要它干嘛？"——攻击面因此比安全工具的进化速度快得多（`00:33:38–00:37:45`）。Sean 补充的缺口则指向生成代码的下游：大量资金涌向代码生成工具压缩了 POC 时间，但从 POC 到生产的验证、测试环节没有同步加速——"我们总得找到加速它的办法，否则生成速度的红利兑现不了"。Hacker News 环节的推荐包括：按都会区统计的美国性别比例数据可视化、一篇"用编码助手复活你永远不会完成的项目"的博客（"书架上少了一本隐喻的书"）、IBM Granite 4.1——80 亿参数以数据质量优先的训练管线打平自家 320 亿 MoE 模型且全部 Apache 2.0 开源——以及 Chalkdust 杂志那篇"如何在俄罗斯方块中作弊"的数学分析：如果你能指定对手的方块序列，哪些组合可以数学上保证对方必输（`00:40:07–00:48:49`）。

## 来源与定位

- 原始节目：[SED News: Anthropic's Mythos, Supply Chain Hacks, and the AI Spending Surge](https://softwareengineeringdaily.com/podcasts/sednews-anthropics-mythos-supply-chain-hacks-and-the-ai-spending-surge/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Mythos 的能力口径与 Project Glasswing 限制发布（00:04:20–00:06:11）
  - "铂金包"稀缺营销与暗网传言的核实（00:06:11–00:09:24）
  - OpenBSD 27 年漏洞与"人类被 AI 击败"的里程碑（00:09:24–00:10:24）
  - Roblox 外挂到 Vercel 的供应链渗透链（00:10:24–00:12:38）
  - secure by default 的老毛病与 Snowflake 先例（00:12:38–00:15:56）
  - Delve 合规认证的疑云（00:15:56–00:17:30）
  - Snap 与 Meta 裁员的两种叙事（00:17:30–00:22:50）
  - 社交平台的 AI 循环之问（00:19:08–00:21:23）
  - 7000 亿资本开支、垂直整合与芯片路线锁定（00:24:53–00:30:04）
  - 工程职位翻倍与"AI 原生初级工程师"的招聘转向（00:30:29–00:33:38）
  - 83% 部署 agentic AI 对 29% 有信心保护的缺口（00:33:38–00:37:45）
  - 代码生成繁荣下的验证与测试缺口（00:38:35–00:39:22）
  - HN 精选：性别比例可视化、复活弃坑项目、Granite 4.1 与俄罗斯方块作弊数学（00:40:07–00:48:49）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字与传闻（漏洞年限、裁员规模、资本开支、估值传闻等）仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
