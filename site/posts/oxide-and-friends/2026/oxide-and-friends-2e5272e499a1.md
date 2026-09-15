---
item_id: oxide-and-friends-2e5272e499a1
title: 复活 1993 年的 BattleTris：考古式软件救援与 LLM 的第三条路
date: '2026-09-15'
published_at: '2026-06-09'
transcribed_at: '2026-09-15'
model: GLM-5.3 Flash
source_url: https://share.transistor.fm/s/b5fcf24b
source_name: Oxide and Friends
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/b5fcf24b/transcription
summary: Bryan 与 Adam 用 Claude 复活 1993 年的对战俄罗斯方块：无 core dump 靠上下文定位 64 位整数 bug，老软件救援从「不知道多远」变成可估。
tags: [开发者工具, LLM]
---

# 复活 1993 年的 BattleTris：考古式软件救援与 LLM 的第三条路

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-06-09 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 2636 字 · 阅读约 7 分钟
>
> 标签：[开发者工具](/tags/开发者工具/) [LLM](/tags/LLM/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/b5fcf24b) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/b5fcf24b/transcription)

## 速读

Bryan Cantrill 把 1993 年自己写的对战俄罗斯方块 BattleTris 在 Brown 计算机系传为经典，之后荒废了二十四年。这期他和 Adam Leventhal 讲这几个月用 Claude 把它复活的全过程：隐式不返回函数被 GCC 静默优化掉、X 的 depth 32 偷渡配置、没有 core dump 也能定位的 64 位整数 bug。更有价值的是结论：LLM 正在改变「老软件值不值得救」的经济学。

## 主题正文

### 一段游戏史与一个差点丢掉的拷贝

BattleTris 诞生于 1993 年暑假 Bryan 的个人项目，1994 年初他和 Mike Shapiro（后来的 DTrace 合作者）在 CS32 软件工程课把它做成正式团队项目，加入 null modem 线缆对战，第三名成员 Chuck 则写出了电脑对手 Ernie——「超前于时代的 AI」（`00:05:16`–`00:12:13`）。插曲是那年夏天返校时，唯一拷贝落在了刚起步的超跑巴士（Super Shuttle）上，他徒手追了四个街区把电脑拿了回来——「这是我毕生的心血」。游戏在 Brown 火到 Adam 的第一次给 Bryan 发邮件就是邀他回校和本科生打表演赛（`00:12:35`–`00:14:58`）。

### 2001 年的复活与二十四年荒废

第二次生命出现在 2001 年秋：Solaris 9 之后的「垃圾时间」里，一群内核工程师突然集体复活并魔改 BattleTris。Bryan 回看日期时的 adult-brain 猜测是，那正是 911 后的两个月，The Onion 那句「国家渴望重新关心无聊的破事」道尽氛围（`00:17:40`–`00:23:30`）。随后大家各自回到 DTrace、Pacifica（后来的 ZFS）和博士论文，游戏彻底荒废——Motif 长期不开源、移植 Linux 成本高企，「太麻烦了」就是墓志铭（`00:25:05`–`00:25:43`）。

### 用 Claude 做考古式救援

今年 Adam 在等一个二十分钟的评估任务时，让 Claude「把这个老东西跑起来」——目录还叫 BTPPC（PowerPC Mac 移植的遗迹），几乎没怎么来回就装好 open Motif 跑通了；Bryan 在 Linux 上复制了这条路（`00:26:39`–`00:33:31`）。过程中有几个教科书级的「以前能用、现在坏了」：一个靠隐式不返回的老函数，如今 GCC 直接判定 fallthrough 并静默不调用、无任何警告；他自己 X defaults 里偷渡的 `*depth: 32` 让所有人（包括 Claude）兜了一圈，最终是 ChatGPT 看了一眼配置文件点破——这本来是数小时的煎熬调试；还有 make 依赖不完整导致的陈旧 vtable 段错误，Claude 顺着 core dump 推到「头文件和目标文件失同步」的结论（`00:33:31`–`00:38:29`）。最惊人的一次：联机对战时游戏崩在 Bryan 的机器上、Linux 默认不留 core dump，他把「栈损坏 + 当时在对战」的上下文直接交给 Claude，它推断出与栈溢出一致、且需要一个「间谍」类武器的 bug——Adam 确认自己确实扔了那个武器。根因是仅在 64 位下暴露的整数宽度问题，而 BattleTris 从未有过 64 位版本（`00:42:15`–`00:45:40`）。

### 第三条路：老软件的经济学被改写

这期真正的论点在收尾。软件荒废从来不是代码在烂，而是它周围的接口与隐式假设在烂；直觉上 LLM 会催生更多重写，但 BattleTris 展示了第三条路——把「显然曾经能用」的工件调试回人间，而且 diff 是可审阅的小补丁，不是凭空生成的呓语（`00:49:00`–`00:51:20`）。外延至少有三：2038 问题（32 位 time_t 溢出）「被 LLM 根本性地改变」了，批量升级这类代码不再可怕（`00:51:20`–`00:57:00`）；许可证 fork 的恐吓 calculus 也变了——「你养不活这个 fork」的叙事在 LLM 辅助维护面前不再必然成立（Cockroach、Terraform 的例子）；以及 Adam 在家翻出的各种「曾经能用」的固件 hack，从此有了调试回存在（debug into existence）的选项（`00:58:48`–`01:00:22`）。收尾的彩蛋：Rain 写了把 SCCS/Teamware 仓库导入 Git 的工具，Claude 再从风格化的大 diff 里分离出实质修复——两位老 Solaris 人管这叫「这个星球上只有五个人会觉得酷的事」（`01:09:22`–`01:11:55`）。

## 来源与定位

- 原始节目：[This Old Repo: LLMs and the Restoration of BattleTris](https://share.transistor.fm/s/b5fcf24b)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - BattleTris 起源与 Super Shuttle 追车（00:04:56–00:09:37）
  - CS32 团队组队与 Ernie 电脑对手（00:10:45–00:12:13）
  - 2001 年 Solaris 空窗期复活（00:17:40–00:24:58）
  - 二十四年荒废的原因（00:25:05–00:25:43）
  - Claude 复活 Mac/Linux 版（00:26:39–00:33:31）
  - 隐式不返回函数被 GCC 静默处理（00:33:31–00:34:27）
  - X depth 32 偷渡配置（00:35:05–00:36:57）
  - make 依赖与陈旧 vtable（00:37:33–00:38:29）
  - 无 core dump 定位 64 位整数 bug（00:42:15–00:45:40）
  - 老软件复活的第三条路（00:49:00–00:51:20）
  - 2038 问题被 LLM 改变（00:51:20–00:57:00）
  - 许可 fork 的算盘变化（00:58:48–01:00:22）
  - SCCS→Git 导入与 diff 分离（01:09:22–01:11:55）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 原始逐字稿为节目托管方自动转写并附说话人标注，人名（Mike Shapiro、Adam Tarr、Matt Ahrens、Ed Yardeni 等）可能存在转写误差，引用处已按上下文核对。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
