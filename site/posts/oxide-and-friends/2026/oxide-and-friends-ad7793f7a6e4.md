---
item_id: oxide-and-friends-ad7793f7a6e4
title: 死无对证的针式打印机：Oxide 信任根背后的密钥仪式
date: '2026-11-01'
published_at: '2026-10-24'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: 'https://share.transistor.fm/s/226b1683'
source_name: 'Oxide and Friends'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/226b1683/transcription'
summary: 'Oxide 复盘 2023 年首台产品出货前的密钥仪式：信任根依赖的 PKI 当时并不存在，制造秘密一旦泄露，任何人都能冒充 Oxide 软件。节目完整还原仪式设计——签名密钥只在 HSM 内生成、认证值分片打印到纸面、执行机拆掉无线、分片存入银行保管箱——以及防篡改袋贴错、形同塑料袋后连夜返工重做的全过程。'
tags: [安全, 硬件, 供应链安全]
---

# 死无对证的针式打印机：Oxide 信任根背后的密钥仪式

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-10-24 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 12241 字 · 阅读约 31 分钟
>
> 标签：[安全](/tags/安全/) [硬件](/tags/硬件/) [供应链安全](/tags/供应链安全/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/226b1683) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/226b1683/transcription)

## 速读

Oxide 复盘 2023 年首台产品出货前的密钥仪式：信任根依赖的 PKI 当时并不存在，制造秘密一旦泄露，任何人都能冒充 Oxide 软件（`you could spoof Oxide software`）。节目完整还原仪式设计——签名密钥只在 HSM 内生成、认证值分片打印到纸面、执行机拆掉无线、分片存入银行保管箱——以及防篡改袋贴错、形同塑料袋后连夜返工重做的全过程（`do we have to do this again`）。这期适合所有关心「供应链信任最终落在哪把钥匙上」的工程师：从 IANA 的 DNS 根密钥仪式到 Caliptra 的新一代信任根思路，这是一堂把安全从口号落到道具清单的公开课（`root signing keys for DNSSEC infrastructure`）。对话三方为 Oxide 的 Bryan Cantrill、Adam Leventhal，与在 Oxide 负责信任根工作的特邀嘉宾 Philip Tricca。

## 主题正文

### 硬件不再拖延：一笔到期的安全债

节目从 Adam 与 Bryan 交换 Elizabeth Holmes 纪录片的观后感开场（`the Elizabeth Holmes documentary`），Bryan 随后把话锋从「装出来的成功」拧向反面：一项 Oxide 从未公开谈过、也几乎注定不被看见的工作——给产品打信任地基。时间拨回 2022 年秋：Oxide 给机架上电，「一半的 sled 当场烧毁」，团队自嘲地称之为「mass casualty event」（`half the sleds blew out`，`the mass casualty event`）。软件团队当时还在玩 schedule chicken——每个人都默认别人是进度的长杆，结果「硬件没有眨眼」（`Hardware did not blink`）。1 月又订上了一次合规测试，Bryan 说自己在 all-hands 上把话挑明：硬件一旦就绪，我们就发货。

就在兑现这句话之前，Philip Tricca 意识到自己坐在一个火山口上：信任根当时已经能跑到「某种程度上可用」，但「我是公司里唯一在依赖一个还不存在的 PKI 构建东西的人」（`relied on a PKI that did not yet exist`）。他解释，计算机安全最令人失望的一点，是一切最终都归结为 PKI：某个持有私钥的实体做出断言，而这套东西的全部安全属性都取决于那把钥匙的保密（`everything seems to boil down to PKIs`）。

利害关系值得展开。制造 sled 时，Oxide 会用一个秘密对设备 ID 做编码；从设备 ID 反推不出秘密，但如果秘密本身失守，就可以冒充 Oxide 软件（`use an oxide secret to encode a device ID`，`you could spoof Oxide software`）。Bryan 补上更直接的一层：一旦有人拿到 Oxide 的签名钥匙，对所有在意 sled 上运行什么软件的人来说都是极坏的消息，「我们就可以被有效地冒充」（`we can now be impersonated effectively`）。物理封存倒是扎实：钥匙存在信任根芯片的内部 flash 里，没有外部芯片、没有对外通信能把它带出「信任根的信封」（`stored in the internal flash on the part`）；Adam 强调它不是那种可以拆焊导出的外挂 flash（`desolder and and exfiltrate`）。但 Phil 的结论依然成立：信任根之外，还需要一套体量相当的系统来建造并维护，而它必须在第一台产品出货前就存在。

### 最低线思维：不求完美，但要经得起审计

