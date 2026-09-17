---
item_id: software-engineering-radio-2f2d215e2394
title: BMC 之痛与控制平面：Bryan Cantrill 谈数据中心的失控底层与 Oxide 的取舍
date: '2026-09-17'
published_at: '2026-02-26'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/02/se-radio-709-bryan-cantrill-on-the-data-center-control-plane/'
source_name: 'Software Engineering Radio'
input_type: official_transcript
transcript_url: 'https://se-radio.net/2026/02/se-radio-709-bryan-cantrill-on-the-data-center-control-plane/'
summary: 'Bryan Cantrill 从三星规模的换料惊魂讲到 BMC「影子基础设施」：控制平面分形复杂、平台即价值观，Oxide 因此选 Rust 把认知负担前移给开发者、选 Illumos 保住调试能力与 ZFS/DTrace。'
tags: [硬件, 云服务, Rust, 安全]
---

# BMC 之痛与控制平面：Bryan Cantrill 谈数据中心的失控底层与 Oxide 的取舍

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-02-26 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6207 字 · 阅读约 16 分钟
>
> 标签：[硬件](/tags/硬件/) [云服务](/tags/云服务/) [Rust](/tags/Rust/) [安全](/tags/安全/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/02/se-radio-709-bryan-cantrill-on-the-data-center-control-plane/) · 📄 [查看官方逐字稿](https://se-radio.net/2026/02/se-radio-709-bryan-cantrill-on-the-data-center-control-plane/)

## 速读

Bryan Cantrill 从三星规模的换料惊魂讲到 BMC「影子基础设施」：控制平面分形复杂、平台即价值观，Oxide 因此选 Rust 把认知负担前移给开发者、选 Illumos 保住调试能力与 ZFS/DTrace。Oxide 联合创始人兼 CTO、前 Joyent CTO 与 Sun DTrace 共同作者 Bryan Cantrill，与主持人 Jeremy Jung 从「为什么 AWS 和 Google 都自己造机器」聊起，一路谈到 BMC 的根密码笑话、Joyent 用 Node 搭控制平面的教训，以及 Oxide 机架「通电两小时就能开 Provisioning」的交付体验（`powered on like two hours ago`）。适合正在评估自建基础设施、被 BMC 或固件问题折磨过、或者想理解「平台价值观」如何影响技术选型的工程师。

## 主题正文

### 三星规模的教训：静默换料与失控的底层

三星收购 Joyent 的原因很直白：三星的公有云账单「极其庞大」，而市场上没有能买到的 on-prem 云产品（`Samsung's Cloud bill was`）。进入三星后，Joyent 团队第一次直面「三星规模」——过去在几百台机器上偶发一次的问题，在一万台上变成日常。最经典的案例来自 Manta 对象存储的 Postgres 元数据层（`Manta`）：某个数据中心磁盘 I/O 延迟病态劣化，层层排查到最后，Cantrill 去查硬盘固件版本时才发现「Toshiba 也造硬盘？」——Dell 悄悄做了元件替换，换上了竞争力不佳的 Toshiba 盘，其固件会让盘停止响应读取长达约 2.7 秒（`Toshiba makes hard drives`，`stop acknowledging any reads from the order of 2,700 milliseconds`）。

他把这归为更深层的问题：Dell 这类厂商通过替换元件边际地降低成本，交给你的是一套它自己都没有信心验证过的系统，发现的义务留给了客户（`the AI infrastructure boom`之外，这种问题遍布 HPE、Supermicro、交换机与存储厂商）。真正的对照是：AWS、GCP 从来不是 Dell/HP/Supermicro 的客户，他们自己设计机器。Cantrill 的结论是云计算是一场重要的基础设施革命，「但它不应该只能租，你应该能买到它」（`you should be able to actually buy it`）——经济性仍是首要理由，此外还有安全、风险管理与延迟。

### BMC：计算机里的计算机，影子基础设施的真实代价

对底层失控最具体的载体是 BMC——「计算机里的计算机」，负责环境监控与风扇等，架构二十来年没有实质进化，核心通常是一家叫 ASPEED 的公司的专有芯片，而其 root 密码「实际上固化在硅片里」（`the root password is encoded effectively in silicon`）。Cantrill 的玩笑是 Oxide 创业早期，办公室 Wi-Fi 密码取的正是 ASPEED BMC root 密码的一小段。BMC 需要一张独立网络，上面跑着古老版本的 Linux：怎么打补丁、怎么管漏洞、被 root 之后整机沦陷——这是一套必须运维的「影子基础设施」，而 HPE 的 iLO、Dell 的 iDRAC 们普遍闭源难用（`an ancient, ancient version of Linux`）。

失效的代价可以量化。他举例某知名厂商的温度传感器坏了，BMC 自创了一套按 CPU inrush 电流调节风扇的控制环：客户的负载一尖峰，风扇就狂转再缓慢回落，转速下降赶不上下一次尖峰，于是风扇长期满转、机房白吹冷风——每台服务器浪费约 100 瓦，乘上整个数据中心就是数百千瓦的浪费（`on the order of like a hundred watts a server`）。更让人无力的是求助无门：厂商一句「只有你一个客户反映这个问题」就能把皮球踢回来，Cantrill 发誓 Oxide 永远不说这句话（`you're the only customer seeing this`）。

### 控制平面：API 请求与机器之间的一切

Cantrill 给控制平面的定义是「API 请求与基础设施被实际执行之间的一切」（`everything between your API request and that infrastructure being acted upon`）：Provisioning 一台 VM 背后是存储、虚拟网络、元数据的联动创建，这个分布式系统自身还必须可靠——sled 拔了怎么办、扩容怎么办、版本怎么滚，而且所有升级都要跨气隙进行，因为这台机器就部署在你的机房里（`all of that has to happen across an air gap`）。他用「分形般复杂」来形容这层软件。CLI、Web UI 与 API 应该从同一份 ground truth 生成，谁也不该是谁的附属（`single ground truth`）。

 VMware vSphere 算是「边缘接触」了控制平面，但对云原生一代来说仍像时光倒流；Proxmox、KVM 需要接入更多组件才称得上可管理的基础设施；OpenStack 则是「所有基础设施厂商的大杂烩」——「公司之间是处不来的」，它更像一个你要运营的项目，而不是产品（`companies don't get along`）。

### 平台即价值观：Node 之殇、Go 的别扭与 Rust 的错误处理

Joyent 时代的控制平面「全用 Node 写」（`we did it all in Node at Joyent`）。Cantrill 不回避这段历史：JavaScript 的设计目标是让尽可能多的人写出程序，代价是严谨性——拼错的属性名要到运行时才变成 undefined，程序员错误与磁盘满这类运维错误被混为一谈，而「可靠系统恰恰需要区分这两者」。他们给 Node 带去了 postmortem 诊断能力（JS 进程崩溃后能出可解析的 core dump），却发现自己是在与整个社区对着干。2014 年 io.js fork 之后，Joyent 把 Node 移交给基金会；2017 年他在 Node Summit 做了那场著名的《Platform is a reflection of values》演讲：Node 社区并非反对严谨，只是每次都要在「严谨」与「易上手」之间选后者（`Platform is a reflection of values`）。他由此得出选型原则：选平台就是选价值观对齐，社区规模远没有人们看的那么重要，他更信任小而自我选择的社区。

Go 在他看来是一次平移：仍然有 GC， generics 上的反复、反断言、反版本化的「自上而下决策」让他疲惫（`garbage collection out of my life`）。他要的是 C 的确定性产物加上好的库支持——2018 年他认定 Rust（逐字稿转作 "roster bust"，即 Rust or bust）。真正征服他的是错误处理与代数类型：Result 强制模式匹配，把「处理失败」从生产环境的运维者前移到开发期的程序员，「那种认知负担的转移正是我要的」（`shifts the cognitive load from the person that is operating this thing in production to the actual developer`）。他还给出 LLM 时代的新注脚：写代码时多付的认知负担可以由 LLM 分担，而 Rust 编译器给了 LLM 最明确的对错反馈，「Rust 非常适合 LLM 时代」（`great fit for the LLM`）——他预期软件将分化为严谨的基石软件与快速定制的另一极。

### 从机架到操作系统：Oxide 的整合答案与透明度

Oxide 的回答是从机架级重新设计：一台机架里是两台交换机加 32 块计算 sled，机架级直流母排由电源架整流供电，sled 对电源与网络（无源线缆背板）都是盲插，拔板不需要拔线；交换机核心是 Intel Tofino，另有一台独立交换机服务所有 service processor（`two switches and 32 compute sleds`，`blind mate`，`passive cabled back plane`，`Intel Tofino`）。交付体验因此变了：传统方式「机架到齐、错误型号的交换机、不匹配的导轨、缺线缆、软件互相甩锅」动辄数月（`easily months`）；Oxide 机架推进门、上电、配好 BGP，就能像公有云一样开 Provisioning——有客户通电两小时就开干了（`powered on like two hours ago`）。

操作系统选了 Illumos（Oxide 的分支叫 Helios），这是「特立独行但非轻率」的决定：一方面 Joyent 有多年 SmartOS 运维经验，另一方面他坚持「看一个操作系统要看它的内置调试器」，而 postmortem 可诊断性是刻在 Sun 血统里的（`you can judge a lot about an operating system by its built-in debugger`）。Linux 的问题不在内核本身——「Linux 是一个内核」——而在于要自己拼一个发行版：选 libc、选组件，维护负担「大得离谱」，从 Red Hat 来的同事 Laura Abbott 当时的警告后来被完全验证（`the maintenance burden of that is off the charts`，`Linux is a kernel`）；ZFS 因许可证问题始终进不了主线内核，也让他们在 Torvalds 对 ZFS 发飙的那个时间点下了决心（逐字稿把 ZFS 误转作 "CFS"，见整理说明；`CFS containers, DTrace, virtual networking`）。ZFS、容器、DTrace、虚拟网络这些能力在 Illumos 里开箱即用。

最后是姿态问题。Dell 与 EMC 的联合支持被形容为「对话离异的父母」——各自设计的系统叠在一起出问题，谁都能把责任推给对方，最终用户只能自认倒霉（`talking to their divorced parents`）。Cantrill 说 Sun 时代 Fishworks（Fully Integrated Software and Hardware）就想兑现系统级承诺，但在「商品硬件」上仍被不受控的固件坑过，直到 Oxide 才真正控制了从固件到软件的全栈（`Fully Integrated Software and Hardware`）；即便问题出在 Oxide 与其他系统的「缝隙」里，他们也会把它追到根因。代价是极度的透明——RFD、代码仓库全部公开，有客户笑着说「我不用你通知，我盯着 GitHub issue 呢」（`watching the GitHub issue`）。

## 来源与定位

- 原始节目：[SE Radio 709: Bryan Cantrill on the Data Center Control Plane](https://se-radio.net/2026/02/se-radio-709-bryan-cantrill-on-the-data-center-control-plane/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 三星收购动机与公有云账单（`Samsung's Cloud bill was`）
  - Dell 静默换料与 Toshiba 盘 2.7 秒停顿（`Toshiba makes hard drives`；`stop acknowledging any reads from the order of 2,700 milliseconds`）
  - 云应该能买不能只租（`you should be able to actually buy it`）
  - BMC、ASPEED 与固化在硅片里的 root 密码（`the root password is encoded effectively in silicon`）
  - BMC 上的古老 Linux 与影子基础设施（`an ancient, ancient version of Linux`）
  - 风扇失控的能耗代价（`on the order of like a hundred watts a server`）
  - 「只有你一个客户反映」与 Oxide 的承诺（`you're the only customer seeing this`）
  - 控制平面定义与跨气隙升级（`everything between your API request and that infrastructure being acted upon`；`all of that has to happen across an air gap`）
  - vSphere/Proxmox/OpenStack 的光谱与「公司处不来」（`companies don't get along`）
  - Joyent 全用 Node 的教训与《Platform is a reflection of values》（`we did it all in Node at Joyent`；`Platform is a reflection of values`）
  - 告别 GC 与 Rust 错误处理的认知负担前移（`garbage collection out of my life`；`shifts the cognitive load from the person that is operating this thing in production to the actual developer`）
  - LLM 时代的 Rust 适配（`great fit for the LLM`）
  - 机架形态与盲插背板（`two switches and 32 compute sleds`；`blind mate`；`passive cabled back plane`；`Intel Tofino`）
  - 数月交付对照两小时可用（`easily months`；`powered on like two hours ago`）
  - 内置调试器、Linux 发行版负担与 ZFS 之困（`you can judge a lot about an operating system by its built-in debugger`；`the maintenance burden of that is off the charts`；`Linux is a kernel`；`CFS containers, DTrace, virtual networking`）
  - 「离异的父母」式支持与责任到根因（`talking to their divorced parents`；`take responsibility for taking that all the way to root cause`）
  - 透明度与盯着 GitHub issue 的客户（`watching the GitHub issue`）

## 整理说明

- 本文基于节目内容与出版方公开的完整官方逐字稿整理。
- 出版方逐字稿为自动生成（页面注明），时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 自动转写存在专名噪声，本文仅在上下文可充分确证处修正：开场 DTrace 转作 "DTRAce"、"bhyve" 转作 "Beehive"（正文未使用该细节）、TJ Holowaychuk 转作 "TJ Holloway Chuck"、iDRAC 转作 "IRAC"、ZFS 在文件系统讨论中转作 "CFS"、SmartOS 转作 "Smarto asset"、roster bust 即 Rust or bust。「约 2.7 秒」「100 瓦/台」「数十万千瓦」「32 sled」「两小时」等数字与表述均为嘉宾口述口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
