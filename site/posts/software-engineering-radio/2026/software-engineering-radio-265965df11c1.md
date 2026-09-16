---
item_id: software-engineering-radio-265965df11c1
title: Martin Kleppmann 谈 Local-first：Git 的能力加 Google Docs 的易用，与"别把数据送去 us-east-1"
date: '2026-09-17'
published_at: '2026-04-15'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/04/se-radio-716-martin-kleppmann-local-first-software/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/04/se-radio-716-martin-kleppmann-local-first-software/'
summary: '《DDIA》作者、Automerge 联创 Martin Kleppmann 谈 Local-first 软件：离线可用与实时协作兼得、sync engine 把分布式问题沉入基础设施、自动合并取代 Git 式冲突解决、Key Hive 端到端加密，以及地缘风险下的去中心化价值。'
tags: [软件工程, 架构, 分布式系统]
---

# Martin Kleppmann 谈 Local-first：Git 的能力加 Google Docs 的易用，与"别把数据送去 us-east-1"

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-04-15 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6625 字 · 阅读约 17 分钟
>
> 标签：[软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) [架构](/tags/%E6%9E%B6%E6%9E%84/) [分布式系统](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/04/se-radio-716-martin-kleppmann-local-first-software/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/04/se-radio-716-martin-kleppmann-local-first-software/)

## 速读

《Designing Data-Intensive Applications》作者、剑桥大学副教授 Martin Kleppmann 与主持人 Adi Narayan 深聊 Local-first 软件:把前互联网时代"文件在你自己电脑上"的本地软件,与云时代的实时协作结合起来——数据同时存在你本地(谁也拿不走)并自动同步协作。Automerge 这个 CRDT 同步引擎是他给出答案。

最值得带走的三点:sync engine = 嵌入式数据库加复制协议,应用只与本地库交互,分布式系统问题被整体沉入基础设施;合并哲学是"自动合并、事后修补",不用 Git 式冲突解决界面,且确定性保证所有人合并出完全相同的状态;human-AI 协作可以当作另一种 human-human 协作——让 AI"对文档发 pull request",逐条 diff 审阅。

## 主题正文

### Local-first 是什么:两个世界取其优

Kleppmann 的定义从两代软件说起。前互联网时代的本地软件:程序跑在你的电脑上,文件存在你的电脑上,简单可靠;云软件带来了 Google Docs、Figma 式的实时协作,极其便利——但文件不再在你自己的电脑上,"一旦被锁在账号外面,你所有的文件都没了"。Local-first 要的就是两个世界之最:既有云软件的协作功能,数据同时又存在你自己的电脑上,"谁也拿不走"。红利有四:离线照常编辑、联网时实时协作、性能极佳(点击按钮不必等一次网络往返)、以及一个常被忽视的开发者红利——传统云开发要写前端、定义 REST API 或 WebSocket 协议、再写后端,层次繁多;Local-first 的目标是只建前端,同步与后端被抽象掉,小团队就能端到端交付;长期愿景则是为这类后端制定开放标准,让可插拔的后端按价格自由替换,不绑定任何一家公司。（原文锚点：`the data is also stored on your own computer locally`；`all of the data sync and backend is just abstracted away`）

### Sync engine:嵌入式数据库加复制协议

实现载体是同步引擎:可以把它理解为"一个数据库复制工具",在用户设备上的内嵌数据库(比如浏览器 local storage)与服务器数据库之间复制数据;你离线时只写本地,联网后与服务器及协作者双向同步。编程模型与 React 同构:UI 是模型对象的函数,只是这些对象不再是普通 JS 对象,而是同步引擎的状态——协作者的改动被引擎合并进本地副本,你只需重新渲染,"不用操心远程改动怎么合并,引擎已经合并好了"。最大的开发者红利由此而来:网络是讨厌的——咖啡店 Wi-Fi 不可靠,请求超时后你根本不知道数据到没到服务器,只能写大量的错误处理代码;sync engine 把网络通信从应用代码中整体移除,"把分布式系统问题下沉到基础设施里",编程模型被大幅简化。（原文锚点：`a sync engine as an embedded database plus a replication protocol`；`pushing these distributed systems problems down into the infrastructure`）

### 去中心化与本地网络:别把数据送去 us-east-1

