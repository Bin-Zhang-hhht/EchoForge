---
item_id: software-engineering-daily-df981f9cdbe5
title: '把 AI 带进物理世界：NVIDIA 的 Cosmos 世界模型与机器人开发栈'
date: '2026-11-01'
published_at: '2026-10-20'
transcribed_at: '2026-11-01'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/physical-ai-at-nvidia/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1958-Amit-Goel.txt'
summary: 'NVIDIA 机器人生态与边缘 AI 产品负责人 Amit Goel 讲解物理 AI：世界模型如何从观测预测未来并规划动作；Cosmos 3 双塔架构让推理脑与行动脑共享潜在空间；视频训练倒逼全新数据管线与三台计算机；40 亿参数 Cosmos 3 Edge 实时跑在护照大小的 Jetson Thor 上，开发者约 1000 美元、几天即可上手。'
tags: [AI Agent, AI 架构, 边缘计算]
---

# 把 AI 带进物理世界：NVIDIA 的 Cosmos 世界模型与机器人开发栈

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-10-20 · 逐字稿获取：2026-11-01 · 笔记整理：2026-11-01
>
> 全文共 13646 字 · 阅读约 35 分钟
>
> 标签：[AI Agent](/tags/AI%20Agent/) [AI 架构](/tags/AI%20%E6%9E%B6%E6%9E%84/) [边缘计算](/tags/%E8%BE%B9%E7%BC%98%E8%AE%A1%E7%AE%97/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/physical-ai-at-nvidia/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/10/SED1958-Amit-Goel.txt)

## 速读

NVIDIA 机器人生态与边缘 AI 产品负责人 Amit Goel 做客 Software Engineering Daily，与主持人 Matt Merrill 从零讲起物理 AI（Physical AI）：它与处理文本的数字 AI 之分在于要面对原子——传感器、3D 空间与连续控制；世界模型以对世界的观测为输入，预测世界接下来会发生什么，并顺带承担规划与反事实评估。

最值得带走的四点：一是 Cosmos 3 的"双塔"架构，推理塔低频做规划、行动塔高频生成几十个电机的连续控制指令，两者在共享潜在空间里高带宽通信；二是训练世界模型的数据与算力组织远超文本 LLM，NVIDIA 为此新建 Curator 数据管线，且训练、仿真、部署需要"三台计算机"；三是 40 亿参数的 Cosmos 3 Edge 据称可实时跑在护照大小、2000 teraflops 的 Jetson Thor 上，直接充当机器人 policy；四是对普通开发者，约 1000 美元预算加几天时间就能做出第一个物理 AI 模型。文中产品能力与数字均为 NVIDIA 受访者口径，对想进入机器人领域的软件工程师尤其值得对照收听。

## 主题正文

### 物理 AI 与数字 AI：从比特到原子

Amit 在 NVIDIA 待了 15 年，负责机器人生态——团队对接全球做 AI 与机器人的开发者——同时带做端侧算力的 Jetson 产品线（原文锚点：`I head up our robotics ecosystem at NVIDIA`）。他给出的物理 AI 分界线很直接：LLM 或一般意义上的数字 AI 处理文本，而物理 AI 处理原子，要面对传感器、空间与 3D 信息、视频以及世界的动力学；他给物理 AI 下的定义是"一个能把周围世界的信息作为输入、并预测这个世界接下来会发生什么的模型"（原文锚点：`you're working with atoms`）。

现实中最接近的样本是自动驾驶：他让听众想象旧金山湾区的 Waymo 车辆——从摄像头、激光雷达与执行器取数据，按乘车人的意图决定下一步动作，从对物理世界的观测推出要在物理世界执行的动作（原文锚点：`you'll see the Waymos driving around`）。他同时提醒，物理智能并非新事物——家里的恒温器、路口的信号灯早已是窄用途的物理 AI；真正的变化是类似 LLM 统一翻译、摘要等专用模型的过程正在物理世界重演：一个通用模型理解全部任务、可以用自然语言编程，走向通用的物理智能模型（原文锚点：`general physical intelligence models`）。

