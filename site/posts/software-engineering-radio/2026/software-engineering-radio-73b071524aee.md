---
item_id: software-engineering-radio-73b071524aee
title: Wisprflow CTO 谈人类输入的模糊性："更多上下文"是唯一的解药，而询问要省着用
date: '2026-09-17'
published_at: '2026-04-08'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/04/se-radio-715-sahaj-garg-on-designing-for-ambiguity-in-human-input/'
source_name: 'Software Engineering Radio'
input_type: video_agent_kit_asr
summary: 'Wisprflow 联创兼 CTO Sahaj Garg 剖析人类输入的模糊性：它与噪声、错误的三分法，上下文工程如何让语音模型理解口音与意图，revealed preferences 用退格键学习用户偏好，以及"提问要省着用"的 UX 权衡。'
tags: [AI, 软件工程, 人机交互]
---

# Wisprflow CTO 谈人类输入的模糊性："更多上下文"是唯一的解药，而询问要省着用

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-04-08 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 6371 字 · 阅读约 16 分钟
>
> 标签：[AI](/tags/AI/) [软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) [人机交互](/tags/%E4%BA%BA%E6%9C%BA%E4%BA%A4%E4%BA%92/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/04/se-radio-715-sahaj-garg-on-designing-for-ambiguity-in-human-input/)

## 速读

语音输入公司 Wisprflow 的联创兼 CTO Sahaj Garg(斯坦福毕业、光子计算公司 Luminous Computing 前第五号员工)与主持人 Amey Ambade 聊一个所有 AI 产品都绕不开的话题:人类输入的模糊性。他给出了清晰的三分法——错误是输出的函数,噪声是输入的函数,而模糊性是系统内在的属性,唯一的解药是更多上下文。

最值得带走的三点:风格类模糊(Gen Z 给朋友发消息与给老板写邮件"说的一样、写的不同")只能靠了解意图解决;最好的个性化信号是"显示偏好"——同一个错误你修了两次,系统就该学会第三次不再犯;而对不确定性的 UX 答案是键盘自动更正式的三候选提示——在文本框里呈现确定性,把选择留给用户。

## 主题正文

### 什么是模糊性:与噪声、错误的三分法

Garg 的定义很干净:模糊性是"一件事可能意味着两种或多种不同的东西,而且真的无法分辨是哪种"。他与主持人共同理清了三个常被混用的概念:错误是系统输出的函数,噪声是系统输入的函数,而模糊性是内在属性——沟通时没给全上下文,它就 inherent 地模糊;加入更多上下文、更多输入、去掉噪声,模糊性可以降低,但三者不是一回事。经典的例子是语气:同样一句"that's great",结尾带一点上扬的肯定与平直的敷衍是两个完全不同的意思,只看文字无法分辨;能解开它的只有更多信息——语调、前后的对话、当时的情境。（原文锚点：`errors are a function of the output of the system`；`Ambiguity is kind of intrinsic as a property`；`the kind of only way to resolve ambiguity is with more information`）

### 人类为什么擅长,模型为什么笨拙

人类解模糊靠的是积累的上下文:对话进行到三分钟后,你理解他每一句话都带着前三分钟的背景。而多数机器学习系统"每次只拿到一小片信息,做完任务就忘了"——每一次与 LLM 的交互都学不到下一次。这正是上下文工程(context engineering)作为一个学科崛起的原因:怎么获取上下文、怎么喂给模型、怎么帮它做更好的决策。他在 Wisprflow 的核心研究问题就此引出:怎么给语音模型、音频模型这种上下文——"现在大多数人用的音频模型根本不考虑上下文",如果能在基础层面解决,就能把这种能力从文本域扩展到其他域。做法类比给 LLM 写提示:写代码时你说"更新这个函数",LLM 因为能访问你的代码库就知道怎么做;语音模型同理——把你过去用过的缩写词、你曾经修正过的输出作为信息随时间喂给它。（原文锚点：`they do a task and then they forget about what’s happened`；`the whole discipline has been around context engineering`；`how do you give that kind of context to a speech model or an audio model`）

### Wisprflow 的问题域:语音输入的模糊性从哪来

Wisprflow 的目标是打造"第一个 10 亿人可以依赖为Primary计算机交互的语音界面",从人们做得最多的事——沟通——切入。说话天然充满模糊:对着麦克风咕哝而背景有消防车经过、一句话说到一半自我修正、不知道你想要的输出是清单还是半结构化的思维倾泻。Garg 把模糊性归类,第一类是风格:Gen Z 给朋友发消息的口语和文字写法差异巨大,同一个人跟老板说话方式不变,但"写出来必须不同"——口语里的"但是""不过""就像"这些口头禅在 Slack 里值得保留,在正式邮件里就该清理;决定怎么处理的,是"我在给妻子、联合创始人、队友还是我妈发消息"这种系统通常不具备的意图上下文。第二类是口音、麦克风距离等所有形式的不确定性——重口音的人说三两个词,不知道其口音时甚至分不清是哪种语言;而认识这个人的声音和说话方式,分辨就容易得多。他自己的观察是"每次遇到新口音的人,头两三分钟很难懂,之后突飞猛进"——他们的技术目标就是为机器复刻这种适应过程。（原文锚点：`I just think of all of it as intrinsic uncertainty`；`the way that they speak might still be the same. But the way that that has to be written is going to look different`；`for the first couple of minutes, it’s kind of hard for me to understand what it is they’re saying`）

