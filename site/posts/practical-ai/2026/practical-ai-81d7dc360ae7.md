---
item_id: practical-ai-81d7dc360ae7
title: '开源模型与物理 AI 的未来：NVIDIA Cosmos 实验室副总裁谈世界模型'
date: '2026-10-17'
published_at: '2026-10-01'
transcribed_at: '2026-10-17'
model: 'GLM-5.3 Flash'
source_url: https://share.transistor.fm/s/217445d3
source_name: 'Practical AI'
input_type: official_transcript
transcript_url: https://share.transistor.fm/s/217445d3/transcription
summary: 'NVIDIA Cosmos 实验室副总裁 Ming-Yu Liu 谈开放模型为何关键：API 能解决问题却不给洞察，物理 AI 的传感器差异与实时约束更需要可定制的开源底座；世界模型从观察中学习物理表示，最新 Cosmos 模型将世界理解与世界模拟融合为全模态模型，但多智能体工厂图景可能还需数十年。'
tags: [LLM, 开源, 多模态, AI 架构]
---

# 开源模型与物理 AI 的未来：NVIDIA Cosmos 实验室副总裁谈世界模型

> 节目：[Practical AI](/podcasts/practical-ai/)
>
> 节目发布：2026-10-01 · 逐字稿获取：2026-10-17 · 笔记整理：2026-10-17
>
> 全文共 9511 字 · 阅读约 24 分钟
>
> 标签：[LLM](/tags/LLM/) [开源](/tags/%E5%BC%80%E6%BA%90/) [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/217445d3) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/217445d3/transcription)

## 速读

这期节目讨论 AI 从云端走向机器人、汽车与工厂等物理系统时，模型生态需要什么。NVIDIA Cosmos 实验室副总裁 Ming-Yu Liu 与 Daniel Whitenack、Chris Benson 对谈开放模型为何关键：API 能解决问题却不给洞察，物理 AI 面对的传感器差异、实时与安全约束，更需要可以拆开、微调的开源底座；他同时界定了物理 AI 的范围，并说明世界模型如何从对世界的观察中学到物理表示。

最值得关注的内容：最新的 Cosmos 模型把世界理解（视频与文本进、文本出）与世界模拟（观察与动作进、视频出）融合为一个支持文本、动作、音频、视频输入输出的全模态模型；嘉宾也给出清醒的距离判断——多智能体协同生产的图景可能还需数十年，人形机器人尚未准备好大规模商用。适合关注开源模型生态、具身智能与世界模型方向的工程师与研究者。

## 主题正文

### 开放模型为什么重要：API 之外的洞察与创新自由

Ming-Yu 从个人经历讲起：学生时代学计算机视觉和机器学习时，社区里有很多开放的代码和模型，「看这些代码和模型帮助我理解概念、帮助我创新」。学术共同体一直这样运作，甚至早于 GPT（transcript 误作 "GBT"）之前就是如此，GPT 过去也发布过开源模型；只是近年模型变大、构建模型需要的资源量级陡增，开放模型的数量随之减少。（原文锚点：`help me understand the concept and help me to innovate`；`GBT also have open source model in the past`）

他并不否认 API 的价值——「API 很好，能解决问题」，但「它们不给你洞察」，不允许人把自己的想法拆开放进去验证；而且要做的事可能适合本地计算，在没有互联网连接的场景里，API 并不总是答案。（原文锚点：`they don't give you the insight`；`you don't have the Internet connection, so API may not always be the solution`）

对 NVIDIA 来说还有一层公司动机。NVIDIA 是加速计算公司，造 GPU 和网络设备，如今也造 CPU 和 SoC；在现代技术栈里，「模型是一种新的库」，开发者在其上构建各类应用。Ming-Yu 说，通过亲手构建模型，NVIDIA 能更好理解该造什么样的计算机和 GPU 架构；而开放模型让用户先测试、组合出面向自己业务的应用，之后也可能发展出自己的模型。（原文锚点：`Model is a new kind of libraries people can use`；`we better understand what kind of computer we should build`）

### 商业视角：创新与选择

Daniel 追问开放模型对 NVIDIA 客户这类商业公司的意义，Ming-Yu 用两个词概括：「创新、自由」。AI 的应用形态不断扩张——从早期的聊天机器人到编码 agent，再到超出预期的各类 agent；未来会出现前沿公司没有预见、需要定制的应用，开放模型「给他们选择，去做目标业务需要的创新」。在他看来，这对整个社会也是好事。（原文锚点：`Innovation, freedom`；`give them choice to do the innovation they need for their target business`）