### 世界模型：观测进、预测出，规划与反事实一并解决

按 Amit 的讲法，理解世界模型看输入输出即可。输入是对世界当前状态的观测：可以是电机等传感器数据、语音指令、文本提示，当然还有摄像头视觉；因为真实世界本身就是多模态的，世界模型天然多输入多输出。典型输出是一段视频——给定提示与当前状态，模型预测"接下来大概率会发生什么"；自动驾驶场景即"以这个速度、看到周围这些情况，告诉我五秒后世界是什么状态"，再据此决定控制动作（原文锚点：`The typical output of a world model is a video`）。

两类关键能力值得单说。其一是规划：模型能从当前状态推演到达目标状态的计划，也就是"我想到那里，怎么去"的思考过程（原文锚点：`predict the plan to go from the current state to the desired state`）。其二是反事实：先问"如果我执行这个动作，世界会变成什么样"，渲染动作之后的整个世界，先评估再决定做不做——他表示这对机器人极其重要（原文锚点：`predicting what the world is going to look like after you take that action`）。

### 双塔架构：推理脑与行动脑如何协同

主持人请 Amit 拆解"从传感器成像到电机指令之间的一百毫秒"。他给出的是典型流程而非承诺的具体时延：先同步相机画面、各执行器状态与 IMU（惯性测量单元，报告机体各部件姿态）等多源数据，再融合到一起（原文锚点：`you need to synchronize all of this`）；随后把当前帧连同历史帧一起分词送入模型——下一步动作不只取决于眼前一帧，也取决于一点历史。

模型内部分成两件事。规划是推理脑：综合当前观测、历史观测与目标函数，决定往左还是往右、要不要弯腰、要够多远；他说今天这由自回归模型按目标函数预测任务序列来完成（原文锚点：`taking my current observation, my past observations, and my objective function`）。行动生成是另一颗脑，也是难点：机型不同可能要同步控制 30 到 40 个电机，而物理世界的量大量是连续的——电流必须逐毫秒连续生成，与预测离散文本序列属于两类模型问题（原文锚点：`controlling 30 to 40 motors`；`The frequency at which the output must be generated is very different`）。频率上的分工因此是：推理与规划可以低频运转，其输出交给跑得非常快、高频控制全部电机的行动模型；末端再由装在电机旁的小计算机或微控制器按目标位置对电流做每个电机的 PID 闭环控制，它不需要知道其余电机的状态（原文锚点：`A reasoning model that is planning can exist at a low frequency`；`PID is the closed-loop control`）。

两颗脑如何共享同一上下文？Amit 说架构方式有很多种，NVIDIA 正在采用的一种是共享潜在空间：两个模型之间做交叉注意力、共享 embeddings，让"两个大脑"之间有高带宽通信；他把 NVIDIA 最新发布的 Cosmos 3 系列描述为输出侧带推理塔与行动塔、彼此对话的双塔结构，两者在潜在空间里交换信息、共享上下文（原文锚点：`having a shared latent space`；`the reasoning tower and the action tower on the output side`）。为什么不分布式部署、解码后再传给对方重新编码？因为机器人系统必须闭环运行，那样会拖慢带宽（原文锚点：`they need to operate really in a closed loop`）。他给了两个类比：像同一块共享内存上的两个进程，不必复制数据就能在不同频率下共享同一上下文；又如建筑师负责规划、执行者照图施工——两者需要同样的信息，但用法不同（原文锚点：`it's an architect, which is planning everything that you need to build`）。

### 数据管线与"三台计算机"：训练世界模型的真实成本