### 固有模糊与可约简模糊:提问是一门要省着用的手艺

模糊性还分两种:可约简的(加上下文就能解)与固有的(世界上本来就有无法预测的未知)。人类的应对方式是追问——而产品也可以学:不确定用户说了什么,"何不直接问,你说的是这个还是那个?"这与人与人之间没听清时的做法一致。但追问自带摩擦,"如果你在我每个回答后都说'能再说一遍吗',我很快就烦了";问一两次则完全可接受,因为它建立的是"你确实听懂了我"的信心。原则是把追问当作人与人之间导航误解的方式——与其反复要求重复,不如说"你能换个方式解释吗"或"说给我一个五岁小孩听的版本";他给出的交互类比是键盘的滑动输入:同一段滑动轨迹给出了错误的词,按一次退格,系统就给出相似的新候选。（原文锚点：`the world is full of so much inherent uncertainty`；`What if we just asked you, did you say this thing or did you say this other thing?`；`if I was talking to you and after every single answer I gave you, you said, could you say that again, I would be very annoyed`）

### 训练:把上下文"逼"进模型,与标注的两个流派

怎么让模型学会利用上下文?训练技巧很具体:开源音频数据集里每个说话人都说了很多句话,那就把说话人的声音特征作为附加信息挂到每条样本上,再故意往音频里加大量噪声——强迫模型学会"在音频很糟时,依靠额外信息还原真实内容",也就是人为放大模糊性、逼模型依赖上下文。数据标注行业有两大流派:雇标注公司(他点到 Mercor、Micro1 等名字)拿专家级金标准数据,贵而慢但质量高;以及交互式信号——ChatGPT 式的点赞点踩与"二选一你更喜欢哪个",捕捉真实偏好用于后续训练。指令微调(instruction tuning)则是让模型产生目标行为的关键,属于大模型训练配方里的后训练(post training)阶段;框架已相当成熟,难的部分是"清晰地规定模型到底应该做什么"。正式与随意语气的训练实例:用合成与真实数据生成不同语气的回答样本,按形式度等轴打分,建立奖励并用 RL 或监督微调框架训练——"隐式地教会模型,对这个用户来说,更正式、更好对齐的回答长什么样"。上下文压缩在语音域比代码域轻松(代码库的体量是根本挑战),更重要的是"选择相关信息":压缩到主题("知道这是放射科标注,你半路加入也能听懂")、表达一个人的声音、从 30 分钟对话里提取关键的缩写词。（原文锚点：`you could train it with extra vocal information and the audio, and then you could add lots of noise to the audio`；`The whole point of instruction tuning is to get the model to actually perform the kinds of tasks that you want it to do`；`more than compression, it’s about selecting the relevant information`）

### 显示偏好:退格键是最响亮的信号

个性化部分的核心概念是显示偏好(revealed preferences):"让我描述自己的写作风格,我很难用语言说清;让我说邮件、Slack、iMessage 里写得有什么不同,我更说不出来——尽管我知道它们不同。"所以与其问用户,不如从行为里读:Wisprflow 持有的原则是"同一个错误你修两次,理想情况下第三次就不该再修"——修错这个动作本身揭示了你的偏好,无论是口音、风格还是别的什么,系统要把它折回来让你下次不必再教。退格键是其中最强的信号("修正说到底是语音输入里最糟的事——你不信任这个输出,不能直接用它");TikTok、Reels 用观看时长这类参与度信号做类似的事,但 Wisprflow 不用那种信息。人口统计学(年龄推 Gen Z 不爱大写)能教一点,但这些偏好的细微差别很难从粗分桶推出,行为式学习更通用。对"不一致的用户怎么办"的追问,他的回答务实:从言行不一致的人那里学到的,可能就是略不一致的输出;但"只要它感觉像你、懂你、覆盖你做事的范围,用户通常就用得很舒服"。（原文锚点：`Revealed preferences are when an action that somebody takes tells you something about what they like or dislike`；`if you speak in your computer and you fix a mistake twice, ideally you shouldn’t have to fix it again`；`so long as it feels like you`）

### AI 写作的均值回归与不确定性 UX

