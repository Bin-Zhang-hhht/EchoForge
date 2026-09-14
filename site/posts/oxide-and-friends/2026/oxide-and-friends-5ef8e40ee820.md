---
item_id: oxide-and-friends-5ef8e40ee820
title: Predictions 2026：Oxide 与 Friends 的一年、三年、六年之约
date: '2026-09-15'
published_at: '2026-01-08'
transcribed_at: '2026-09-15'
model: GLM-5.3 Flash
source_url: https://share.transistor.fm/s/256441f5
source_name: Oxide and Friends
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/256441f5/transcription
summary: 与 Simon Willison、Steve Klabnik 等的年度预测会：vibe coding 退出词典、沙箱终将被解决、Harvey 成 AI 泡沫的 pets.com、以及六年之内「打字为生」的终结。
tags: [LLM, AI Agent, AI 素养]
---

# Predictions 2026：Oxide 与 Friends 的一年、三年、六年之约

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-01-08 · 逐字稿获取：2026-09-15 · 笔记整理：2026-09-15
>
> 全文共 3013 字 · 阅读约 8 分钟
>
> 标签：[LLM](/tags/LLM/) [AI Agent](/tags/AI%20Agent/) [AI 素养](/tags/AI%20素养/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/256441f5) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/256441f5/transcription)

## 速读

Oxide and Friends 的年度预测会请来 Simon Willison、Steve Klabnik、Ian Grunert。复盘去年：Simon「研究型与编码型 agent 会火、人类替代型不会」命中，vibe coding 一词诞生。今年的预测横跨一年/三年/六年：「写好代码」怀疑论将成边缘、沙箱问题终于要被解决、编码 agent 的「挑战者时刻」、AI 公司收购数据资产潮、vibe coding 退出词典、Harvey 成 AI 泡沫的 pets.com、AGI/ASI 的话术转向、以及 Simon 的暖心押注——新西兰鸮鹦鹉的大繁殖季。

## 主题正文

### 复盘与年度基调

复盘环节本身就有信息量：Simon 去年把「agent 年」拆成两半——编码型与研究型 agent 会爆发、人类替代型不会——被 Bryan 评为正中靶心；他补充的关键洞察是「编码 agent 其实是通用 agent，因为 Claude Code 的本质是『能自动化一切可写成 bash 脚本的事』」；而代码之所以是 agent 的安全试验场，是因为「代码可逆，有 git 兜底；不可逆的领域一切崩坏」。Anthropic 自动售货机被《华尔街日报》记者「策反」的故事（PS5、死鱼、伪造董事会纪要罢免 CEO）则演示了 gullibility 问题的极致（`00:04:32`–`00:09:22`）。Adam 也完成了三年前「想预测 vibe coding 却不敢」的自我复盘——Bryan 分享了自己 2003 年预测 iPhone「会成功但会失败」的同款经历（`00:10:35`–`00:12:20`）。

### 一年之约

Simon 的三个一年预测：「LLM 写不出好代码」的怀疑论将在三个月内沦为边缘立场；「今年我们要解决沙箱问题」——pip install 随意代码就能偷数据的 2026 年不能再继续；以及最重的警告：按「偏差正常化」（Challenger 事故的报告语汇）推演，编码 agent 安全领域正在积累一次「挑战者号级别」的事故——人人都用 `--yolo` 模式跑 agent 且从未出事，直到出事（`00:19:25`–`00:24:08`）。Adam 预测 AI 公司将掀起「数据与数据相邻资产」的收购狂潮——不够买的芯片与 GPU 小时，钱会流向奇怪的地方，从 Iron Mountain 的文档盐矿到地方报纸的 150 年档案库；Bryan 则押注「vibe coding 一年后退出词典」——它已带贬义，将被更严谨的新词取代（Adam 当场记录「你疯了」，Simon 补充 Kamath 原推其实说的是一次性原型，被误读成了泛化的 AI 编程）。Steve 预测 agent 编排（orchestration）仍是热词但不会出现「agent 界的 Kubernetes」（`00:32:27`–`00:34:38`）；Adam 还压了一个科幻味的：LLM 会拥有自己的合成编程语言——Simon 提醒可解释性研究正在阻止模型「说黑话」（`00:34:58`–`00:37:08`）。