数据规模先给人量级感：喂给世界模型的数据比文本 LLM 高出若干数量级，因为 15 分钟的视频就是几个 GB（原文锚点：`orders of magnitude more than what you would feed into a text LLM`；`a video of 15 minutes is several gigabytes of data`）。训练的瓶颈不只在 GPU，还在喂料：要并行取回图像、动作或电机控制指令以及对应的文本标注（原文锚点：`You need to retrieve the text annotation for all of that in parallel`）。这类预处理过去跑在 CPU 上，模型经常在等数据；为文本模型建的既有管线撑不住，而 GPU 资源又稀缺，NVIDIA 于是为处理这些数据新建了完全不同的一套栈，并做了名为 Curator 的组件——把大量视频处理、存储成能让训练数据持续供给的形态（原文锚点：`build out a completely different stack in order to process this data`；`We created something called a curator`）。

训练分期与 LLM 类似（预训练、中期训练、后训练），但强化学习的验证工具不同：编码模型的 RL 可以跑编译看对错，而世界模型的职责是模拟世界，必须调用物理仿真器；这类仿真器最适合跑在带光追核心、能做传感器仿真的另一类 GPU 上——整个体系由此变成异构计算问题（原文锚点：`another kind of GPU, which has the ray-tracing cores`；`it has become the heterogeneous computing problem`）。评估场景反而可以离线：让世界模型按一张图片"造出纽约某条街道的世界"来跑评测，负载极重但可以离线慢慢算、尽量堆算力（原文锚点：`That part is super heavy, but that part can also run offline`）；Cosmos 家族本身多尺寸，从能跑在边缘的小模型到 nano 与 super 各档，可分别用于造数据与离线评估（原文锚点：`we have nanos and super models`）。

他总结说，LLM 开发者习惯了"一台 Blackwell 集群走天下"——训练、测试、评估、推理全在最新集群上；物理 AI 却需要三台计算机：训练一台、仿真（造数据或做 RL 后训练）一台、部署还要一台——模型必须再经量化、蒸馏、压缩，才能塞进机器人"大脑"里的小计算机（原文锚点：`it requires actually three computers`；`model quantization, distillation, compression`）。他转述领导 NVIDIA 物理 AI 与人形机器人研究团队的 Jim Fan 的玩笑来概括这种落差：羡慕 LLM 世界的朋友只愁 GPU 不够，而自己这边传感器数据缺一半、同步缺失，训完还要找仿真环境、部署到真机器人后线缆还在断（原文锚点：`I'm always envious of my friends in the LLM world`）。

### 泛化：模仿学习、野外数据与 Real-to-Sim

如何让模型泛化到没见过的场景？Amit 说当下主要两条路。第一条是把数据收集铺进多样环境：以"装箱一双鞋"为例，袋子与鞋盒尺寸各异，靠很多人在不同工厂、不同环境里执行任务来采集，把训练分布拉宽，让真实世界落进分布内——他表示这就是模仿学习正在做的事（原文锚点：`collect data in diverse environments`）。第二条路源于一个硬约束：无论在真实世界采多少数据，真实世界的分布是无限的、连续的，永远会有分布外样本（原文锚点：`the real world has an infinite distribution`）。所以要让推理模型与真实数据配对使用：推理模型从"野外数据"学习——利用可得的文本数据与跨领域采集的视频数据（原文锚点：`learning from data in the wild`）；真实动作数据（人做任务、机器人做任务）负责教会具体技能，两条线合在一起训练。他举例说，只看工厂数据学不到猫和牛长什么样，把家内、户外数据都喂进去，推理能力才能泛化（原文锚点：`not see a cat, or cow coming`）。

仿真是另一条腿：可以安全地测试模型，还能以快于实时的速度跑强化学习，但搭建仿真世界的成本很高（原文锚点：`reinforcement learning faster than real time speeds`）。主持人提到 Reddit 上背奇怪背包的人，Amit 确认那多半是背着相机与激光雷达采集真实世界的人：把真实数据送进模型、生成世界的仿真版本，即他们所说的 Real-to-Sim（原文锚点：`somebody carrying a backpack with some cameras and Lidars`；`what we like to call Real-to-Sim`）。有了仿真版本再做数据增强——楼的颜色不同？光照不同？路更窄？——让数据更接近真实分布；这类数据常用于后训练，比如让通用模型在某个特定街区变得非常强（原文锚点：`What if the lighting was different`）。

