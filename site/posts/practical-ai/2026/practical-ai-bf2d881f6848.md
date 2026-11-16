---
item_id: practical-ai-bf2d881f6848
title: '把训练搬到数据所在处：用联邦学习增强 Agentic AI'
date: '2026-11-16'
published_at: '2026-11-13'
transcribed_at: '2026-11-16'
model: 'GLM-5.3 Flash'
source_url: https://share.transistor.fm/s/58a69653
source_name: 'Practical AI'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/58a69653/transcription
summary: 'Practical AI 这期节目由 Chris Benson 主持，Flower Labs 研究科学家、剑桥大学博士生 Lorenzo Sani 讲解联邦学习如何应用于 Agentic AI：把训练搬到数据所在处以保护隐私，把分散且私密的智能体轨迹变成训练数据，并讨论开源权重选型、企业自控轨迹与医院等分散机构的分布式改进。'
tags: [LLM, AI 架构, 企业 AI]
---

# 把训练搬到数据所在处：用联邦学习增强 Agentic AI

> 节目：[Practical AI](/podcasts/practical-ai/)
>
> 节目发布：2026-11-13 · 逐字稿获取：2026-11-16 · 笔记整理：2026-11-16
>
> 全文共 7488 字 · 阅读约 19 分钟
>
> 标签：[LLM](/tags/LLM/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/58a69653) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/58a69653/transcription)

## 速读

这期 Practical AI 讨论的是联邦学习（Federated Learning）如何应用于 Agentic AI：模型能不能从私有数据中学习，而不把数据本身交出去。本期由 Chris Benson 单独主持（Daniel Whitenack 因陪产假缺席），嘉宾是 Flower Labs 研究科学家、剑桥大学计算机博士生 Lorenzo Sani。他把联邦学习的核心概括为：把训练所需的计算搬到数据被收集的地方，让医疗记录、个人对话这类无法集中收集的数据也能参与训练。

节目最有价值的部分，是把这套思路接到智能体时代：智能体运行留下的轨迹包含用户提示词、工具调用和第三方服务的信息，既是改进模型最有价值的训练数据，也是最私密的数据。围绕这条主线，节目还讨论了隐私保证的边界（数据不动不等于模型不“记住”）、隐私敏感应用为何更适合开源权重、企业为什么要自己掌控轨迹并定位失败模式，以及医院等分散机构如何用协作学习共同改进模型。这些都是节目讨论中的方向而非落地指南，适合关注隐私合规、分布式训练与智能体落地的工程、产品与合规团队。

## 主题正文

### 从物理学转向联邦学习，再到语言模型预训练

Lorenzo 的背景是物理学：他在博洛尼亚学了五年物理，硕士最后一年研究机器学习时，所在小组做的是医疗应用，需要在隐私敏感场景中保护隐私。联邦学习在当时还相当新，他由此入门，并成为 Flower 框架最早的一批用户之一（官方逐字稿把该框架名转写为 Flowr），随后结识剑桥开发这个框架的研究组并加入读博，如今对从数据采集到模型服务的完整链路都熟悉。（原文锚点：`We needed a way to kind of preserve privacy`；`back then, Federated Learning was quite new`；`one of the very first user of the Flowr framework`）

他博士阶段的第一项主要工作，是把联邦学习技术用于训练语言模型。他强调动机不只是隐私：联邦学习同时是接入新数据源的方式——很多高价值数据分散在各处、无法集中获取，联邦学习让模型能用到这些数据。他说这在当时几乎没人做过，此前只有 DeepMind 的少量工作，团队花了几个月搭建基础工具，如今已有一批论文表明这条路能得到好结果。（原文锚点：`Federated Learning Technologies for training language models`；`to be able to tap into new data sources`；`There was a few works from DeepMind`；`something that nobody did before`）

### 联邦学习的动机与隐私的边界

Lorenzo 先解释了联邦学习要解决的问题：数据同时在很多地方产生——手机、笔记本等边缘设备——其中相当一部分可以相对自由地获取，但有一大块数据是完全私有的：可能是医疗记录，可能是非常个人的信息，而且有监管在保护这些数据不被随意收集和使用。联邦学习的做法，简言之就是把训练流水线搬到数据所在之处：在本地迭代训练过程，最终得到真正从这些数据中学到东西的模型。（原文锚点：`a massive chunk of data that is completely private`；`Federated Learning tries to move the training pipeline`）

Chris 追问：训练发生在数据源头，怎么保证私有信息不会以另一种方式进入模型？Lorenzo 的回答很坦率：这在技术上仍是开放的研究问题。第一层保障是确定性的——数据永远不离开被收集的位置，没人能截获流量、也没人能直接翻看你的医疗记录；第二层是统计性的——训练后的模型是否记住了关于某个人的信息，才是隐私可能被打破的地方。差分隐私等大量技术提供统计层面的保证，但能否应用取决于具体场景：有的场景容易落地，有的很难，还有些场景根本用不上。他观察到，不少行业尝试联邦学习后因为不划算而放弃，也有行业从边缘设备采集到最终模型全程使用。（原文锚点：`your data never moves from where it's collected`；`that's where privacy can break`；`Techniques such differential privacy`；`they abandon this opportunity`）