「必须完美」的压力是真实的，Phil 却当场拆掉了这个标准：「它不可能完美」（`it can't be perfect`）；如果拿完美来定义完成，「我们可能永远发不出第一台产品」（`perfection is how you define done`）。能定下的是结构性底线：任何参与者都不能在其他人不知情时单独破坏系统，至少要两人合谋才可能得手（`two parties involved collude`）。更深一层是心态：要为成功做规划——如果公司真的跑起来、开始大量出货，第一台产品的安全属性必须与未来造的同样可信（`To plan for success`）。

行业的反面教材不缺。产线上要给钥匙做认证时，常见的省事办法是在平台外生成钥匙再注入进去（`create it outside the platform and then inject it`）；Phil 猜想，创业公司的 PKI 是「某人书桌抽屉里优盘上的未加密钥匙」的数量「恐怕远大于零」（`sitting on a thumb drive in someone's desk drawer`）。Bryan 点破精益创业方法论在这里的失效：产品可以迭代，但这套东西「你要与之共处非常、非常久」（`live with for a really, really, really long time`）。麻烦在于，这条最低线没有任何人替你定义，从业者对此讳莫如深，只能自己选（`the minimum bar isn't really defined`）；Oxide 给自己定的那条朴素得近乎寒酸——「钥匙不能放在某人的桌子里」（`our minimum bar was not having keys in someone's desk`）。

Phil 的大厂履历恰好反衬出创业公司的处境：在 Intel，PKI 办公室「大概从八十年代就存在」（`their PKI office has been around since probably the eighties`）；而在 Oxide，「突然之间你得自己来」（`suddenly you gotta do it yourself`）。公开资料几乎为零，他找到的唯一好材料来自 IANA——归档转写把这个名字拼作 "Ayanna"——这个掌管 DNSSEC 根签名钥匙的机构把自己视作公共品来经营，对流程极度透明（`the only good resources I could find publicly`，`root signing keys for DNSSEC infrastructure`）。他们的签名仪式有录像、脚本可下载、全程可查（`they record their signing ceremonies`，`You can get the scripts`）。Phil 说，正因为了解其流程，他作为互联网用户反而更信任那套系统——这正是 Oxide 想给客户的东西：透明是信任的前提，你必须知道自己信的是什么（`Transparency is a prerequisite for trust`；`by virtue of knowing their processes, I trust that system more`）。所以脚本里连犯的错都原样保留——「这些脚本里很多内容，就是我们犯的错」（`us making mistakes`）。

这个视角也解释了投入的量级。Phil 想象的场景是：公司若真的成功，「四大」会计师事务所之一迟早会上门审计你的流程（`the big four accounting firms show up and audit your processes`）；供应链安全如今声量极大，「而这是供应链中巨大的一环」（`supply chain security has gotten a lot of traction`）。后来 Oxide 把更新后的仪式细节写进 RFD 585（Cosmo 签名仪式）公开，但部分细节仍需脱敏——Phil 承认 Oxide 已是个相当显眼的目标（`on the Cosmo ceremony`，`we're a pretty appealing target`）。

### 道具清单：HSM、拆掉无线的笔记本与 M-of-N 分片

整套设计首先撞上一个自举困境：你本想替换掉的那些不可信平台，恰恰是眼下唯一可用的记录工具——没法把这套基础设施托付给一台满身已知漏洞的笔记本（`a real bootstrapping problem`）。原则由此展开：真正的资产是签名钥匙，要让它们暴露给尽可能少的组件，所以要有 HSM——专为处理密钥材料设计、不把它们暴露给通用计算平台的硬件（`specifically designed for handling keying material`）。钥匙在 HSM 内部生成、永不离开；能使用钥匙的是另一层「认证值」，它必须交给保管人（`we have authentication values that enable their use`）。这些认证值不是签名钥匙，但同样是秘密：随机生成、不重复使用，没人背得下来（`We generate them randomly`）。备份与恢复采用 M-of-N 分片——多个人各持份额，恢复时要凑齐其中的多数（`we do an M of N key splitting`，`the majority of them`）。

执行平台的加固清单同样偏执：静态镜像、从只读介质加载、没有可写文件系统、能核验磁盘摘要并记录在案（`does not have a writable file system`，`load it from read only media`）。最大的心病是无线——「有个 Wi-Fi 天线、蓝牙电台，那些东西会流向哪？」（`When there's a Wi Fi antenna, a Bluetooth radio`）——于是直接把天线从笔记本里拔掉（`we pulled that out of the laptops`）。但也不能走另一极端去买停产的老爷机：机器会坏，坏了造不出新的（`if it breaks and it will`）。Phil 的远期愿望，是有一天用 Oxide 自研、自己理解其安全问题的系统来跑签名仪式甚至制造流程（`even our manufacturing processes with systems that we have built`）。

