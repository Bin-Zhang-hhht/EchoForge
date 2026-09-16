---
item_id: software-engineering-radio-3d8c8af0cbe0
title: Dan Lorenc 谈 Sigstore：给开源供应链装上"防拆封条"，让签名像 HTTPS 一样普及
date: '2026-09-17'
published_at: '2026-03-18'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/03/se-radio-712-dan-lorenc-on-sigstore/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/03/se-radio-712-dan-lorenc-on-sigstore/'
summary: 'Chainguard CEO Dan Lorenc 讲透 Sigstore：npm 与 GitHub 之间缺失的密码学链接、Shai-Hulud 蠕虫的醒悟时刻、Fulcio/Rekor 组件与透明日志的"以透明换信任"，以及 Let''s Encrypt 式愿景——让签名免费、简单、自动。'
tags: [安全, 开源, 软件工程]
---

# Dan Lorenc 谈 Sigstore：给开源供应链装上"防拆封条"，让签名像 HTTPS 一样普及

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-03-18 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6378 字 · 阅读约 16 分钟
>
> 标签：[安全](/tags/%E5%AE%89%E5%85%A8/) [开源](/tags/%E5%BC%80%E6%BA%90/) [软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/03/se-radio-712-dan-lorenc-on-sigstore/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/03/se-radio-712-dan-lorenc-on-sigstore/)

## 速读

软件供应链安全公司 Chainguard 的联合创始人兼 CEO Dan Lorenc 重返 SE Radio,与主持人 Priyanka Raghavan 聊 Sigstore——为开源设计的大规模代码签名体系。他从 npm 的 Shai-Hulud 蠕虫讲到 Sigstore 的三组件(cosign/Fulcio/Rekor)与透明日志,核心类比是:Sigstore 之于软件供应链,就像 Let's Encrypt 之于 HTTPS,又像酱料瓶上那个防拆封条——它不保证原料好坏,只证明封条未被拆动。

最值得带走的三点:开源的法律定义只覆盖源码,而你安装的是从 npm/PyPI 下载的构建产物——两者之间没有任何链接,这正是攻击者反复利用的缝隙;签名本身什么都不做,"只有人们在验证它才有意义";及一条最实务的建议——永远不要从个人笔记本发布任何东西,一切产物必须出自受保护的构建系统。

## 主题正文

### 供应链攻击为什么是"从后门进门"

Lorenc 的定义直白:软件供应链是"做成你手上那个最终软件的全部工具、步骤、库与原料";攻击则是攻击者利用链条上某个环节的漏洞拿到最终产物的执行权——"不再从正门黑进系统,而是从供应链这个后门进来,而一旦代码进了最终产品,就 game over 了"。为什么今天尤其严重?正门已经被修得太好:双因素认证、登录短信,这些几年前只有安全关键机构才用的东西如今无处不在;攻击者于是转向下一个最薄弱的入口——供应链;与此同时开源进入了最敏感的环境,攻击面大增。（原文锚点：`once you get code into that finished product, it’s game over code execution`；`they pivot to the next easiest way, which is the supply chain`）

### Shai-Hulud:一场让行业醒来的蠕虫

去年年底 npm 上的 Shai-Hulud 攻击(名字是攻击者自己取的——检测特征就是它创建的同名公开仓库)值得细讲:攻击者先通过常规的维护者账号接管攻陷了几个包,然后不再满足于攻击这几个包,而是放出一条自复制蠕虫——被感染包会窃取你的 npm 发布凭证,再把恶意代码注入你发布的所有包,指数级扩散。"双位数百分比的互联网生态很快被波及。"npm 摘除后攻击者又回来了两三次(Shai-Hulud 一、二、三)。之所以是行业警钟,一是因为传播速度,二是因为这是最早"偷凭证而非只挖矿"的大型攻击之一——此前的攻击多半只是装挖矿程序,"电费涨一点,还不是世界末日";而拿到代码执行后,勒索、窃密,什么都做得出来。（原文锚点：`it was a self-replicating worm in the npm registry`；`it was one of the first ones that stole credentials in that way`）

### Sigstore 是什么:缺失的那段密码学链接

