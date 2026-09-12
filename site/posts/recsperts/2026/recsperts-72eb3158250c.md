---
item_id: recsperts-72eb3158250c
title: '推荐系统要优化的不是点击：Joseph Konstan 谈有用性与长期价值'
date: '2026-09-11'
published_at: '2026-09-01'
transcribed_at: '2026-09-11'
model: 'gpt-5.6-sol'
source_url: 'https://share.transistor.fm/s/c07c7bf6'
source_name: 'Recsperts'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/c07c7bf6/transcript.txt
summary: '有用的推荐不等于高准确率或高点击率，必须结合具体情境、长期关系、真实用户实验和多方利益相关者来定义价值，再选择模型和指标。'
tags: [推荐系统, 产品指标]
prev: false
next: false
---

# 推荐系统要优化的不是点击：Joseph Konstan 谈有用性与长期价值

> 节目：[Recsperts](/posts/recsperts/)
>
> 节目发布：2026-09-01 · 逐字稿获取：2026-09-11 · 笔记整理：2026-09-11
>
> 阅读约 7 分钟
>
> 标签：[推荐系统](/tags/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F/) [产品指标](/tags/%E4%BA%A7%E5%93%81%E6%8C%87%E6%A0%87/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/c07c7bf6)
>
> 📄 [查看官方逐字稿](https://share.transistor.fm/s/c07c7bf6/transcript.txt)

## 速读

这期长访谈适合推荐算法工程师、产品经理和做实验平台的人。Joseph Konstan 反复追问的不是“模型能否预测用户会点什么”，而是“推荐是否在具体情境中为用户创造了原本不会发生的价值”。这一区别会改变离线指标、在线实验、界面设计和长期业务目标。

访谈也回顾了推荐系统研究社区与真实用户实验平台的发展，但本文不展开需要额外听检才能确认的人名、年份和规模。官方 transcript 没有时间戳，所有定位都使用可在全文中搜索的原文短语，不编造时间。

## 主题正文

### 高准确率可以只是在正确地说废话

Konstan 用超市思想实验说明准确率与价值的差别：如果在每辆购物车上都印上“buy bananas and bread”，之后统计顾客是否购买香蕉和面包，结果可能非常准确，却未必改变了任何人的选择。推荐系统真正要回答的是，系统是否帮助用户发现、比较或决定了原本不会发生的事情。

早期协同过滤经常预测错误，但偶尔命中时会带来惊喜；现代系统可能更少犯错，却更擅长返回用户本来就知道的东西。由此不能简单得出“错误越多越好”，而应先明确任务：找回已知项目、在窄范围内选择，还是发现未知内容。用于找回的 leave-one-out 等指标，若直接拿来证明发现价值，可能测到的只是系统能否复现用户历史。（原文锚点：`I don't care about prediction at all.`、`buy bananas and bread`、`optimize for value.`）

### 点击率和季度收益不是长期关系的同义词

访谈讨论了个性化邮件短期提升销售、随后因发送频率增加而出现退订的回忆案例。由于嘉宾对具体网站名称也不确定，本文不把它写成某家公司的已核实事实；它的作用是提示代理指标的时间尺度问题：一次点击或一次购买可以上升，同时用户对产品的耐心、信任和长期关系可能下降。

Amazon 的个人体验例子也有同样张力。Konstan 在个人账户浏览跑步机、由大学的另一个账户完成购买后，个人账户仍缺少“购买已完成”的信号并继续显示相关商品。这不一定说明技术做不到新颖性或多样性，也可能反映业务更重视让用户回到商店。Konstan 同时保持克制：外部观察者不知道公司内部是否已经讨论过长期价值，也不知道更广的品类发现是否真的更赚钱。长期实验、信任和声誉值得测量，但节目没有给出一套已验证的统一目标。（原文锚点：`what can I squeeze out of my customer this quarter?`、`longitudinal testing`、`the customer is the product and not the partner`。）

### 真实用户平台决定研究究竟能回答什么

Konstan 回顾了 GroupLens、MovieLens 和新闻推荐实验平台的经验。核心价值不只是收集更多评分，而是让研究者观察推荐界面如何改变真实用户行为，并在长期运行的系统里测试文章选择、标题呈现和反馈机制。

这类平台也暴露了实验边界。邮件里的链接点击容易记录，但用户可能只看标题就已获得信息；单一 click 无法覆盖链接点击以外的行为。研究瓶颈因此不只是提出新算法，还包括获得活跃参与者、设计可解释的反馈，以及让界面记录真正与问题相关的行为。访谈中涉及的平台人数和历史细节均为嘉宾回忆，本文不把它们用作量化证据。（原文锚点：`where do they dwell`、`operating for more than a year with public users`、`what links people click on`、`not clicking because they learned what they needed`。）

### 推荐系统是完整系统，不是孤立模型

Konstan 认为，推荐问题只在一部分上是机器学习或计算问题。数据如何获得和整理、推荐如何呈现在界面里、用户当下要完成什么任务、平台如何赚钱，以及生产者、消费者和平台之间的利益如何平衡，都会改变“好推荐”的定义。

这也是 RecSys 需要多方法和多学科视角的原因。一个旅游推荐器还要考虑目的地容量，一个约会系统涉及双边选择，新闻推荐会影响内容生态。单一相关性指标很难代表所有参与者。对话式推荐的潜力也不只是换成聊天框，而是先询问用途、场景和过去经验，再缩小选择范围；节目将其作为方向讨论，并未声称已有通用方案。（原文锚点：`we're bigger than that`、`remaining multi approach and multidisciplinary`、`multi-stakeholder, multi-sided recommendation problems`。）

### 新人应先理解应用，再决定使用哪种模型

访谈最后给出的建议很直接：先沉浸到一个具体应用中，理解用户、运营者和内容生产者的痛点，再判断 LLM、强化学习或其他工具能改善什么。技术栈会变化，但“价值由谁定义、如何观察、由谁承担副作用”不会因为换模型自动消失。

这条建议也解释了整期访谈的主线。推荐系统不是先选择一个先进模型，再寻找可优化指标；更可靠的顺序是先定义情境和价值，再选择数据、实验与算法。（原文锚点：`immerse yourself in an application`、`What's their biggest pain point`、`what is it that I believe my wonderful large language model could improve for them?`。）

## 来源与定位

- 原始节目：[#33: Useful Recommender Systems and 20 Years of RecSys with Joseph Konstan](https://share.transistor.fm/s/c07c7bf6)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 可搜索 `buy bananas and bread`
  - `optimize for value`
  - `longitudinal testing`
  - `what links people click on`
  - `multi-stakeholder, multi-sided recommendation problems` 与 `immerse yourself in an application`

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳的位置，使用原文短语进行定位。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：gpt-5.6-sol
- AI 编辑整理，请以原始节目为准。