然后是那台针式打印机。认证值要离开系统、点对点地交给具体的人，让对方拿到一件实物（`You want it to go to a specific person for them to take a physical thing`）；「这就是针式打印机出场的原因」（`This is where the dot matrix printer comes in`）。要澄清的是，打印的并不是签名钥匙——Bryan 一度以为打印机吐出的是私钥材料，被 Phil 连声否定——打印的是启用钥匙所需的认证值。选它的逻辑是「尽可能原始、但仍买得到」：整机可以拆开、逐个辨认部件，没有蓝牙、没有 Wi-Fi（`no Bluetooth, no wifi built into it at all`）。它并非无懈可击：打印机里有约 16MB 的可写存储（`was only like 16 megabytes`），可以接地某个管脚实现硬件禁写，但那样打印机就不工作了（`it won't actually write to the flash`）。所以仪式之后，它的结局是被 Dremel 电磨「外科手术式地谋杀」（`a very surgical murder of this dot matrix printer`）。复盘时 Phil 承认打印机不是好选择——太麻烦；后来改用可写 CD-ROM，代价是透明度下降：CD-ROM 没法拆开再装回去检视（`the printer was probably not the right way to go`，`we've switched over to using a writable CD ROMs`）。而这一整套家当的最终归宿，是一家「未具名银行」的保管箱，有带枪的守卫看着（`guarded by a person with a gun`，`in an unspecified bank for sure`）。

### 仪式当天：防篡改袋成了塑料袋

仪式定在 Gimlet 出货之前、2023 年，且已被推迟过，是踩着硬时限办成的（`before we're gonna ship Gimlet`）。此前的准备以周为单位摇摆：「这周能办吗？」「哦，还差个东西，下周吧」（`we were literally going week by week`）。Phil 事后总结，这类流程里的错误恰恰发生在理解不足的灰色地带，最伤人的就是没时间排练（`happen in those gray areas`）。当天的另一个硬约束是银行：东西必须在关门前存进保管箱，否则就得两个人守着笔记本对坐一整夜（`stuck with it overnight`）。

那天 Phil 第一次见到他们选用的防篡改袋——这种包装没有说明书，全靠自己悟（`no instructions on how to actually use the tamper evident package`）。结果恰恰栽在这里：撕开粘封的手法不对，防篡改层形同虚设，「我们用错了，它们就是普通塑料袋」（`We did it wrong and they were just plastic bags`）。Phil 开车回家路上越想越不安，索性掉头回办公室，拿一个袋子反复开封重封做实验——结论成立：这就是个塑料袋（`I literally just turned my car around and went to the office`）。风险要摊开说才显得严重：分片在各人手里，等于 HSM 口令在整整 24 小时内「实际上未受保护」——这种话没法对严肃的审计者说出口（`effectively unprotected for twenty four hours`）。Phil 把这称为对信念的测试：我们知道能做得更好。

当晚 CEO Steve 还在办公室加班。听完汇报，他问：「我们必须重做吗？」「必须吗？」得到「必须」的答复后，他说「好，那就重做」（`do we have to do this again`）。于是有了第二台针式打印机登场（`a second dot matrix printer`）。Phil 说，每多跑一次仪式、每写一版新脚本，流程就更顺畅、更自然，担当角色的人也更熟练（`get better every time we do it`）。

当天还有两段小插曲。仪式由运营团队的 Kate Hicks 拉进来操办（`Kate Hicks from our operations team`），她还提议「得给这事配几件长袍」（`we gotta get robes for this thing`）；袍子买回来才发现基本是塑料袋材质，静电大到可能击穿设备，仪式中途只好脱掉（`They were basically plastic bags`，`picking up an enormous amount of static`）。而 RFD 585 里记录了后续的改良：选一台能放进保管箱的小打印机，要求无 Wi-Fi、无蓝牙——Phil 说全市场能找到的只有一款（`the selection criteria for a smaller printer`，`there is literally one out there that I could find`）；改用标签打印机后流程轻松许多，打印机不必再死，连机带防篡改包装一起住进保管箱（`label printer makes this so much easier`，`it lives in tamper evident packaging in a safe box`）。

### 从 Secure Boot 批判到 Caliptra：LLM 时代的固件信任