Sigstore 针对的缝隙非常具体:开源的法律定义(OSI 认证)只约束源代码,而组织消费开源的方式是从 npm/PyPI 安装构建产物——"审了 GitHub 上的源码说不含恶意代码,装下来却 boom,里面全是恶意软件,因为有人在那一步塞了进去"。源码与安装包之间没有任何链接。Sigstore 提供的正是这段密码学链接:由人或构建系统签名,声明"这个 npm 包确实来自这份源码"。他强调这不是第一个做签名阴影保护的体系(PGP 的 key signing party 是前辈),类比是食品工业的防拆封条:它不告诉你原料好不好、有没有过期,只告诉你"运到你手上时封条没被拆"——是加固供应链诸环节中的重要一环。这套体系同样适用于企业内部供应链(内部人员风险、双人复核),也能在其上构建更高层的信任系统(Rekor 账本让"Dan 说这个软件没问题"这句话本身可被密码学验证)。（原文锚点：`this npm package actually came from this piece of source code`；`it’s like that, tamper proof seal on the jar of pasta sauce`）

### Let's Encrypt 楷模:免费、简单、自动

Sigstore 的设计深受 Let's Encrypt 启发,甚至他认为 Let's Encrypt 某种程度上"导致"了供应链攻击的兴起——它把 HTTPS 证书从"填表格、找注册商、签支票"的繁琐流程变成免费自动化,互联网加密率从低两位数百分比涨到接近 100%,浏览器开始强制要求。代码签名此前正处于同样尴尬的境地:证书难拿、开源几乎无签名、拿到了也没人验证。Sigstore 的方法论一致:"免费、简单、自动",让开发者愿意签名,直到"下载未签名的东西反而显得奇怪"的那一天。（原文锚点：`encryption on the internet went from low double digits to close to a hundred percent`；`make it free, make it easy, and make it automatic`）

### 组件拆解:身份即邮件地址,三种工具各司其职

签名与证书归结到底都是身份问题——证书把"一长串随机数"(私钥)绑定到某个身份:人名、假名、GitHub 账号、邮箱或某个构建系统。开源的身份根基选的是 OIDC(OpenID Connect,就是"使用 Google 登录"那个按钮背后的协议):维护者的邮箱地址是信任链的根;签名时按需签发一次性临时证书,开发者从此不必管理"密钥泄漏了怎么办"。身份提供方可插拔(GitHub 账号、企业内部的 Active Directory/Okta 皆可);签名对象本质上是摘要而非工件本身——容器、Python 包、一条推文、一封邮件皆可。三件工具各司其职:cosign 签容器(另有 Python、Node 版本),Fulcio 做身份校验(点击"Sign in with Google"弹窗的那一环),Rekor 是透明日志账本。"任何人都能签名,但它只有在人们验证时才有意义"——验证会告诉你"是哪个邮箱签的",至于你是否信任那个邮箱,Sigstore 管不了。（原文锚点：`this temporary certificate that’s just used for signing that one piece of code`；`anyone can sign something, but it only works if people are checking those signatures`）

### 透明日志:以透明换信任

整套体系的底座是透明日志(transparency logs)——Let's Encrypt 与全球所有 HTTPS 证书都在用的密码学原语:一个"可以证明长期未被篡改、且所有人看到同一份"的追加式账本。你签名时得信任 Sigstore 不作恶、不被攻陷;透明日志让这种信任不再必要——签名必须出现在账本里才能通过验证,"以透明换信任";每个签名者的邮箱出现新签名时会有自动邮件提醒("如果那天你什么都没发布,这就是大红警报");出事时凭借时间戳可以精确追责——"100 个签名里 99 个有效且确实是你,只有这一个是假的",无需全盘作废。它与区块链神似但用途不同;Google 打开首页时信任的证书机构,同样是靠监控透明日志来防滥用——在"民族国家资助大规模网络攻击"的世界里,"信任来自透明"是整个生态的立足点。Fulcio 与 Rekor 由 OpenSSF(Linux 基金会旗下)运营为公共善益实例,值班的是来自各公司志愿者的轮班团队(Chainguard 也有人参与);企业若不想暴露部署频率等信息,可自建实例。CI/CD 场景则用工作负载身份:不问"服务器的邮箱是什么",而是"只有这个云区域里这个 K8s pod、这个仓库这个分支上的 GitHub Action 允许发布"——AI agent 同理(签名模型、验证 Hugging Face 上下载的是不是真模型也是同一套原语,Google 已为自家 ML 模型全面签名)。（原文锚点：`there’s this append only ledger that you can prove hasn’t been tampered with over time`；`So it’s kind of trust through openness`；`you can say, this GitHub action running from this repository on this branch is allowed to publish into this registry`）

### Typosquatting 与 Unicode 陷阱