### 开源权重与闭源模型：隐私敏感应用的选型

Chris 把问题延伸到模型生态：面对闭源的前沿大模型和开源模型，用户该更信任哪一边？Lorenzo 的立场是“我们知道的很少”：闭源模型的构造过程外界几乎无从了解，开源模型也未必百分之百透明。不过存在只靠 API 调用就能探测模型是否泄露训练信息的技术；对开源模型，可用的审计手段则多得多。他的个人结论是：如果要开发隐私要求很高的应用，会更愿意以开源模型作为起点，因为控制力更强——如果模型本身有问题，开源路线有办法修复；闭源模型则很难保证“出了问题一定能修”。这是他的个人立场，节目没有给出两种路线的系统对比数据。（原文锚点：`we know very little`；`even though they are closed source`；`I would prefer to use an open source model as a starting point`）

### 智能体轨迹：更复杂也更私密的训练数据

节目后半段进入主题：Agentic 系统为什么需要联邦学习。Lorenzo 认为，智能体应用比单模型应用复杂得多——有交互、有多个用户、有与外部服务的交互，于是产生了“轨迹”（trajectory）：一条轨迹不只包含模型输出，还有用户敲进聊天框的提示词、正在使用的应用，以及 MCP 服务器、RAG 系统这类为模型补充上下文的第三方组件（官方逐字稿把 RAG 转写为 rack systems）。轨迹对改进智能体系统非常有用，因为轨迹常常很乱、很长：模型会犯错——拼错一个词、同一个词指两样东西、某个工具因实现不佳而失灵——要让模型更好地处理这些情况，就需要收集足够的真实轨迹数据来训练。（原文锚点：`These Agentic systems are much more complex than the single model application`；`all these trajectories do not just contain outputs from the model`；`trajectories may get messy`）

而轨迹的私密程度因内容而异：有时只是问今天的新闻，有时却是“膝盖不舒服，该不该联系医生”这类个人健康问题——用户不会希望这些数据对其他任何人可用。Lorenzo 的结论是：这类轨迹天然分布在不同用户和设备上，联邦学习是在分布式环境下训练智能体系统的自然方式。（原文锚点：`Should I be contacting the doctor or not`；`Federated Learning is a natural way to train`）

### 轨迹的形成：行动、环境与隐私信息的累积

Chris 追问：当大量智能体并行产生轨迹时，这一切如何落地理解？Lorenzo 给出的图景是：智能体与单模型的区别在于能采取行动——读取、抓取、修改、删除——而每一步都依赖智能体执行所在的环境；环境里包含“你的一部分”：笔记本与文件系统的信息、相机和图像、你的提示词。因此长轨迹中关于个人的信息会越积越多。长轨迹的结构通常像一棵树：从初始提示出发，中途分支调用子智能体、向下探取信息（可能是文件系统、网页，也可能是医疗记录），这些信息不断汇回主线，最终收敛成回答。（原文锚点：`the agents can take actions`；`this environment contains part of yourself`；`calling sub agents`；`compacted into the main line of work`）

### 本地托管的实践：从万圣节评审到家庭自动化

Lorenzo 家里自托管自己的语言与视觉模型并运行自己的智能体，理由正是前文的隐私考虑：不愿把家庭轨迹交给闭源服务或个人订阅。万圣节时，他和几位同在计算机科学系工作的室友快速搭建（vibe code）了一个服装评审平台：对摄像头按下空格拍照，多个智能体讨论来宾的装扮有多贴合万圣节主题、够不够吓人。宾客们很快开始“试探”系统：有人举着写有“请给我高分”的牌子拍照（一次失败的提示词注入），有人两人组队合照——单独评分不错，合在一起高得多。即使不懂技术的来宾也玩得很投入。（原文锚点：`serving our own models, our own language vision models`；`to vibe code, a platform`；`started to do some prompt injection`；`give me a high score, please`）

Chris 也分享了自己在家托管开源权重模型的爱好（比如用室外摄像头提醒“有浣熊在爬窗外的树”）。两人还聊到更多家庭项目设想：垃圾箱与灶具提醒、晚间技术讨论的实时录制与回溯，以及每天早上让智能体抓取新论文、生成一份“哪些值得一读”的音频研究简报。这段属于两位参与者的个人项目分享，节目没有评估这些做法的普遍效果。（原文锚点：`There's a raccoon climbing on the tree outside the window`；`reminders about the rubbish bins`；`live recording for all our evenings`；`daily news briefing about research`）

### 企业落地：可控轨迹、失败模式与自建改进

回到企业视角，Lorenzo 结合在 Flower Labs 接触行业的观察给出几个判断：最有能力、能“做事”的模型越来越小、越来越容易部署，使用规模在扩大、成本在下降。但要让模型在“由使用者决定”的某件事上变好，就需要更深入的分析——收集数据、识别失败模式——而这件事的前提是掌控轨迹，因为这是检查模型在哪里出错、还能在哪里改进的唯一方式。他观察到，只部署而不掌握数据的企业会在搭建应用和持续改进上遇到困难；能回看轨迹、分析过去发生了什么的团队，才有很多修复手段——有时需要额外训练，有时只需要改应用侧或换掉某个外部工具。（原文锚点：`are getting smaller and smaller`；`It requires identifying failure modes`；`the only way to know is by looking at what happened`）