Chris 补充了一段行业背景，注意这是主持人的观察而非嘉宾陈述：几个月前西方开放模型一度承压，一些「未具名组织」由开放转向封闭，NVIDIA 接过开放旗号让他很高兴；他还提到「即将到来的 Hugging Face 收购」。Ming-Yu 在节目中没有就这笔收购本身展开。（原文锚点：`the Hugging Face acquisition that's coming in`）

### 物理 AI 的版图：定义、垂直领域与人形机器人

Ming-Yu 界定：物理 AI 覆盖几个重要的垂直领域——汽车是其一，工厂自动化是另一个，机器人是其中一个子领域，此外还可能有农业、建筑等。他给出的定义是：物理 AI 是部署在物理设备上的 AI，物理设备扰动世界状态、完成特定任务，结果体现为物质的、可触摸的产物。今天的物理设备里已有一些 AI，但都还比较初步。（原文锚点：`physical AI is a term covers several important verticals`；`physical device perturb the state of the world and complete certain tasks`）

他认为物理 AI 最令人兴奋的形态之一是人形机器人：现在我们周围还没有人形机器人，但将来它们会围绕在我们身边，需要强大的计算机来处理视觉输入、理解人的指令、并对未完成的任务自我修正。他直言这些是 NVIDIA 的巨大商业机会，公司方向与物理 AI 生态是高度对齐的，因此 NVIDIA 想帮助这个领域向前走。（原文锚点：`one of the most exciting forms of physical AI is a humanoid robot`；`great business opportunity for NVIDIA`）

### 开放模型为何契合物理 AI：传感器差异、策略模型与每瓦智能

Daniel 问：物理 AI 的约束是否让开放模型有特殊意义。Ming-Yu 以策略模型为例：策略模型基于视觉观察和用户（或机器）给出的指令，生成动作来完成任务——「观察、指令进，动作出」。麻烦在于每个机器人的传感器配置都不同：有的有两个「眼睛」，有的在夹爪上装相机；自动驾驶汽车有的 11 个相机、有的 7 个，还有的带 LiDAR。每个机器人看世界的方式不同，很难用一个 AI 模型覆盖所有情形。（原文锚点：`A policy model is a model based on the visual observation`；`every robot see the world differently`）

开放模型的价值正在于此：模型自带世界理解或仿真的先验能力，用户可以用自己设备采集的数据做微调——比如初始模型只支持单相机，通过后训练与开放模型扩展出多视角，他强调「用开放模型更容易做到」。效率是另一面：他判断最终的演进方向是「每瓦智能」。（原文锚点：`enabled through post training and open model`；`the primary evolution will be intelligence per per watt`）

### 从云端到设备：物理 AI 改变推理架构

Chris 请 Ming-Yu 给习惯云端 API 的从业者补一堂物理 AI 入门课。核心差异是：机器人要快速反应，处理必须实时、就地完成，而且「很多任务是 batch size 为 1 的推理问题」——云端 API 可以聚合不同用户的请求来填充算力，嵌入式设备没有可聚合的 API 调用。（原文锚点：`lot of tasks is a batch size one inference problem`）

他用云端最流行的语言模型架构说明：LM 基于自回归 transformer（transcript 误作 "auto regress transformer"），是访存受限（memory bound）的，靠聚合 API 调用才能高效利用 GPU 算力；同一架构放进嵌入式设备便无法充分利用算力，因此「某些其他架构可能更高效」——应用不同，需要的架构与同步方式就不同，再叠加实时与安全约束，物理 AI 会催生不一样的架构选择。（原文锚点：`LM is based on the auto regress transformer, so it's memory bound`；`there's a real time constraint and safety constraint`）

### 世界模型是什么：从语言表示到物理表示

Daniel 请他向只用过 LLM 的人解释世界模型，并以自己的观察铺垫：语言只承载了人类体验世界的一小部分——人用眼睛看、用耳朵听、从不同视角看着物理如何演化。（原文锚点：`it's only a small piece of how people experience the world`）

Ming-Yu 给出两条表示路径的对照：语言模型通过处理以语言书写的人类知识建立内部表示，并针对语言表示做优化来生成聊天与代码；世界模型则从对世界的传感观测出发——传感器捕捉世界的不同角度，也捕捉物理如何演化的动态。他认为，通过对这些信号建模，可以隐式编码世界的物理；有了物理的模型，就能开始做模拟；再把世界表示与语言表示连接起来，就能生成解释，帮助理解「为什么发生这件事」。在他看来，这是两种不同的学习表示的方式，用例也不同。（原文锚点：`implicitly encode the physics of the world`；`then you can start to do simulation`）

关于定义他刻意保持谨慎：有人用 world model（transcript 误作 "war model"）指这类模型，对他来说世界模型是解决某些任务的方式，很难用输入输出去定义——「对世界的某种建模，就是世界模型」。（原文锚点：`some sort of modeling of the world is a world model`）