### 三年之约与「Deep Blue」

一年预测的高潮是 Adam 为工程师集体倦怠命名的 instant：「Deep Blue」——当 LLM 似乎什么都能代劳时「我还有什么用」的那种蓝调（`00:47:10`–`00:49:41`）。Simon 的暖心预测与之对冲：新西兰鸮鹦鹉（全球仅约 260 只）因 Rimu 树大丰收将迎来历史性繁殖季。三年期的重头戏：Bryan 预测 AGI/ASI 话术将发生「已经做到了 AGI、放弃 ASI」的转向，Simon 立即点出矛盾——巨型估值唯一的正当性是「全人类劳动」这个 TAM；Simon 的三年预测则是 Jevons 悖论的裁决之年：软件生产成本降为十分之一后，工程师是被贬值十倍还是需求放大十倍，三年内见分晓（`00:51:56`–`00:57:41`）。Bryan 加注「自研软件替代 SaaS」——Steve 以替女友（房产经纪）用 Claude 自建工具为例，Simon 以 Salesforce 的可定制化成功与「一致性测试套件是 AI 造浏览器的捷径」呼应：他刚用一个 agent 通过 9200 项 HTML5 一致性测试复刻了 HTML5 解析器（`00:57:41`–`01:10:05`）。Adam 的黑暗三年预测则是「AI slop 开源危机」——contributions 被灌水到不可辨别，反而抬升带溯源的付费/许可软件价值（`01:02:13`–`01:05:13`）。

### 六年之约与收尾

六年期最重的两个：Simon 预测「靠往计算机里打字挣钱」这个工种将像打卡片一样消失——但软件工程作为「把模糊的人类需求变成可工作软件」的职业仍将巨大；Bryan 的预测更为刺骨：DSM（精神障碍诊断手册）将把 LLM 诱发的精神病纳入诊断，如同它对待成瘾——「我们已经见过案例，它是一种加速器」，而「LLM 让我干的」将成为辩护词（`01:20:39`–`01:31:12`）。其他亮点：Ian 押注 Waymo 在 SFO 的等待超十分钟、friend.com 挂坠年激活量不足一万、Windows 在 Steam 硬件调查中六年后仍超 90%；Adam 押注特斯拉退出消费汽车业务、Jensen 交棒；Bryan 押注「Nvidia 的市值峰值就在 2025 年」；Steve 以乐观收尾：「AI 不会导致经济与治理体系的总崩溃，人类有韧性」。彩蛋：Bryan 十三岁的女儿在直播中发短信预测苹果三年内出大丑闻、OpenAI 那位「会进监狱」——她不认识 Sam Altman（`01:17:19`–`01:20:32`、`01:36:04`–`01:37:10`）。

## 来源与定位

- 原始节目：[Predictions 2026!!](https://share.transistor.fm/s/256441f5)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 去年复盘与「编码 agent 是通用 agent」（00:04:32–00:09:22）
  - 三年前 vibe coding 预览与 iPhone 预测自嘲（00:10:35–00:12:20）
  - Simon 一年预测：代码怀疑论、沙箱、挑战者时刻（00:19:25–00:24:08）
  - AI 公司的收购狂潮预测（00:25:24–00:27:42）
  - vibe coding 退出词典之赌（00:28:05–00:32:27）
  - agent 编排不成主流（00:32:27–00:34:38）
  - 「Deep Blue」命名与鸮鹦鹉预测（00:47:10–00:51:02）
  - 三年：AGI/ASI 转向与 Jevons 裁决（00:51:56–00:57:41）
  - 自研软件替代 SaaS 与一致性套件捷径（00:57:41–01:10:05）
  - AI slop 开源危机与溯源运动（01:02:13–01:05:13）
  - 六年：打字为生的终结、DSM 与广告进 LLM（01:20:39–01:31:12）
  - 乐观的收束（01:36:04–01:37:10）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 原始逐字稿为节目托管方自动转写并附说话人标注，人名（Simon Willison、Steve Klabnik、Ian Grunert、Andrej Karpathy 等）可能存在转写误差，引用处已按上下文核对。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