钥匙一旦写进芯片，游戏规则就变了。信任根所用芯片自带 verified boot 实现，其中 key slot 数量有限、写一次即定，「烧完就烧完了」（`a finite number of key slots`）。今天还做不到更新钥匙（`you can't update the key`），但 Phil 强调终目标恰恰是能够 rekey——「必须有办法给这些系统换钥」，而且要把它当成没有退路的事（`to be able to rekey these things`）；业界默认这类钥匙长命，但理想是不必长命（`not require that they be long lived`）。初始阶段相关的 PKI 是三个中的两个，其一是硬件身份钥匙——信任根对安全状态做断言所用，「实际上就是你的 attestation signer」（`two PKIs of three`，`effectively your attestation signer`）。

Secure Boot 本身也被重新审视。它的出身是 UEFI：约 2010 年前后获得牵引，UEFI 会把插卡上的代码拉进自己的单一地址空间执行，攻击者于是借 PCI 扩展卡埋持久化，重启即接管 UEFI（`load it into its single address space`，`they took over UEFI`）。在「从未知来源加载代码进单一地址空间」的运营模型里，签名是唯一防线；但只要硬件能保证「让第一段被加载执行的代码显形」，代码是否出自 Oxide 就不再是关键——只要能讯问平台、发现它跑着不认识的代码，就按未知代码对待（`make evident the first code that was loaded and executed`）。Caliptra（归档转写作 "Calyptra"）和新的 RoT 思路正在让摆脱这类架构成为可能，但「这些东西仍然非常新」（`things like Calyptra`）。背后的信念一以贯之：固件里的不透明与保密，「掩盖的问题比解决的多」（`hiding more problems than it's solving`）。当然也有极限——AMD 平台 bundle 是加密的，跑在封装上隐藏的非架构核心里，Oxide 自己也没有可见性（`an encrypted bundle that runs on the hidden cores`）。

把话题拉回当下：Bryan 惊讶于 LLM 在挖掘高复杂度漏洞上的进步。Phil 的类比是核武器——过去整个行业的老手花大量时间寻找的东西，如今 LLM 十分钟就能把一段老代码「翻过来，把零钱抖出来」（`flip it over and shake all the change out of it`）；过去要五个资深漏洞挖掘者协作完成的事，现在五分钟、零先验知识就能做到，「这很可怕」（`in five minutes with no prior knowledge is terrifying`）。UEFI 这类诞生于不同年代的设计首当其冲，而推动它改变的激励「有点上下颠倒」，在乎的人太少（`the incentive unfortunately is a bit upside down there`）。另一个连锁反应是：能随手用上这些工具的人，往往没有与厂商和利益相关方周旋的历练，负责任披露流程常常不被遵守（`responsible disclosure of processes often don't get followed`）。

Oxide 给出的答案是保持动态：必须能更新，还必须更新得够快（`You have to be dynamic`）。没有 UEFI 包袱的一个正后果，是最底层的平台软件随每次软件更新一起发布——「我们一直在更新」（`We update all the time`）；「除非硬件坏了别去更新 BIOS」的世界，早就结束了（`don't update your BIOS unless you have a hardware problem`）。这几年的制造流程也在持续改造：信任根的产出开始用于在节点之间构建自举信任（呼应此前的 trust quorum 一期），attestation 甚至暴露到了虚拟机层，RFD 605 记录了这项工作（`We started exposing it up to the virtual machine layer`，`See RFD605 on that`）。Phil 自嘲这原本不在他的 bingo card 上：他以为此生的日子就是杀打印机、修管道。而这期节目的由头，正是 FAQ Friday 上有人问出的那个问题——「如何防止有人冒充 Oxide？」（`how do you prevent someone from impersonating Oxide`）。Bryan 的收束是：死去的针式打印机很高兴你问了这个问题，因为它们没有白白牺牲。

## 来源与定位