### 安全与开放：分层护栏、反事实评估与制衡

物理空间的"幻觉"代价高。Amit 给出分层做法。其一，模型可以保守：遇到没学过的分布外情形就拒绝行动（原文锚点：`make your model really conservative`）。其二，反过来主动把 policy 放进仿真里的恶劣环境打分验证——有些环境甚至不必真实存在——让它在分布外仍然安全（原文锚点：`expose them to those adverse environments in simulation`）。其三，护栏主要加在规划脑上：它类似 VLM 或 LMM，像给 LLM 加护栏那样在规划阶段约束"不许规划不可接受的动作"，而行动脑只执行规划脑输出的方案（原文锚点：`The planning brain is like a VLM, or an LMM`）。其四，要有冗余的外部监督：一个独立观察并验证的要素，最好是一个既能观察、又能接管控制机器人或汽车的 AI——把行动者与监督者分开（原文锚点：`some level of external element that is observing and verifying`）。他强调这些手段要组合使用，目标是既安全、又不把模型压得过度保守而一半任务不敢做。

世界模型在安全上的最大价值是反事实：能当场推演"如果这么做会怎样"。他举 NVIDIA 最近发表的自驾团队工作 Alpamayo 为例——一个推理模型，能预测 10 种不同未来、逐一打分，选出最安全且最符合目标函数的一个去执行，而且是在评估/决策当场进行，不局限于模仿学来的"正确做法"（原文锚点：`They can do counterfactuals`；`self-driving car team called Alpamayo`；`predict 10 different futures and choose one of them`）。可接受行为还有地域性：波士顿与湾区可接受的驾驶行为不同、跨国差异更大，所以要把这些能预测各种反事实场景的世界模型做后训练，让它们学会选择当地可接受的行为——这也是他认为模型应当开放的原因之一（原文锚点：`acceptable driving behavior in Boston is likely different`）。

对"开放模型会不会落入坏人之手"的担忧，他的判断带一个前提：只要怀着好意接触模型的人多于坏意者——他自己也补了一句"希望我们生活在那样的世界"——开放生态反而是安全工具，更多人能为它构建监督系统；他提到约两周前 Huggingface 上的 agent 事故，社区正是用开放模型完成了分诊与修复（原文锚点：`outnumber the people who will have access to this with the bad intention`；`use an open model to actually go and triage that and fix it`）。他给出开放的深层理由：开放的模型可内省、可引导、可加装监控，而封闭模型能做的有限、还会引入单点故障；多样性与选择、一个模型检查另一个模型，是他眼中对安全问题更好的答案（原文锚点：`one model checking the other one is the best way`）。他还拿家务开涮：连装洗碗机的方式夫妻俩都难统一，理应允许每个人按自己的偏好去训练自己的机器人，而不是由某个封闭模型替所有人拍板。

### Cosmos 3 Edge 与 Jetson Thor：装进机器人的世界模型

按 Amit 的介绍，世界模型有多种用途：生成随机世界供 policy 评估、对真实数据做环境增强，以及充当机器人的规划脑——预测多种场景并挑最符合目标函数的一个。充当规划脑的那部分必须跑在机器人本体上，而它不需要生成好看的 10 秒视频，可以收窄到关心的领域，只要能预测未来、控制机器人即可。NVIDIA 从多尺寸的 Cosmos 3 模型做出了 40 亿参数版本，即 Cosmos 3 Edge：输入文本、动作或视频，生成机器人要执行的下一个动作，可直接充当机器人本身的 policy（原文锚点：`a 4 billion parameter version of it`；`generate the next action that the robot needs to do`；`the policy of the robot itself`）。

