---
item_id: recsperts-86d906321f15
title: '用户不是数据点：Elisabeth Lex 谈心理学感知的推荐系统'
date: '2026-09-13'
published_at: '2026-02-19'
transcribed_at: '2026-09-12'
model: 'GLM-5.3-Flash'
source_url: 'https://recsperts.com/31-psychology-lex'
source_name: 'Recsperts'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/08c95763/transcript.txt
summary: '格拉茨工业大学 Elisabeth Lex 把心理学请回推荐系统：认知、情感与人格三类建模；用 ACT-R 记忆模型预测音乐「再收听」，对小众听众尤其有效；她同时警告——LLM 不能替代真实用户实验。'
tags: [推荐系统, 可解释性]
---

# 用户不是数据点：Elisabeth Lex 谈心理学感知的推荐系统

> 节目：[Recsperts](/podcasts/recsperts/)
>
> 节目发布：2026-02-19 · 逐字稿获取：2026-09-12 · 笔记整理：2026-09-13
>
> 全文共 2642 字 · 阅读约 7 分钟
>
> 标签：[推荐系统](/tags/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F/) [可解释性](/tags/%E5%8F%AF%E8%A7%A3%E9%87%8A%E6%80%A7/)
>
> 🎧 [收听原节目](https://recsperts.com/31-psychology-lex) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/08c95763/transcript.txt)

## 速读

嘉宾 Elisabeth Lex 是格拉茨工业大学教授，即将出任人机交互与包容性技术讲席。这期节目回到推荐系统共同体被遗忘的源头——1979 年的第一个推荐系统 Grundy 发表在认知科学期刊上——并系统梳理「心理学感知推荐系统」的三条路线：认知启发、情感感知与人格感知。她用 ACT-R 认知架构预测音乐再收听行为的研究尤其扎实：频率与近因的记忆激活规律在小众听众身上拟合最好。适合想跳出「离线指标内卷」的推荐系统研究者。

官方逐字稿为 Whisper 自动生成、无时间戳，本文定位使用可搜索原文短语；研究结论以嘉宾口述为准。

## 主题正文

### 「这不可能是全部」：从 MovieLens 报告到心理学

Lex 的学术转折发生在博士早期的一场会议：一连串报告都是「在 MovieLens 上把准确率提高一点点」的离线研究，她当时想——「要么这个领域已经解决了，要么用户侧还有更多事可做」。她选择了后者，并延展出一条明确的研究线：为非主流偏好的用户改善推荐——「听小众金属乐的人却收到 Nickelback 的推荐」。更深层的动机被她一句话点破：推荐系统研究常把人当作数据点，但「人类不是数据点，而是有目标、有记忆、有情绪、有认知能力也有认知极限的人」；那些在计算视角下的「噪声」，其实是心理学（`humans are not just data points`）。

她提醒听众一个历史事实：1979 年 Elaine Rich 提出的第一个推荐系统 Grundy（电视节目推荐）发表在认知科学期刊上，用的是「刻板印象（stereotype）」——从心理学看那只是人类加速决策的启发式。机器学习兴起后，两个共同体渐行渐远；她把原因归于学科壁垒（「模型」一词在两个领域含义都不同）、跨学科研究难发论文难拿经费，以及「数据在手、问题变简单」的错觉——她引用 Robin Burke 的话：解容易的问题总是诱人的（`it's appealing to solve an easy problem`）。

### 三条路线与 ACT-R 记忆模型

2021 年的综述《Psychology-Informed Recommender Systems》把领域分成三类：认知启发（用人类认知模型设计算法）、情感感知（娱乐内容天然触发并依赖情绪选择）与人格感知（外向/内向等特质与多样性、流行度、惊喜度偏好相关）。认知路线的核心工具是 ACT-R 认知架构——一个用数学形式化描述人类记忆的模型：陈述性记忆存储事实知识，记忆单元有「激活值」，激活取决于使用的频率与近因，并按幂律随时间衰减（`this activation decays over time`）。

她的团队把它用在音乐再收听预测上（RecSys 2021 论文）：音乐是少数「重复消费是常态」的领域，而音乐心理学早已发现「熟悉效应」——听得越多越喜欢。他们在真实听歌数据中观察到：高频且近期的收听确实按幂律衰减的规律再次发生，而且这个规律对小众听众拟合得最好——他们的口味更个体化，受社会影响更小（`this function fitted the best for those consumers of niche items`）。把 ACT-R 的激活公式直接实现为排序算法，「效果非常好」。ACT-R 还有扩展组件：扩散组件（建模同听共现）、部分匹配组件（基于内容特征的相似性）与估值组件（建模情感）——后两者在她的数据上贡献有限，原因是特征数据不够丰富而非机制无效。2023 年的后续工作把 ACT-R 与协同过滤（BPR）结合，用社会影响补足多样性并带来可解释性。

这批研究还有一个少有人提的应用展望：许多神经多样性人群（如自闭症谱系）偏好稳定与重复，能准确建模「再收听」的算法对他们可能反而是更高的用户满意度——「这有待研究，但值得研究」。

### 评估的清醒剂：LLM 不能替代用户实验

访谈的另一半是方法论批评。离线指标回答不了「算法更准是否等于对用户更有帮助」;用户中心评估要问的是态度、动机、感知与经历。她举了两个常被忽略的细节：推荐与既有认知冲突时会触发「认知失调」，如果你不追问负面信号的来源，就无法区分是算法差还是「观点不同」；界面质量会先入为主地影响用户对算法的评价——「算法再好，界面糟糕，用户已经带着负面偏差在打分」，首因与近因效应也会左右注意力（`the user interface is not great and the algorithm can deliver the best results`）。

对当下流行的「用 LLM 模拟用户做评估」，她最为警惕：LLM 有偏、不透明、掌握在少数供应商手里，「它们不是人，不能替代真实用户研究」，还要警惕由此形成的自我强化循环。对人格数据（如大五人格）的使用，她反对「因为敏感就一禁了之」——行为数据本就能推断出大量敏感属性，与其自欺，不如在 GDPR 与 AI 法案的框架下、在共同体的价值共识（公平、多样性）之上，让用户自主决定是否上传自己的画像；她即将赴任的包容性技术讲席，正是想把这套「心理学+算法」的能力带给能力各异的用户（`we as a community should move towards having recommendation systems as a real support structure`）。

## 来源与定位

- 原始节目：[#31: Psychology-Aware Recommender Systems with Elisabeth Lex](https://recsperts.com/31-psychology-lex)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 「人类不是数据点」的研究动机（`humans are not just data points`）
  - Grundy、刻板印象与学科分野（`it's appealing to solve an easy problem`）
  - 三分类与 ACT-R 记忆模型（`this activation decays over time`）
  - 再收听预测与小众听众（`this function fitted the best for those consumers of niche items`）
  - 用户中心评估与 LLM 评估批评（`the user interface is not great and the algorithm can deliver the best results`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 整理模型：GLM-5.3-Flash
- AI 编辑整理，请以原始节目为准。