- 原始节目：[Dead Printers Tell No Tales](https://share.transistor.fm/s/226b1683)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 开场闲聊：Elizabeth Holmes 纪录片（`the Elizabeth Holmes documentary`）
  - 2022 年秋机架上电事故与硬件不再拖延（`half the sleds blew out`；`the mass casualty event`；`Hardware did not blink`）
  - 信任根依赖尚不存在的 PKI（`relied on a PKI that did not yet exist`；`everything seems to boil down to PKIs`）
  - 制造秘密与冒充风险（`use an oxide secret to encode a device ID`；`you could spoof Oxide software`；`we can now be impersonated effectively`）
  - 密钥封存于信任根芯片内部（`stored in the internal flash on the part`；`desolder and and exfiltrate`）
  - 不求完美、两人合谋底线与为成功做规划（`it can't be perfect`；`perfection is how you define done`；`two parties involved collude`；`To plan for success`）
  - 行业惨状与最低线（`create it outside the platform and then inject it`；`sitting on a thumb drive in someone's desk drawer`；`live with for a really, really, really long time`；`the minimum bar isn't really defined`；`our minimum bar was not having keys in someone's desk`）
  - Intel 对照与创业公司自力更生（`their PKI office has been around since probably the eighties`；`suddenly you gotta do it yourself`）
  - IANA 的 DNSSEC 根密钥仪式与公开脚本（`the only good resources I could find publicly`；`root signing keys for DNSSEC infrastructure`；`they record their signing ceremonies`；`You can get the scripts`）
  - 透明换信任、脚本记录错误、审计想象与 RFD 585（`Transparency is a prerequisite for trust`；`by virtue of knowing their processes, I trust that system more`；`us making mistakes`；`the big four accounting firms show up and audit your processes`；`supply chain security has gotten a lot of traction`；`on the Cosmo ceremony`；`we're a pretty appealing target`）
  - 仪式平台的自举困境、加固与无线拆除（`a real bootstrapping problem`；`does not have a writable file system`；`load it from read only media`；`When there's a Wi Fi antenna, a Bluetooth radio`；`we pulled that out of the laptops`；`if it breaks and it will`；`even our manufacturing processes with systems that we have built`）
  - HSM、认证值与 M-of-N 分片（`specifically designed for handling keying material`；`we have authentication values that enable their use`；`We generate them randomly`；`we do an M of N key splitting`；`the majority of them`）
  - 针式打印机的出场、选型、禁写尝试与销毁（`You want it to go to a specific person for them to take a physical thing`；`This is where the dot matrix printer comes in`；`no Bluetooth, no wifi built into it at all`；`was only like 16 megabytes`；`it won't actually write to the flash`；`a very surgical murder of this dot matrix printer`）
  - 改用可写 CD-ROM 与银行保管箱（`the printer was probably not the right way to go`；`we've switched over to using a writable CD ROMs`；`guarded by a person with a gun`；`in an unspecified bank for sure`）
  - 仪式时间表与银行关门的硬期限（`before we're gonna ship Gimlet`；`we were literally going week by week`；`happen in those gray areas`；`stuck with it overnight`）
  - 防篡改袋失效与连夜返工（`no instructions on how to actually use the tamper evident package`；`We did it wrong and they were just plastic bags`；`I literally just turned my car around and went to the office`；`effectively unprotected for twenty four hours`）
  - CEO 拍板重做与第二台打印机（`do we have to do this again`；`a second dot matrix printer`；`get better every time we do it`）
  - 长袍插曲与后续的小打印机改良（`Kate Hicks from our operations team`；`we gotta get robes for this thing`；`They were basically plastic bags`；`picking up an enormous amount of static`；`the selection criteria for a smaller printer`；`there is literally one out there that I could find`；`label printer makes this so much easier`；`it lives in tamper evident packaging in a safe box`）
  - 写一次的密钥槽与 rekey 目标（`a finite number of key slots`；`you can't update the key`；`to be able to rekey these things`；`not require that they be long lived`）
  - 两个 PKI 与硬件身份钥匙（`two PKIs of three`；`effectively your attestation signer`）
  - Secure Boot 的 UEFI 渊源与「让第一段代码显形」（`load it into its single address space`；`they took over UEFI`；`make evident the first code that was loaded and executed`）
  - Caliptra 与透明的极限（`things like Calyptra`；`hiding more problems than it's solving`；`an encrypted bundle that runs on the hidden cores`）
  - LLM 时代的漏洞挖掘与披露（`flip it over and shake all the change out of it`；`in five minutes with no prior knowledge is terrifying`；`the incentive unfortunately is a bit upside down there`；`responsible disclosure of processes often don't get followed`）
  - 持续更新与对客暴露（`You have to be dynamic`；`We update all the time`；`don't update your BIOS unless you have a hardware problem`；`We started exposing it up to the virtual machine layer`；`See RFD605 on that`）
  - 节目缘起（`how do you prevent someone from impersonating Oxide`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 归档转写为机器转写、存在专名噪声：IANA 被转作 "Ayanna"/"Ianna"，Caliptra 被转作 "Calyptra"，RoT 偶作 "RRT"，M-of-N 分片的数量口径在对话中亦有出入。本文按节目简介中的规范名称与 Oxide 惯用拼写还原，引文锚点一律保留归档转写的原文拼写。出版方页面原带段落级时间标注，归档规范化时被去除，故本文不使用任何时间定位。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
