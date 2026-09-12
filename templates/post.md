---
item_id: <stable-item-id>
title: <中文文章标题>
date: 'YYYY-MM-DD'
published_at: 'YYYY-MM-DD'
transcribed_at: 'YYYY-MM-DD'
model: <处理模型>
source_url: https://example.com/episode
source_name: <Podcast 名称>
input_type: official_transcript
transcript_url: https://example.com/transcript
summary: <一句话说明这篇文章为什么值得看>
tags: [标签]
---

# <中文文章标题>

> 节目：[<Podcast 名称>](/posts/<source-id>/)
>
> 节目发布：YYYY-MM-DD · 逐字稿获取：YYYY-MM-DD · 笔记整理：YYYY-MM-DD
>
> 全文共 N 字 · 阅读约 M 分钟
>
> 标签：[标签](/tags/标签/)
>
> 🎧 [收听原节目](https://example.com/episode) · 📄 [查看官方逐字稿](https://example.com/transcript)

无官方公开逐字稿时，删除同一行里的「📄 查看官方逐字稿」并去掉 `transcript_url`，只保留「🎧 收听原节目」。

## 速读

说明这期讨论什么、适合谁，以及最值得关注的内容，回答“为什么值得看”。列表页和首页展示的一句话摘要来自 frontmatter 的 `summary` 字段（不超过 180 字），请与速读开头保持一致，不要在两处重复维护不同说法。

## 主题正文

### <重点主题>

说明观点、依据、适用条件和分歧。

## 来源与定位

- 原始节目：[<标题>](https://example.com/episode)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - <一句说明本段主张>（00:14:06–00:22:38）

时间戳统一补零为 HH:MM:SS（不足一小时也写 00）。正文引用节目内容时，在句末追加（`00:14:06–00:22:38`），每段时间用反引号包裹、多段之间用中文逗号分隔，单点写（`00:08:10` 起）。来源没有可靠时间戳时，定位说明改为「官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。」（ASR 来源写「时间戳取自 ASR 逐字稿。」），条目与正文改用可搜索原文短语，不写推算的时间。

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：<处理模型>
- AI 编辑整理，请以原始节目为准。

前两条按来源调整：ASR 来源第一条写「本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。」；无时间戳来源第二条写「原节目未提供可靠时间戳，全部定位使用可搜索原文短语。」