落到 Cosmos 的实践：Cosmos 的使命是为整个生态构建物理基础模型。团队早期就意识到需要世界模拟能力——输入当前观察与动作序列（动作有时可以用文本描述），输出未来会发生什么，比如以视频呈现，将来可能扩展到其他模态。另一侧是世界理解：机器人没能完成任务时（例如障碍物挡住了机械臂的路径），要能解释发生了什么——这需要把世界表示连接到语言，生成人能理解的描述，形式上更接近多模态 LLM：视频与描述进，文本出。（原文锚点：`physical foundation model to help the whole ecosystem`；`the input is the current observation and the action sequence`）

在最新的 Cosmos 3（transcript 作 "COSMO three"）中，两者被融合：用途不同，但建模的是同一个世界，表示可以共享。合在一起就是一个全模态（omni）模型——Cosmos 支持文本、动作、音频、视频作为输入，也支持文本、音频、视频、动作作为输出，开发者可以自选组合在其上构建。（原文锚点：`we actually fuse them together`；`we actually support text, action, audio, video as the input`）

### 规则模拟器与神经模拟：数据驱动的物理近似

Chris 请他厘清「模拟器」与「世界模型」的关系。Ming-Yu 区分了两类：人们花几百年研究世界如何运转并总结成方程，用程序按这些方程模拟环境（比如两个物体相撞会发生什么）——这些是经典模拟器，基于规则；另一条路是把海量视觉观察喂给模型——物体如何相撞、水泼到地上如何散开——模型从数据中近似、预测在相似模式下会发生什么，这是一种「数据驱动的模拟方式」，即基于模式识别的神经模拟。他总结：「一个是基于规则的，另一个更像数据驱动的近似。」（原文锚点：`we consider classical simulators`；`data driven way of doing simulation`；`one is rule based, but the other is more like a data driven approximation`）

### 用世界模型加速策略开发：仿真验证与正则化

Ming-Yu 以自动驾驶说明世界模型的具体用途：开发驾驶策略时会产生很多 checkpoint，过去要比较孰优孰劣，得靠车队和司机把新策略部署到真车上路并记录表现——这「明显不可扩展」，限制了迭代次数。有了世界模型，策略不必先上真车，而是与世界模型交互——左转会看到什么、右转会看到什么——在模拟中验证 checkpoint 的准确性，快速缩小假设范围，只把少数真正有价值的候选拿去实测。他强调技术领域最重要的就是「你能把迭代做多快」。（原文锚点：`interact with a world model`；`you can verify the accuracy of a checkpoint`）

另一条用途是把世界表示当作策略模型的骨干（transcript 误作 "parsing model"）：世界模型生成像素空间的演化，而「像素空间演化与完成操作任务所需的控制信号有强相关」；当数据更有限时，这种相关性会成为训练更好策略模型的「强正则化」。他总结：既然物理 AI 要在真实世界里运行，封装在基础模型中的世界表示会以多种方式派上用场——也因此需要开放，让人们测试并向 NVIDIA 反馈，从而把投入加倍到对物理 AI 生态更重要的能力上。（原文锚点：`the pixel space evolution has a strong correlation to the control signal`；`become a great regularization to help you build a better policy model`；`we need to make it open so that`）

### 多智能体图景、数十年的距离与 NVIDIA 版开放模型

Chris 把话题推向大量物理设备彼此互动的未来。Ming-Yu 给出一个个人色彩浓厚的想象（他两次强调「这是我的观点」）：一家制造商造机器狗玩具，用 LLM 驱动的数字 agent（transcript 误作 "LN"）做高层规划——盘点库存、掌握各地物料；它向 B 工厂的产线 agent 发需求并握手确认，机器人与移动平台把货装上自动驾驶卡车，从 B 工厂运到 A 工厂；产线每个工位都有带视觉检查的机械臂闭环，由另一个 agent 操作。他由此判断「世界将是多 agent 的」——无人机也可以是其中一员，比如茶园用无人机采茶装袋。评判标准回到效率：最终「每美元智能」才是关键，机械臂不需要会解奥数题，更要在特定操作任务上足够灵敏。（原文锚点：`I think the world gonna be multi agent`；`the intelligence per dollar`；`This is my view, by the way`）

对这条路上的挑战，他给出清醒的距离判断：上述多 agent 协同完成生产任务的图景「可能还有几十年之远，我们还没到那里」。正确性验证极其重要——他设想工厂里还需要 supervisor agent 来捕捉尚未被识别的场景；构建物理 AI 也需要强健的机器人，人形机器人演进很快，「但还没到可大规模商用的程度」；要实现完全自动化，机器人还得更聪明、更可配置——比如读一下用户手册就知道怎么装配新任务——这些都还没实现。他认为一家公司做不完这些事，需要整个生态，这正是开放模型重要的原因：「要到达那个美好未来，开放模型将扮演关键角色。」（原文锚点：`might be decades away`；`not yet kind of ready for major commercial use`；`it's difficult for one company to do it alone`；`open model gonna play a critical role`）

