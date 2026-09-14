---
item_id: oxide-and-friends-7aab8c73c810
title: 信任法定人数：机架如何在没有操作员的情况下自举信任
date: '2026-09-15'
published_at: '2026-04-04'
transcribed_at: '2026-09-15'
model: GLM-5.3 Flash
source_url: https://share.transistor.fm/s/d176e5fe
source_name: Oxide and Friends
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/d176e5fe/transcription
summary: Andrew Stone 与 Finch Foner 复盘四年半的 TrustQuorum：RoT 证书链、放弃 SPDM、LRTQ 权宜、Shamir 秘密共享的自愈扩展与 ZFS 原子换钥。
tags: [分布式系统, 安全, Rust]
---

# 信任法定人数：机架如何在没有操作员的情况下自举信任

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-04-04 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 2918 字 · 阅读约 8 分钟
>
> 标签：[分布式系统](/tags/分布式系统/) [安全](/tags/安全/) [Rust](/tags/Rust/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/d176e5fe) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/d176e5fe/transcription)

## 速读

Oxide 的机架要在无人值守的机房里断电重启后自动解密全部硬盘——这意味着 sled 之间必须先互相证明「我们是正牌 Oxide 硬件、跑的是正牌软件」，再用 Shamir 秘密共享凑齐机架密钥。Andrew Stone 与新加入的 Finch Foner 复盘这场四年半的长跑：RoT 制造证书链、SPDM 标准的尝试与放弃、赶首机交付的「低配版」LRTQ、可以自愈的 GFSS 秘密共享扩展，以及借 ZFS channel program 在内核里原子换钥的妙手。

## 主题正文

### 从 RoT 到安全通道：标准的诱惑与放弃

一切的地基是每个 sled 上的 Root of Trust（NXP LPC55S69）：借助硅杂质构成的物理不可克隆函数（PUF）获得不可伪造身份，制造时生成密钥对、经签名请求换回内嵌主板序列号与公钥的证书——私钥永不离开芯片（`00:07:23`–`00:10:55`）。 sled 间安全通道最初瞄准了 DMTF 的 SPDM 协议（约等于「TLS + 远程证明共用一把钥匙」），Andrew 在 RoT 上跑起了非标准实现的原型，随后发现问题：我们想要证明用一把钥匙、通道用另一把，而 SPDM 强制单钥匙耦合；纠缠许久后的顿悟来自同事一句话——「直接用 TLS，把证明分层叠上去就行」。最终架构反而是两个标准叠加：TLS 1.3 通道 + 独立的远程证明（基于 DICE 度量启动与 CoRim 清单）。Bryan 总结了这条弯路的教训：当你为了适配场景而拉伸一个标准时，就同时失去了「标准」与「自建」两者的好处（`00:11:13`–`00:18:14`、`00:40:23`–`00:41:44`）。

### 威胁模型与「低配版」TrustQuorum

要解决的核心问题：加密的 ZFS 数据集在机房断电重启后，没有操作员插笔记本输密码，怎么解密？威胁模型被精确地划为「随意物理接触」——防人顺走几块盘、几个 sled，不防整台三吨的机架被搬走（`00:19:38`–`00:24:55`）。方案是 Shamir 秘密共享：机架密钥被拆成 key shares 分布在各 sled 的 M.2 上，凑够门限即可重构、派生盘加密密钥。但 2022 年 8 月距离交付只有数周，完整的协议（密钥轮换、剔除 sled、远程证明）不可能完成，于是有了 LRTQ（low-rent trust quorum）：机架初始化时通过 bootstrap 网络（不出机架）的明文 TCP 分发 shares——没有轮换、没有剔除、没有证明，但「静态加密 + 防随意物理接触」两大目标达成， Robert 对提案的评价「我不喜欢它，但也不讨厌它」被 Andrew 视为最高褒奖（`00:29:09`–`00:35:47`）。预生成 255 份 shares 加密分存 32 个 sled 的巧思，让未来加入的 sled 也能领到 shares；代价是「忒修斯之机架」不可行——逐台替换到最后一块时额外 shares 已耗尽（`00:36:21`–`00:39:06`）。