据他介绍，这个模型能在 Jetson Thor 上实时运行——一台只有护照大小、算力 2000 teraflops 的计算机（原文锚点：`the size of a passport that has 2,000 teraflops of compute`）；他说很多机器人内部装的就是它，例如 1X 机器人与 Boston Dynamics 人形（原文锚点：`the 1X robot, the Boston Dynamics Humanoid, they are all powered by this small computer`）。主持人追问后他确认了护照大小的说法，并补充这里的边缘是机身内、电池供电、一直在线运行的意思——与 CDN 那种地理分布的"边缘"不是一回事，功耗也必须可控（原文锚点：`It's this battery-powered, running on device, plus running all the time`）。

### 开发者上手：从仿真到几百美元的机械臂

Amit 说这个领域过去 12 到 18 个月门槛显著下降：以前硬件贵、为机器人学家设计，NVIDIA 与 Huggingface 团队合作的切入点，正是让习惯写程序的软件开发者开始编程机器人（原文锚点：`much easier in the last, I would say, 12 to 18 months`；`working with the team at Huggingface`）。第一步在仿真：用现有电脑下载仿真器和现成模型、接起来看效果——一台带 4090 GPU 的笔记本就够，也可以用 DGX Spark（原文锚点：`a decent laptop today, which has a 4090 GPU`）。想碰真机，几百美元就能买到一只可训练的机械臂：遥操作采集数据、整理格式、发布到 Huggingface、训练 policy、转换并部署到小 Jetson，让机器人自己干活（原文锚点：`a couple of hundred dollars, you can get a robotic arm`；`train a policy, convert it, deploy it onto the small Jetson`）。他的预算与时间说法是：一台好电脑、约 1000 美元预算、几天时间，就能有第一个能干活的物理 AI 模型（原文锚点：`you can have your first physical AI model doing things`）。

机械臂是第三方生态：可以自己 3D 打印，也有厂商做整套套件寄来；SO-101 机械臂是目前 maker 群体里最流行的（原文锚点：`SO-101 arm, that's the most popular with the makers`）。再往上，如今 1 万到 1.5 万美元就能买到一台人形机器人（原文锚点：`humanoids for $15,000, $10,000 these days`）。选型上他建议按"端到端模型"的思路检索——这类模型像素进、控制出——先选定主流的机器人 policy/AI 模型，再找与之适配、被测试过的硬件，避免为不同硬件改造模型（原文锚点：`taking pixels in, controls out`；`a hardware that works with this particular model`）。Huggingface 上的 checkpoint 正是按"模型+硬件"组织的，例如 action-chunking transformer 这类主流模型有对应具体硬件的 checkpoint，先拼起来跑通第一次、之后再谈定制（原文锚点：`action-chunking transformer model`；`the Huggingface checkpoints are really good`）。

### 五年展望与资深工程师的转型建议

五年之问，Amit 的预期有二。其一，机器人会更常伴身边、更无处不在、更多功能：今天的机器人是为特定目的建造的——人形、Roomba 或搬运整车的工业臂，人们想到的是"身体"而不是"能做十件事的大脑"；五年后他预期人们提起机器人想到的将是一台能做一类事的机器，形态只是载体（原文锚点：`robots that are more around us, more ubiquitous`；`You think about the body, not the brain`）。其二，编程机器人将从专家专属变成示教：过去编程机器人让人望而生畏，得是技师或博士；有了基础模型，演示一次、带着机器人做两次，用数据教机器人完成任务——他承认这在今天的机器人从业者听来像魔法（原文锚点：`show a task, do it one time, do it with the robot two times`）。

