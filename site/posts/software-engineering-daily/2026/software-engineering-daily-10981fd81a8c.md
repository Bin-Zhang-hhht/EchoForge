---
item_id: software-engineering-daily-10981fd81a8c
title: 'Cilium 与 eBPF：基于身份的网络、service mesh 之辩与"杀死这个词"'
date: '2026-09-13'
published_at: '2026-03-26'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/cilium-ebpf-and-modern-kubernetes-networking-with-bill-mulligan/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1902-Cilium-and-eBPF.txt'
summary: 'Cilium 生态的 Bill Mulligan 讲 eBPF 网络革命：iptables O(N) 到 HashMap O(1)、基于身份替代基于 IP、Hubble 可观测性，以及"杀死 service mesh 这个词"。'
tags: [开发者工具, 开源, 分布式系统]
---

# Cilium 与 eBPF：基于身份的网络、service mesh 之辩与"杀死这个词"

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-03-26 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 3569 字 · 阅读约 9 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [开源](/tags/%E5%BC%80%E6%BA%90/) [分布式系统](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/cilium-ebpf-and-modern-kubernetes-networking-with-bill-mulligan/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1902-Cilium-and-eBPF.txt)

## 速读

Cilium 生态的 Bill Mulligan（Isovalent/Cisco）接受 SED 访谈（主持为 Gregor Vand），讲 eBPF 如何重建 Kubernetes 网络。Cilium 距首个 commit 几乎正好 10 年、个人贡献者已突破 1000 人。技术核心是两个切换：把 iptables 的 O(N) 线性规则遍历换成 HashMap 的 O(1) 查找（Trendyol 替换 kube-proxy 后集群吞吐提升 40%）；把网络模型从"基于 IP"换成"基于身份"（label），容器生灭不再引发规则 churn。

最鲜明的观点是 Bill 对 service mesh 的否定——他想"杀死 service mesh 这个词和这个品类"，认为 mesh 想解决的本质是网络问题。文中性能数字与排位口径均为访谈中的口头引用（两人口径不一处已标注）。

## 主题正文

### eBPF 是什么：内核的 JavaScript

Bill 的路径：生化本科 → 社科硕士 → 2018 年创业做"K8s 上的 AI 平台"（"当时没人在做 AI、没人做 K8s"，公司很快倒闭）→ CNCF → Isovalent。eBPF 约 11 年历史；他的类比是"eBPF 之于内核，如同 JavaScript 之于浏览器"——从只能静态消费到可交互、可编程。（`00:01:50–00:11:50`）

为什么需要它：Linux 明年就 35 年了，功能必须 upstream、开发周期长，而用户实际运行的是落后 2-5 年的内核——对多数人而言内核"实际上是静态的"。eBPF 允许把程序插到内核 hook 上、触发即运行；安全性来自验证器：每个程序插入前经校验、确认不会崩溃内核——他以 CrowdStrike 事件（内核 bug 导致全球 IT 崩溃）为反例，主持人补充那是 Windows。Cilium 由 Open vSwitch 团队出身的人创建，核心能力是"对 Linux 内核重新编程"；名称史：BPF=Berkeley Packet Filter，eBPF 已远超"包过滤器"，涵盖可观测性、安全、profiling、调度。（`00:05:59–00:13:49`）

### 两个核心切换：O(1) 查找与基于身份

传统网络基于 IP 与 iptables：按 IP 列表线性遍历规则（O(N)），在数千至百万容量的集群中效率低；Cilium 用全部由 BPF 编写的 Kube-proxy Replacement 取代 iptables 和 kube-proxy，改为 HashMap 查找（O(1)）——Trendyol（土耳其电商）替换后集群吞吐提升 40%（受访者引用的案例数字）。第二个动机：容器 IP 不固定、频繁生灭，基于 IP 的规则要频繁更新；Cilium 把模型切换为"基于身份"（label）——从"IP X 能访问 IP Y"变为"front end 能访问 back end"，后端容器轮换不影响身份。类比是 Okta 式身份系统：新 pod 带 front end 标签即自动获得对应通信权。（`00:13:49–00:21:09`）

### 网络策略与 Bloomberg 案例

用户选择 Cilium 的主因（他列了四项，虽然自述"三个"）：网络策略、kube-proxy 替换、流量加密、Hubble 可观测性。Cilium 实现 K8s 的 L3/L4 网络策略，额外提供 L7 策略（按域名允许/拒绝）与集群级策略。Bloomberg 案例：面向客户的数据沙箱产品（Jupyter Notebook 分析金融数据），用 namespace 隔离多租户、网络策略禁止跨 namespace 通信、禁止数据 egress 出集群。一个关键条件：部分 CNI 根本不实现网络策略——此时 K8s 策略写了也不生效。（`00:21:09–00:25:32`）