一个容易被忽视的细节:打印出"签名邮箱"供人肉眼核对其实并不安全——Unicode 里有长得一模一样的字符变体,"我今天就能注册一个看起来和你的一模一样、中间藏了个特殊字符的邮箱"。Sigstore 已修改默认行为:不再让你"看",而是要求你输入期望的邮箱地址,系统回答"是/否有这个地址签过"。typosquatting 攻击一直都在,这类细节很 subtle 但值得较真。（原文锚点：`I could go make an email address today that looks just like yours but with like a Unicode character in the middle`）

### 实务建议、Chainguard 与 AI 前景

小团队最容易落地的一步:"永远不要从个人笔记本发布任何东西"——迁到构建系统,要求所有进入生产环境的产物出自那里;构建系统当然也要保护,但它的攻击面远小于"每个人的笔记本",还会倒逼出一整套发布卫生习惯。入门最简单的路径是下载 cosign,`cosign sign` 加容器名即可,GitHub Actions、GitLab 与主流 CI 都有现成流程。签名很容易("每次构建多跑一条命令"),难的是后半段——让消费者真的去验证;签名本身不阻止 Shai-Hulud 式攻击,但如果首批被攻陷的包维护者当时在签名,"那些冒名上传的签名是不会通过验证的"——维护者无法替消费者自保,但可以让自保成为可能。他也在 Chainguard 实践整体方案:从源码重建 2000 多个容器镜像(全程 Sigstore 签名、SLSA 标准)、自动化补丁生命周期(Log4j 式漏洞无需人工追赶)、并按 CIS/Stig 基线提供加固档位——默认安全(无 shell),也提供带 shell 与包管理器的完整版本,毕竟"生产环境里没有 shell 的容器出问题时极难调试",这是一个光谱而非开关。对 AI 的展望双面并存:写软件的人与软件都会暴增,漏洞也随之暴增;但"同一批系统也能检查与修复安全问题,agent 永远不会累"——前提是别把 agent 生成的代码不加验证地直接推上生产。他预计各环节最终都会有专属 agent(选镜像、做验证),而这些 agent 的机器身份正是本期讨论的工作负载身份的延伸。（原文锚点：`don’t ever publish anything from people’s laptops`；`Signing does nothing by itself. But if people are checking them.`；`there’s a lot of slop published and all of that stuff. But I think over time it’s just going to improve things for everyone`）

## 来源与定位

- 原始节目：[SE Radio 712: Dan Lorenc on Sigstore](https://se-radio.net/2026/03/se-radio-712-dan-lorenc-on-sigstore/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 供应链攻击定义与"后门"逻辑（`once you get code into that finished product, it’s game over code execution`；`they pivot to the next easiest way, which is the supply chain`）
  - Shai-Hulud 蠕虫：凭证窃取、自复制与二次三次返场（`it was a self-replicating worm in the npm registry`；`it was one of the first ones that stole credentials in that way`）
  - 源码与安装包之间的缺失链接（`there’s no direct link from the source code that is up on GitHub to the open-source package`）
  - 防拆封条类比与 PGP 前辈（`it’s like that, tamper proof seal on the jar of pasta sauce`）
  - 内部供应链与 Rekor 账本上的高阶信任系统（`Sigstore can be used in that way too`；`The Ledger, which is a core component of Sigstore`）
  - Let's Encrypt 楷模与"免费、简单、自动"（`encryption on the internet went from low double digits to close to a hundred percent`）
  - OIDC 身份根、临时证书与可插拔 IdP（`this temporary certificate that’s just used for signing that one piece of code`）
  - cosign/Fulcio/Rekor 分工与"签名易、验证难"（`anyone can sign something, but it only works if people are checking those signatures`）
  - 透明日志、以透明换信任与精确追责（`there’s this append only ledger that you can prove hasn’t been tampered with over time`；`So it’s kind of trust through openness`）
  - 公共善益实例、工作负载身份与 AI agent/模型签名（`this GitHub action running from this repository on this branch is allowed to publish into this registry`）
  - 采用版图：Kubernetes、PyPI trusted publishing、npm 与 Maven Central（`The Kubernetes project signs all of their release artifacts with Sigstore`）
  - Typosquatting 与 Unicode 同形字陷阱（`I could go make an email address today that looks just yours but with like a Unicode character in the middle`）
  - "别从笔记本发布"、Chainguard 模式与 AI 展望（`don’t ever publish anything from people’s laptops`；`there’s a lot of slop published`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 嘉宾姓名（Dan Lorenc）与主持人（Priyanka Raghavan）按节目出版方元数据核正；Shai-Hulud 攻击、Salesforce/Codecov 等事件均为节目转述的公开事件，细节以原始报道为准；"双位数百分比生态受影响"等为嘉宾记忆口径。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