对没有机器人背景、但有大量软件经验的资深工程师，他的建议顺序明确：先从仿真开始——依然像在写软件，但会暴露在重力、摩擦这些代码世界里没有的概念与数据面前；熟悉仿真后再上真机部署（原文锚点：`starting, I believe, with simulation`；`exposed to gravity, you get exposed to friction`）。他认为软件开发者与硬件开发者越多协作、软件侧越理解机械约束，系统就会越好（原文锚点：`software developers and hardware developers work together`）；而机器人周边的开源生态已经相当完整——工具、资产、模型都拿得到，可以直接上手（原文锚点：`open-source ecosystem around robotics is pretty strong`）。

## 来源与定位

- 原始节目：[Physical AI at NVIDIA](https://softwareengineeringdaily.com/podcasts/physical-ai-at-nvidia/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 嘉宾职责：机器人生态与 Jetson 端侧算力产品（原文锚点：`I head up our robotics ecosystem at NVIDIA`）
  - 物理 AI 与数字 AI 之分：与原子、传感器、3D 信息打交道（原文锚点：`you're working with atoms`）
  - Waymo 是现实中最接近的物理 AI 样本（原文锚点：`you'll see the Waymos driving around`）
  - 从窄用途走向通用物理智能模型（原文锚点：`general physical intelligence models`）
  - 世界模型的典型输出是预测下一步的视频（原文锚点：`The typical output of a world model is a video`）
  - 规划：从当前状态到目标状态的计划（原文锚点：`predict the plan to go from the current state to the desired state`）
  - 反事实：渲染执行动作之后的世界（原文锚点：`predicting what the world is going to look like after you take that action`）
  - 毫秒级循环第一步：多传感器同步与融合（原文锚点：`you need to synchronize all of this`）
  - 规划脑：综合当前/历史观测与目标函数（原文锚点：`taking my current observation, my past observations, and my objective function`）
  - 行动脑：同步控制 30-40 个电机、连续量高频输出（原文锚点：`controlling 30 to 40 motors`；`The frequency at which the output must be generated is very different`）
  - 推理可低频、行动须高频与电机旁的 PID 闭环（原文锚点：`A reasoning model that is planning can exist at a low frequency`；`PID is the closed-loop control`）
  - 共享潜在空间与 Cosmos 3 双塔（原文锚点：`having a shared latent space`；`the reasoning tower and the action tower on the output side`）
  - 闭环要求驱动共享上下文设计（原文锚点：`they need to operate really in a closed loop`）
  - 建筑师与执行者的分工类比（原文锚点：`it's an architect, which is planning everything that you need to build`）
  - 数据规模远超文本 LLM，15 分钟视频数 GB（原文锚点：`orders of magnitude more than what you would feed into a text LLM`；`a video of 15 minutes is several gigabytes of data`）
  - 训练喂料需并行取回多模态标注（原文锚点：`You need to retrieve the text annotation for all of that in parallel`）
  - 新建数据处理栈与 Curator（原文锚点：`build out a completely different stack in order to process this data`；`We created something called a curator`）
  - RL 验证依赖带光追核心的物理仿真 GPU，整体成为异构计算（原文锚点：`another kind of GPU, which has the ray-tracing cores`；`it has become the heterogeneous computing problem`）
  - 离线评估可承受重负载；Cosmos 家族多尺寸（原文锚点：`That part is super heavy, but that part can also run offline`；`we have nanos and super models`）
  - 三台计算机与部署前的量化蒸馏压缩（原文锚点：`it requires actually three computers`；`model quantization, distillation, compression`）
  - Jim Fan 的"羡慕 LLM 世界"玩笑（原文锚点：`I'm always envious of my friends in the LLM world`）
  - 多环境模仿学习扩分布；真实分布无限（原文锚点：`collect data in diverse environments`；`the real world has an infinite distribution`）
  - 推理模型从野外数据学习（原文锚点：`learning from data in the wild`）
  - 只看工厂数据学不到猫和牛（原文锚点：`not see a cat, or cow coming`）
  - 仿真可安全测试并快于实时跑 RL（原文锚点：`reinforcement learning faster than real time speeds`）
  - 背包采集与 Real-to-Sim、数据增强后训练（原文锚点：`somebody carrying a backpack with some cameras and Lidars`；`what we like to call Real-to-Sim`；`What if the lighting was different`）
  - 安全之一：保守拒绝分布外情形（原文锚点：`make your model really conservative`）
  - 安全之二：在仿真恶劣环境中压测 policy（原文锚点：`expose them to those adverse environments in simulation`）
  - 安全之三：规划脑加护栏（原文锚点：`The planning brain is like a VLM, or an LMM`）
  - 安全之四：冗余的外部观察与验证要素（原文锚点：`some level of external element that is observing and verifying`）
  - Alpamayo 反事实：评估时预测 10 种未来并打分选择（原文锚点：`They can do counterfactuals`；`self-driving car team called Alpamayo`；`predict 10 different futures and choose one of them`）
  - 可接受行为的地域性与后训练开放模型的原因（原文锚点：`acceptable driving behavior in Boston is likely different`）
  - 开放生态的制衡逻辑与 Huggingface 事故修复（原文锚点：`outnumber the people who will have access to this with the bad intention`；`use an open model to actually go and triage that and fix it`）
  - 多样性与"一个模型检查另一个模型"（原文锚点：`one model checking the other one is the best way`）
  - Cosmos 3 Edge：40 亿参数、生成下一动作、可作机器人 policy（原文锚点：`a 4 billion parameter version of it`；`generate the next action that the robot needs to do`；`the policy of the robot itself`）
  - Jetson Thor：护照大小、2000 teraflops，驱动 1X 与 Boston Dynamics 人形（原文锚点：`the size of a passport that has 2,000 teraflops of compute`；`the 1X robot, the Boston Dynamics Humanoid, they are all powered by this small computer`）
  - 边缘即机身内电池供电常开运行（原文锚点：`It's this battery-powered, running on device, plus running all the time`）
  - 12-18 个月门槛下降与 Huggingface 合作（原文锚点：`much easier in the last, I would say, 12 to 18 months`；`working with the team at Huggingface`）
  - 仿真起步：带 4090 GPU 的笔记本或 DGX Spark（原文锚点：`a decent laptop today, which has a 4090 GPU`）
  - 几百美元机械臂与"训练-部署"全流程（原文锚点：`a couple of hundred dollars, you can get a robotic arm`；`train a policy, convert it, deploy it onto the small Jetson`）
  - 1000 美元、几天做出第一个物理 AI 模型（原文锚点：`you can have your first physical AI model doing things`）
  - SO-101 机械臂与万元级人形机器人（原文锚点：`SO-101 arm, that's the most popular with the makers`；`humanoids for $15,000, $10,000 these days`）
  - 端到端模型按"像素进、控制出"检索并按模型选硬件（原文锚点：`taking pixels in, controls out`；`a hardware that works with this particular model`）
  - Huggingface checkpoint 按"模型+硬件"组织（原文锚点：`action-chunking transformer model`；`the Huggingface checkpoints are really good`）
  - 五年展望：更无处不在的多功能机器人（原文锚点：`robots that are more around us, more ubiquitous`）
  - 想到"大脑"而非"身体"（原文锚点：`You think about the body, not the brain`）
  - 示教式编程机器人（原文锚点：`show a task, do it one time, do it with the robot two times`）
  - 转型建议：从仿真开始、接触重力与摩擦（原文锚点：`starting, I believe, with simulation`；`exposed to gravity, you get exposed to friction`）
  - 软硬协作与机器人开源生态（原文锚点：`software developers and hardware developers work together`；`open-source ecosystem around robotics is pretty strong`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 文中的产品能力、算力、参数量与价格等数字均为 NVIDIA 受访者口径，无法独立验证，仅作为节目中的观点或案例呈现；本期主持人为 Matt Merrill。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
