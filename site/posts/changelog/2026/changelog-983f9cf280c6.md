---
item_id: changelog-983f9cf280c6
title: Changelog 新闻速递：Bitwarden CLI 供应链中招与 TypeScript 7、Spinal、PG Backrest
date: '2026-09-15'
published_at: '2026-04-29'
transcribed_at: '2026-09-15'
model: GLM-5.3 Flash
source_url: https://changelog.com/news/185
source_name: The Changelog
input_type: video_agent_kit_asr
summary: 本周要闻：Bitwarden CLI 在 npm 供应链攻击中被植入凭据窃取；TypeScript 7 beta 快 10 倍；Spinal 把 Ruby 编译成原生二进制；PG Backrest 停止维护。
tags: [安全, 开源, 开发者工具]
---

# Changelog 新闻速递：Bitwarden CLI 供应链中招与 TypeScript 7、Spinal、PG Backrest

> 节目：[The Changelog](/podcasts/changelog/)
>
> 节目发布：2026-04-29 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 1672 字 · 阅读约 5 分钟
>
> 标签：[安全](/tags/安全/) [开源](/tags/开源/) [开发者工具](/tags/开发者工具/)
>
> 🎧 [收听原节目](https://changelog.com/news/185)

## 速读

这是 The Changelog 2026 年 4 月 27 日当周的新闻速递（约 8 分钟），六条要闻里最重的是 Bitwarden 官方 CLI 在 npm 供应链攻击中被植入凭据窃取代码——运行过 `bitwarden`/`bw` 命令的机器要按事件响应处理而非打补丁。其余：Warp 终端开源、TypeScript 7.0 beta（快约 10 倍）、Ubuntu 26.04 LTS、Ruby AOT 编译器 Spinal，以及 PG Backrest 十三年后停止维护。

## 主题正文

### Bitwarden CLI：密码管理器的门口失守

Socket 团队标记的恶意 CLI 被发布到 npm，属于近几周横扫开发者工具链的同一场「checkmarks 主题」供应链攻击（`00:00:48`–`00:01:08`）。被植入的版本会抓取 GitHub token、AWS/Azure/GCP 凭据、npm 配置、SSH key、shell 配置文件，甚至 CLAUDE 与 MCP 配置文件，回传到伪造的端点（`00:01:08`–`00:01:32`）。主持人的要点值得原文复述：如果你最近几周在开发机或 CI runner 上跑过 `bitwarden`/`bw`，「这是事件响应，不是补丁周期」；Socket 的判断是它复用了同一波攻击的 GitHub Actions 供应链向量——「这是一次战略性攻击，开发工具正处在瞄准线上」（`00:01:32`–`00:01:59`）。

### 其余五条

**Warp 终端开源**（`00:00:10`–`00:00:43`）：官方理由是「与社区协作能更快交付更好的 Warp」。**TypeScript 7.0 beta**（`00:01:59`–`00:02:54`）：核心从 JS 自举编译器重写为 Go，头条数字是比 6.0 快约 10 倍，声称高度稳定、可立即进 CI，正式版预计两个月内。**Ubuntu 26.04 LTS**（`00:02:56`–`00:03:46`）：支持到 2036 年 4 月；最有信息量的信号是 Canonical 给「Rust 核心工具替换」踩了刹车——对 LTS 而言这是加分的保守。**Spinal**（`00:05:42`–`00:06:46`）：Ruby 的 AOT 编译器，源码→C→GCC/clang 原生二进制，基准约 11.6 倍、计算密集型（Conway 生命游戏）86 倍；作者的信号是给 Ruby 一条「类型化预编译车道」， CLI/Lambda/短进程场景不再被迫转 Go/Rust。**PG Backrest 停止维护**（`00:06:46`–`00:07:53`）：13 年后 David Steele 归档仓库，readme 冠以「obsolescence 声明」，原话是「与其做得差或做三天停三天，不如硬停」。作者的提醒很实在：它编织在大量生产 Postgres 部署的 runbook 和灾备方案里，下一个 CVE 来了不会再有补丁——如果你在生产用它，这是本周任务。

## 来源与定位

- 原始节目：[Bitwarden CLI compromised (News)](https://changelog.com/news/185)
- 定位：时间戳取自 ASR 逐字稿。
  - Warp 开源（00:00:10–00:00:43）
  - Bitwarden CLI 供应链攻击与凭据窃取清单（00:00:48–00:01:59）
  - TypeScript 7.0 beta 与 10 倍（00:01:59–00:02:54）
  - Ubuntu 26.04 LTS 与 Rust coreutils 刹车（00:02:56–00:03:46）
  - Spinal：Ruby AOT 编译器（00:05:42–00:06:46）
  - PG Backrest 停止维护（00:06:46–00:07:53）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 该期无官方逐字稿（新闻页无 transcript、GitHub 逐字稿仓库未收录），时间戳取自 ASR 逐字稿。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