NVIDIA 对「开放模型」的定义也比开放权重宽得多：除权重之外还提供训练框架，让人能拿开放模型加自有数据训练出更贴合自身场景的版本；他们甚至开放自建的数据；还有开发者博客、示例配方等形式沉淀的客户用例。他建议研究者善用自己惯用的 agent（无论是 Gemini、GPT 还是 Claude——transcript 误作 "a cow"）去检索材料，未来大家都会确保材料对 agent 易于访问，让 agent 能更好地辅助人类开发者。具体落点：开放模型放在 Hugging Face（transcript 误作 "hacking phase"），核心资源在 GitHub，GitHub 上还有帮助开发者学习他人用法的 recipe cookbook；他说这套做法适用于 Cosmos，也适用于 Nemotron（transcript 误作 "Nemo Tron"）等其他开放模型家族。（原文锚点：`open model is not just have the model open weight`；`We even open source data that we created`；`ask them to look around and find useful materials`；`recipe cookbook`）

## 来源与定位

- 原始节目：[Open models and the future of Physical AI with NVIDIA](https://share.transistor.fm/s/217445d3)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 开放模型的学术传统与 API 的边界（`help me understand the concept and help me to innovate`；`GBT also have open source model in the past`；`they don't give you the insight`；`you don't have the Internet connection, so API may not always be the solution`）
  - NVIDIA 建开放模型的动机：模型是新的库（`Model is a new kind of libraries people can use`；`we better understand what kind of computer we should build`）
  - 商业价值：创新与选择（`Innovation, freedom`；`give them choice to do the innovation they need for their target business`）
  - 主持人关于开放生态与 Hugging Face 收购的观察（`the Hugging Face acquisition that's coming in`）
  - 物理 AI 的定义、垂直领域与人形机器人（`physical AI is a term covers several important verticals`；`physical device perturb the state of the world and complete certain tasks`；`one of the most exciting forms of physical AI is a humanoid robot`；`great business opportunity for NVIDIA`）
  - 策略模型、传感器差异与每瓦智能（`A policy model is a model based on the visual observation`；`every robot see the world differently`；`enabled through post training and open model`；`the primary evolution will be intelligence per per watt`）
  - 物理 AI 对推理架构的不同要求（`lot of tasks is a batch size one inference problem`；`LM is based on the auto regress transformer, so it's memory bound`；`there's a real time constraint and safety constraint`）
  - 世界模型的两种表示路径与定义（`it's only a small piece of how people experience the world`；`implicitly encode the physics of the world`；`then you can start to do simulation`；`some sort of modeling of the world is a world model`）
  - Cosmos 的世界理解与世界模拟融合（`physical foundation model to help the whole ecosystem`；`the input is the current observation and the action sequence`；`we actually fuse them together`；`we actually support text, action, audio, video as the input`）
  - 经典模拟器与神经模拟（`we consider classical simulators`；`data driven way of doing simulation`；`one is rule based, but the other is more like a data driven approximation`）
  - 用世界模型验证策略与正则化（`interact with a world model`；`you can verify the accuracy of a checkpoint`；`the pixel space evolution has a strong correlation to the control signal`；`become a great regularization to help you build a better policy model`；`we need to make it open so that`）
  - 多智能体图景与效率判断（`I think the world gonna be multi agent`；`the intelligence per dollar`；`This is my view, by the way`）
  - 距离判断与开放生态（`might be decades away`；`not yet kind of ready for major commercial use`；`it's difficult for one company to do it alone`；`open model gonna play a critical role`）
  - NVIDIA 的开放模型包与上手资源（`open model is not just have the model open weight`；`We even open source data that we created`；`ask them to look around and find useful materials`；`recipe cookbook`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 归档逐字稿存在明显转写误差，正文按上下文校正，锚点保留原文写法以便检索，主要包括：「GBT」→GPT、「war model」→world model、「parsing model」→policy model、「LN」→LLM、「a cow」→Claude、「hacking phase」→Hugging Face、「Nemo Tron」→Nemotron、「auto regress transformer」→autoregressive transformer、「COSMO three」→Cosmos 3；「for good」与「alpha band media」疑为模型名转写误差，因无法独立确认未在正文采用，其余零散误差按上下文理解，不逐条列出。
- 无法独立验证的数字仅作为节目中的观点或案例呈现。
- 节目中关于多智能体协作的图景是嘉宾明示的个人观点；「可能还需数十年」与「人形机器人尚未准备好大规模商用」是嘉宾给出的时间与成熟度判断，均按节目原貌呈现，未作外推。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