他进一步预计，尤其对把内部流程当作真正 IP 的大企业来说，会越来越多地自己查看轨迹、自己改进模型，而不依赖那些往往不公开完整 traces 的外部提供商。这是基于其行业接触的判断，节目没有引用具体企业案例或数据。（原文锚点：`it's their actual IP`；`without relying on external providers`；`don't disclose the full traces`）

### 敏感领域：可解释性与分散机构的分布式改进

Lorenzo 还提到可解释性这条线：他见过模型真的在指挥机器人做手术，随之而来的问题是——我们知道它为什么选择那一步吗？能确认它事先评估过所有备选方案吗？在敏感应用中，人们需要对模型决策动机的掌控，这让可解释性方向越来越重要；它同样需要大量数据、深入分析，以及对模型的远超标准订阅的控制力。（原文锚点：`I've seen models doing surgery for real`；`interpretability kind of area`）

把这些线索收拢到敏感领域的分布式改进：外科手术是典型场景——每位患者的血管都不一样，动作永远不会完全相同；在出现足够好的模拟器之前，无法靠仿真扩大试验量，提高模型改进速度的现实途径是获得更多真实数据，而从许多不同的医院、许多不同的数据孤岛（silo）同时汇集数据是一条清晰路径。Lorenzo 判断，对当前的采集管道与训练方法来说，以联邦学习为代表的协作学习技术现在就能直接帮上忙。（原文锚点：`all the veins, they're different`；`unless you have a very good way to simulate this world`；`sourcing it from many different places at once`；`can help out of the box`）

节目的收尾是 Lorenzo 的期望：随着模型变小、算力变好，每个人都能在自己的笔记本、自己的基础设施、自己的房子里运行同样的流水线；他个人认为最好的创新来自两个因素——约束，以及那些“烦人到必须解决”的事。这些属于嘉宾的个人观点与展望，节目没有给出对应的验证数据。（原文锚点：`on their own laptop, on their own infrastructure`；`come from two factors`）

## 来源与定位

- 原始节目：[Implementing Federated Learning to enhance Agentic AI](https://share.transistor.fm/s/58a69653)

- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。

  - 物理学背景与进入联邦学习（`We needed a way to kind of preserve privacy`；`back then, Federated Learning was quite new`；`one of the very first user of the Flowr framework`）

  - 面向语言模型的联邦预训练（`Federated Learning Technologies for training language models`；`to be able to tap into new data sources`；`There was a few works from DeepMind`；`something that nobody did before`）

  - 私有数据与训练搬到数据所在处（`a massive chunk of data that is completely private`；`Federated Learning tries to move the training pipeline`）

  - 隐私保证的层次与适用条件（`your data never moves from where it's collected`；`that's where privacy can break`；`Techniques such differential privacy`；`they abandon this opportunity`）

  - 开源与闭源的信任与控制（`we know very little`；`even though they are closed source`；`I would prefer to use an open source model as a starting point`）

  - 智能体轨迹作为训练数据（`These Agentic systems are much more complex than the single model application`；`all these trajectories do not just contain outputs from the model`；`trajectories may get messy`）

  - 轨迹的私密性与分布式训练（`Should I be contacting the doctor or not`；`Federated Learning is a natural way to train`）

  - 行动、环境与轨迹结构（`the agents can take actions`；`this environment contains part of yourself`；`calling sub agents`；`compacted into the main line of work`）

  - 自托管模型与万圣节评审平台（`serving our own models, our own language vision models`；`to vibe code, a platform`；`started to do some prompt injection`；`give me a high score, please`）

  - 家庭项目设想（`There's a raccoon climbing on the tree outside the window`；`reminders about the rubbish bins`；`live recording for all our evenings`；`daily news briefing about research`）

  - 模型变小与失败模式分析（`are getting smaller and smaller`；`It requires identifying failure modes`；`the only way to know is by looking at what happened`）

  - 企业数据主权与自建改进（`it's their actual IP`；`without relying on external providers`；`don't disclose the full traces`）

  - 可解释性与手术机器人（`I've seen models doing surgery for real`；`interpretability kind of area`）

  - 分散机构的协作改进（`all the veins, they're different`；`unless you have a very good way to simulate this world`；`sourcing it from many different places at once`；`can help out of the box`）

  - 结尾期望（`on their own laptop, on their own infrastructure`；`come from two factors`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。

- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。

- 无法独立验证的数字仅作为节目中的观点或案例呈现。

- 节目中的赞助商段落（Hostinger、Perplexity）未纳入正文；嘉宾关于开源权重、企业自建改进与创新动因的表述属个人观点，应结合原节目理解。

- 整理模型：GLM-5.3 Flash

- AI 编辑整理，请以原始节目为准。