### "杀死 service mesh 这个词"

Bill 观点最鲜明的段落：他明言想"杀死 service mesh 这个词和这个品类"，写过《The Future of Service Mesh is Networking》。论证：mesh 想解决的微服务间网络/可观测/安全本质上是网络问题，只盯 L7 一层会丢失其他层的上下文。技术细节支持这个论点：Cilium 可从 socket 直达 socket、不走完整内核网络栈，叠加的 service mesh 在网络栈末端等 L7 流量——"包根本不经过那里"，mesh 看不到流量。Cilium service mesh 的实际内容是 L7 网络策略、L7 流量路由与一体的可观测性——他审视后认为当时已有"service mesh 的 80%"，只缺 L7 的 20%，故补齐而非从零造。他今天对它的定义是"Cilium 在 K8s 上的 Gateway API 实现"。（`00:25:32–00:32:03`）

### Hubble：复用 CNI 数据的可观测性

Hubble 的原理：eBPF 程序已在内核路由全部流量、天然可见，Hubble 把这些信息直接呈现——非独立采集。形态是网络流日志加 Hubble UI（集群服务地图）。他引用 ESNet（美国能源科学网络）的评价："过去要花几天工程时间排查的问题，现在 30 秒解决"；并称 Hubble 是"几乎每个用户的最爱功能"。一个新世界的代价：传统工具（如 tcpdump）依赖网络栈，而 eBPF 的 socket-to-socket 路由绕开传统工具——需要新工具如 pwru（"packet, where are you"）。（`00:32:24–00:37:20`）

### 架构、迁移与社区

架构：Cilium operator 管理集群内所有 agent 生命周期；agent 以 DaemonSet 每节点一个、负责安装全部 eBPF 程序。核心设计是数据平面与控制平面生命周期解耦：agent 挂掉后已安装的程序继续路由流量，只是不能再更新。L7 部分由 Envoy（每节点一个）协作完成。迁移有渐进路径：CNI chaining（在 Flannel 之上装 Cilium 只做可观测性或策略，Alibaba 案例）；或用 CiliumNodeConfig 逐节点切换（DB Schenker 完成了 live migration）。社区规模：个人贡献者 2025 年 10 月突破 1000 人——他的解释是典型用户是"4 名平台工程师支撑 200 名开发者"，会写 BPF 的人远少于会写 HTML 的人；CNCF 内排位两人口径不一（"前三"vs"第二大"），已如实保留。（`00:37:25–00:50:16`）

### 2026 展望：IPv6 之年与 Netkit

IPv6：CiliumCon 有 ESNet 与 TikTok 两场 IPv6-only 集群实践分享；他判断"今年也许终于是 IPv6 之年"（条件性）。VMware 迁移背景带来两条线：VM 跑进 K8s（KubeVirt）与集群外 VM 资产的连通。Netkit（他重点项目，由 eBPF 共同创始人 Daniel Borkmann 开发、Linux 内核特性）：容器是宿主机上带独立网络 namespace 的进程、进出有开销；Netkit 把包从网卡直接送进容器，"基本零开销"；KubeVirt 场景下消除"VM 套容器再套宿主机"的双重开销。可用性：容器部分"现在就已发布"（前提是内核与 Cilium 版本对），VM 部分"大概明年"。（`00:50:16–00:54:23`）

上手路径：cilium.io 官网、官方 hands-on labs（免自建集群）、著名的 Star Wars 演示（如何炸掉/保护 Death Star）、GitHub 与 Slack。（`00:54:23–00:57:15`）

## 来源与定位

- 原始节目：[Cilium, eBPF, and Modern Kubernetes Networking with Bill Mulligan](https://softwareengineeringdaily.com/podcasts/cilium-ebpf-and-modern-kubernetes-networking-with-bill-mulligan/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - eBPF 原理与"内核的 JavaScript"类比（00:05:59–00:13:49）
  - O(1) 查找与基于身份的切换（00:13:49–00:21:09）
  - 网络策略与 Bloomberg 案例（00:21:09–00:25:32）
  - "杀死 service mesh 这个词"（00:25:32–00:32:03）
  - Hubble 可观测性与排障案例（00:32:24–00:37:20）
  - 架构解耦与渐进迁移（00:37:25–00:50:16）
  - IPv6、Netkit 与 2026 展望（00:50:16–00:54:23）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 性能数字（Trendyol +40%、ESNet 评价）、CNCF 排位等均为访谈中的口头引用，两位说话人排位口径不一致处已如实保留；受访者为 Cilium 生态利益相关方。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