同步引擎对服务器假设各有不同:有的假设传统中心服务器,Automerge 则为去中心化而生——可以用单一同步服务器,也可以多台服务器并存,甚至走点对点或蓝牙本地连接。Automerge 需要的只是"把字节从设备 A 送到设备 B"的某种途径;纯 P2P 有时不可靠、只靠它有危险,但把本地连接作为服务器之外的选项非常赋能:田野里的农民没有蜂窝信号,也想在手机和拖拉机之间同步数据——两台设备近在咫尺,就应该能直接同步。他金句总结:Local-first 里的 local 不只指本地存储,也指本地网络;"如果两台设备就摆在彼此旁边,还要把所有数据经由 AWS us-east-1 绕一圈,这有点荒谬"。离线协作的冲突问题则与 Git 同构——不同人离线改动同一处就会冲突;Automerge 用自动合并算法(CRDT 一族)处理,同一句子被两人编辑时能合并但无法保证语法正确,如何把这类冲突呈现给用户仍是 UX 层面的未解问题。（原文锚点：`It’s like asking how many users does Postgres have`之外的核心句——`if you have two devices that are physically close to each other, then they should just be able to communicate over a local network`；`we’ve had pretty good experiences using automatic merging algorithms`）

### Git 类比、CRDT 与 Automerge 的合并哲学

他给 Local-first 找的最贴切参照物是 Git:Git 完全符合 local-first——离线提交、离线改写本地历史,只有 push/pull 需要联网——开发者早已把这种能力视为理所当然;Automerge 的目标就是把 Git 式能力带给文本之外的其他文件类型与软件形态,因为 Git 对二进制无能为力("把电子表格放进 Git 只是二进制团块,两人分头改完,合并祝你好运"),而理想的形态是"Git 的能力,加上 Google Docs 的易用"。使能技术是 CRDT(无冲突复制数据类型):Google Docs 用的 operational transformation 自 90 年代初就有,但依赖单一中心服务器;CRDT 不做服务器假设——这正是他 2015 年读到此研究后入行的起点,此后多年都在打磨这些数据结构的效率与性能。Automerge 的定位是一个跑在浏览器或移动应用里的内嵌数据库/同步引擎:数据用 JSON 加少量扩展表示,每次编辑持久化到本地存储(浏览器里是 IndexedDB),网络协议负责在重连时算清该上传下载哪些变更;在线时实时转发给协作者,离线时本地缓冲。合并哲学与 Git 有意不同:没有显式的冲突解决步骤——"用过 Git 的人都讨厌解决合并冲突,那令人困惑甚至烧脑"——自动合并保证确定性(两人独立合并同样的改动,必然得到完全相同的状态),语义不佳就事后手工修补;未来的方向是工具化地"提示哪些合并值得复审",但"邻近"在文本、表格、图形应用里定义都不同,尚未破解。新文件类型接入 Automerge 需要映射到它的 JSON 模型(如同为关系库建模);它假设应用构建在 sync engine 之上,对没有这层的既有应用较难改造——成功案例是矢量绘图工具 tldraw,把其内部数据模型映射到 Automerge 文档后"相当容易"变成了协作应用。（原文锚点：`Git is totally Local-first`；`they’re called Conflict Free Replicated Data Types or CRDTs`；`every single keystroke becomes a commit`；`they will end up in exactly the same state`）

### 性能挑战、Key Hive 与端到端加密

多年的最大挑战是性能与内存: Automerge 像 Git 一样保留完整编辑历史——可以回看任意历史版本、可以 diff"同事上周你度假时改了什么"——但要支撑实时协作,每次击键都是一次提交,Git 式做法会荒谬地低效;内部数据结构的工程打磨花了好几年。规模定位的设计目标直指"维基百科级协作";不过大规模协作真正的难题在权限与人的协调(公开可编辑必然招来破坏),那不是 Automerge 这个同步引擎能解决的。解法是配套的 Key Hive——加密访问控制系统(开发约一年,尚未就绪):Google Drive 式的权限(授权某个文件夹、可撤销、可按团队授予),但不依赖单一可信服务器;为每台设备生成独立密钥对,由创建者把访问权委托给密钥或密钥组,权限校验系统判定"这条编辑是否来自被授权者"——全程无需中心服务器。密钥体系顺带带来了端到端加密:同步服务器完全看不到文档内容,只有用户设备能解密——"本质上是要把 Signal、WhatsApp 式的端到端加密带到文件编辑上"。（原文锚点：`we are working on a cryptographic access control system called Key Hive`；`the sync servers can’t actually see the content of the documents at all`）

### 边界、搜索、备份与"复杂度税"之辩