### GFSS：可以自愈的秘密共享

真正的 TrustQuorum（RFD 238）重写了三遍以上：两阶段协议容忍异步与部分失败、支持密钥轮换与离线 sled 事后追赶；核心用 sans-io 风格写成——协议是纯状态机，副作用被物化为枚举——于是 prop fuzzing、oracle 对照、可单步快照的调试器全部成为可能（Andrew 专门写了带假节点的 TrustQuorum 调试器）；TLA+ 规格先行（`00:45:12`–`00:56:37`）。最漂亮的扩展是 GFSS（Galley Field Secret Sharing）：Andrew 钻进数学后发现，Shamir 插值不仅能重构 x=0 处的密钥，还能重构多项式上任意 x 处的 share——于是掉队的 sled 归队后可以向同伴询问、按自己的身份重算出最新轮次的 share，并解密历史 epoch 完成异步轮换。他判断这种用法「可能比谁都深」——Shamir 共享到处有人用，但把它烤成系统信任核心并玩出自愈的，Oxide 可能是第一家（`00:58:24`–`01:02:21`）。

### ZFS channel program：内核里的原子换钥

Finch 接手的硬骨头是轮换的落地：ZFS change-key 无法原子地同时设置记录密钥版本的用户属性——跨 sled、跨盘、属性与换钥之间三层部分失败，最坏情况是重启时机不巧导致数据无法解密（兜底的穷举试解已内建，但不能每次轮换都线性扫一遍）。解法是一段跑在 ZFS 内核模块里的 Lua channel program：借助事务组获得全有全无的原子性，Lua 脚本自身再实现应用层回滚以保证「真原子」；从没写过 Lua 的 Finch 靠 Claude Code 上手，并配了相当彻底的测试套件，在 4x2 模拟平台与 racklet 上验证升级路径（`01:02:53`–`01:12:14`）。合并最后一天的感受是「反高潮」——难的部分早已工作，剩下的只是管道工活；Bryan 则提醒长跑项目的「产后效应」：LRTQ 合入那天 Andrew 真的哭了，而大得多的 TrustQuorum 合并时反而没有 exhilaration（`01:14:40`–`01:18:38`）。下一步的「秘密份额天花板」是把 M.2 上的明文 shares 绑定到 RoT 启动，让偷 M.2 变成偷整机架；而客户兴趣的分布也很有趣——有武装警卫的客户反而不关心，主流企业恰恰最在乎。「我们做的不是安全产品，而是安全的产品」（`01:19:14`–`01:21:16`）。

## 来源与定位

- 原始节目：[Building a Quorum of Trust in the Oxide Rack](https://share.transistor.fm/s/d176e5fe)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - RoT、PUF 与制造证书链（00:07:23–00:10:55）
  - SPDM 的尝试、放弃与 TLS+证明两阶段（00:11:13–00:18:14）
  - 威胁模型：无操作员冷启动与随意物理接触（00:19:38–00:24:55）
  - LRTQ 权宜方案与 Robert 的评语（00:29:09–00:35:47）
  - 255 份预生成 shares 与忒修斯之机架限制（00:36:21–00:39:06）
  - sans-io 核心与 TrustQuorum 调试器（00:45:12–00:56:37）
  - GFSS：可重构任意 share 的自愈扩展（00:58:24–01:02:21）
  - ZFS channel program 原子换钥（01:02:53–01:12:14）
  - 反高潮、LRTQ 的眼泪与项目产后效应（01:14:40–01:18:38）
  - 秘密份额天花板与「安全的产品」（01:19:14–01:21:16）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 原始逐字稿为节目托管方自动转写并附说话人标注，人名与专名（Andrew Stone、Finch Foner、SPDM、CoRim、GFSS、RFD 238 等）可能存在转写误差，引用处已按上下文核对。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