对"AI 写作为什么总回归均值"的追问,他的诊断在产品层面之上:"这是人们把思考让渡给 AI 的问题。"人之为人的特殊在于信念与在意的事;语音之所以特别,因为它独一无二地属于每个人。解药是用法:他现在用 AI 写作时完全聚焦于"受众是谁、我希望他们带走什么、这是我全部想法的倾泻,请帮我讲得让那个人最易懂"——最新的模型已经能可靠地写出"代表我的想法"的东西;而如果只丢一句"给我生成篇博客",得到的就是"听起来煞有介事却毫无有趣内容"的文字。语气与风格终将易解(分析你的邮件和 Slack 即可),难的是内容本身:"如果一段沟通的内容完全可以被自动化,那它本来就不是一段多有意思的沟通。"对不确定性的 UX,他推崇键盘自动更正的三候选模式:文本框里呈现确定性的完整文本,不确定性被装进几个可点的候选按钮——"给用户太多选择只会带来更多困惑";读不出的名字和缩写,用户自然会拼读出来,系统要接得住这种自然沟通方式,就像打电话时报字母表。推荐系统展示多个选项是因为探索本身就是用户目标,而文本与语音场景"一般来说不要":你说四遍同样的话来让我理解,是很痛苦的交互;ChatGPT 的二选一 UI 让他"心里一哆嗦"——一切都要回到"兑现对用户的承诺"(帮找餐厅时给两三个选项是对的)。（原文锚点：`it’s a problem of people relegating their thinking to the AIs`；`it will come up with something that sounds so plausibly good and yet says nothing interesting`；`That kind of user experience is not bad`）

### 评测、在线信号与跨行业的启示

怎么评估系统对模糊性处理得好不好?两个维度:一致性——对模糊输入,系统的决策应当可预测;以及"还有多少模糊本可以被更多上下文解决"。度量方法是拿已知答案的难例,系统仍做错的部分就是残余模糊性,再加更多上下文看能提升多少。在线信号两分:用户如何与输出交互(改了就是没做好),以及参与度——"用一次就再也不来,我们大概搞砸了;用一次之后又来一百次,那至少还行";但要小心反例——在 ChatGPT 里连说二十次"不是这个意思"也是高参与度的坏信号,"隔天还回来"才是最好的预测指标。这些反馈环既改进模型,更把模型逐步 tailor 到单个用户:话题、缩写、对话风格,人各不同,但可以做到对每个人各自一致。他的一句总结可以跨行业迁移:"模糊性靠更多上下文来解决。你能给系统的上下文越多,它表现越好;如果发现它表现不如预期,先看看能不能再给它一点上下文。"对被欠规格 prompt 折磨的开发者(比如做代码生成产品的),他以 Claude Code 为范例:"它提问的数量恰到好处"——先穷尽已有信息自动推断,模型不自信时才问,并把问题按影响排序——"用户只有这么多的耐心,编码场景大概只够你问两三个问题,那就只问最要命的"。（原文锚点：`the level of ambiguity left in the system is how much you still get things wrong`；`it’s about users engaging over and over, and us collecting information based on their usage to set up feedback loops`；`ambiguity gets resolved with more context`；`it asks just, just the right number of questions`）

## 来源与定位

- 原始节目：[SE Radio 715: Sahaj Garg on Designing for Ambiguity in Human Input](https://se-radio.net/2026/04/se-radio-715-sahaj-garg-on-designing-for-ambiguity-in-human-input/)
- 定位：时间戳取自 ASR 逐字稿。
  - 模糊性的定义与错误/噪声/模糊的三分法（00:01:22–00:02:47）
  - 人类靠积累上下文解模糊,模型做完就忘（00:03:01–00:04:45）
  - Wisprflow 的问题域:语音输入的固有模糊（00:04:54–00:06:05）
  - 风格类模糊:说的一样、写的不同与意图上下文（00:06:25–00:08:22）
  - 口音、麦克风距离与新口音适应（00:08:22–00:10:15）
  - 上下文工程与语音模型的上下文注入（00:10:15–00:12:28）
  - 固有 vs 可约简模糊与"提问要省着用"（00:12:41–00:15:36）
  - 训练技巧:噪声放大模糊与标注两流派（00:15:38–00:18:43）
  - 指令微调、正式/随意语气的奖励训练（00:19:16–00:23:15）
  - 上下文压缩与"选择相关信息"（00:23:15–00:25:09）
  - 推理时延与预填充（00:25:09–00:26:10）
  - 显示偏好:退格键信号与 TikTok 对比（00:26:11–00:29:00）
  - 不一致用户、AI 写作均值回归与解药（00:29:47–00:34:20）
  - 混合语言是"第三种语言"（00:34:31–00:36:02）
  - 不确定性 UX:三候选模式与"兑现用户承诺"（00:36:02–00:39:22）
  - 评测两维度、在线信号与 Claude Code 的提问之道（00:39:26–00:46:37）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 嘉宾姓名（Sahaj Garg）与公司名（Wisprflow）按节目出版方元数据核正；ASR 全篇将公司名误听作 whisper、姓氏偶误作 Kirk，均按出版方信息校正。
- "16% 时间写代码"为上期节目所引 Atlassian 调查口径的转述，"10 亿人""2865 万"类数字均以节目原话为准，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