Local-first 并非万能。它最适合"用户可以随意编辑数据"的应用——文本编辑器、表格、绘图;不适合管理现实世界资源的应用——银行账户里"我可以给余额末尾加个零,但银行才不会理会我的编辑";大数据集也不合适——电商把整个商品目录同步到每台设备没有意义,用户只关心其中的微小片段,传统按页取用的 Web 方式反而合适。对"复杂度税"的疑问,他的回答反直觉:希望是更容易而非更难——CRDT 的细节是应用开发者永远不必操心的(Automerge 官网几乎不提这个词),真正的采用门槛只是"学习一个新模型"的切换成本。搜索与备份两个常见质疑他也有答案:要离线搜索,搜索就得在客户端(他举 Obsidian 为例——多年笔记在击键间即可命中;服务端搜索的规模化其实比客户端更难),Automerge 与搜索引擎的集成是未来投入点;设备丢失问题则由同步服务器的备份职能兜底——P2P 场景下也该有个"备份 peer"——而云备份作为"纯粹的老实存储"完全受鼓励,只是别依赖它做协作与检索。（原文锚点：`If with a bank account I could edit the bank account balance and add an extra zero at the end, but the bank is not going to pay any attention`；`making a client-side search engine`；`it’s just very straightforward storage`）

### AI 协作、地缘风险与去中心化的新价值

AI 与 Local-first 意外地相互成全。其一是架构:Local-first 只建前端、部件更少,"vibe coding 一个完整应用并让它跑起来"反而更容易。其二是更漂亮的结合:AI 与人的协作,本来就是人与人社协的另一个实例——让 AI agent 改写你写的文档时,你肯定想审阅它的每一处改动,于是"AI 对你的文档发起一个 pull request,你可以看到 diff,逐条接受或拒绝",复用的正是为人类协作准备的版本控制与变更追踪设施——"这原本不在计划里,但在 AI 时代它工作得出奇地好"。已有数十款自我标榜 local-first 的产品,设备端开源模型也让"离线的 AI 功能"成为有前途的方向。而他个人最看重的推力,是摆脱对单一供应商的依赖:被自动化系统以违反服务条款为由锁在 Google 账号之外时,"祝你好运能找到一个真正的 Google 人类员工"——知道有一份谁也拿不走的本地副本,这是他最在意的底气。更宏观的担忧是地缘政治:欧美围绕格陵兰的紧张关系让他意识到,欧洲高度依赖美国云服务,"如果某道行政命令突然限制欧洲企业访问美国云服务呢?这本来不可想象,现在已经不再不可想象"。Local-first 与去中心化的价值正在于此:多台服务器、不同公司、不同国家托管,倒了一家的其它还在——"用稍微松弛一些的模型,抵御这类地缘风险"。资源入口:automerge.org、Ink & Switch 上的 2019 年 Local-first 论文、local-first.fm 的 landscape 目录,以及他个人网站上的论文列表;《DDIA》新版电子书已出,纸质版 2026 年 3 月上市。（原文锚点：`the AI makes a pull request against your document and you get to see a diff`；`good luck getting ahold of an actual human being at Google`；`a year ago it would’ve been unthinkable and now it’s unfortunately no longer unthinkable`）

## 来源与定位

- 原始节目：[SE Radio 716: Martin Kleppmann on Local-First Software](https://se-radio.net/2026/04/se-radio-716-martin-kleppmann-local-first-software/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - Local-first 定义：两代软件取其优与"谁也拿不走"（`the data is also stored on your own computer locally`）
  - 只建前端、同步与后端被抽象掉（`all of the data sync and backend is just abstracted away`）
  - sync engine 编程模型与 React 同构（`a sync engine as an embedded database plus a replication protocol`；`pushing these distributed systems problems down into the infrastructure`）
  - 本地网络即协作通道与 AWS us-east-1 之喻（`if you have two devices that are physically close to each other, then they should just be able to communicate over a local network`）
  - Git 是完全的 local-first 与 CRDT 入场（`Git is totally Local-first`；`they’re called Conflict Free Replicated Data Types or CRDTs`）
  - 合并哲学：自动合并、确定性结果、无显式冲突解决（`they will end up in exactly the same state`）
  - 性能与内存的多年打磨：每次击键都是一次提交（`every single keystroke becomes a commit`）
  - Key Hive 加密访问控制与端到端加密（`we are working on a cryptographic access control system called Key Hive`；`the sync servers can’t actually see the content of the documents at all`）
  - 适用边界：银行账户与大商品目录的反例（`If with a bank account I could edit the bank account balance and add an extra zero at the end`）
  - 搜索与备份：Obsidian 例与"老实存储"（`making a client-side search engine`；`it’s just very straightforward storage`）
  - AI 协作即 pull request 评审（`the AI makes a pull request against your document and you get to see a diff`）
  - 供应商锁定、地缘风险与去中心化收尾（`good luck getting ahold of an actual human being at Google`；`a year ago it would’ve been unthinkable and now it’s unfortunately no longer unthinkable`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 嘉宾姓名（Martin Kleppmann）与主持人（Adi Narayan）按节目出版方元数据核正；《DDIA》新版上市时间（电子书已出、纸质版 2026 年 3 月）与"30 万册销量"为嘉宾/主持人口述口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
