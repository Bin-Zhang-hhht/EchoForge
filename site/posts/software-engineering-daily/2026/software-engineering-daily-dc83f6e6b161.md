---
item_id: software-engineering-daily-dc83f6e6b161
title: 'AI Agent 时代的反欺诈：设备指纹信号、bot 身份验证与 Firefox/Tor 隐私漏洞披露'
date: '2026-11-17'
published_at: '2026-11-12'
transcribed_at: '2026-11-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/fraud-prevention-in-the-age-of-ai-agents/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/11/SED1979-Keshia-Rose-.txt'
summary: 'Fingerprint 开发者关系负责人 Keshia Rose 对话主持人 Gregor Vand：设备指纹如何用一百多个信号在不依赖 cookie 的情况下识别设备，短信 pumping、AI token 滥用这类换标签老滥用怎么防，如何用 web bot auth 区分合法 AI agent 与恶意 bot，和 Firefox/Tor 隐私漏洞的披露。'
tags: [安全, AI Agent, 企业 AI]
---

# AI Agent 时代的反欺诈：设备指纹信号、bot 身份验证与 Firefox/Tor 隐私漏洞披露

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-11-12 · 逐字稿获取：2026-11-17 · 笔记整理：2026-11-17
>
> 全文共 18897 字 · 阅读约 48 分钟
>
> 标签：[安全](/tags/%E5%AE%89%E5%85%A8/) [AI Agent](/tags/AI%20Agent/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/fraud-prevention-in-the-age-of-ai-agents/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/11/SED1979-Keshia-Rose-.txt)

## 速读

Fingerprint 开发者关系负责人 Keshia Rose 本期对话主持人 Gregor Vand：设备指纹如何用一百多个信号在不依赖 cookie 的前提下识别设备与浏览器，短信 pumping、AI token 滥用这类换标签老滥用怎么防，如何区分合法 AI agent 与匿名或恶意的 bot，以及 Fingerprint 研究团队发现并披露 Firefox 私密浏览与 Tor 浏览器隐私漏洞的故事。

最值得带走的三点：一是指纹与 cookie 的本质差异——cookie 存在用户浏览器里、随时可被清掉，指纹读的是设备自身特征组合，反欺诈因此从"记住你"转向"认出你"；二是 AI agent 是识别的新边疆——web bot auth 让 agent 用密码学签名自证身份，但"不报名字"的 agent 只能靠启发式与信号叠加来判断；三是识别与隐私的边界——她的立场是站内识别可以做、跨互联网建画像不做，发现能跨站追踪人的安全问题时选择披露。

## 主题正文

### 嘉宾轨迹：从行为健康分析师到开发者关系

Keshia Rose 的入行路径与典型工程师不同：她最早在一家非营利组织做行为健康分析，后来因为喜欢上合作过的一家公司而转进科技行业——那是 Tableau Software。她从销售工程师做起，之后转到产品侧做 PM，同时兼做一些开发者关系；离开 Tableau 后去 Algolia 继续做 PM，发现还是想念开发者关系这条线，于是把下一份工作明确瞄准开发者布道方向，最终加入 Fingerprint。（原文锚点：`I actually started out as an analyst in behavioral health`；`I started there as a sales engineer`；`I left Tableau to go to Algolia as a PM`；`That's how I ended up at Fingerprint`）

她对开发者关系的自我定义很朴素：参与社区，但更重要的是"能不能真正帮人把你的产品用起来"——做内容、跑活动、办网络研讨会、写示例代码和演示应用、出教程，让开发者看完能说出"哦，原来是这么接的"。她和 Fingerprint 的工程师协作密切：工程师拿出原始内容或基础代码，她负责打磨并推向市场。（原文锚点：`can you actually help people use your product`）

主持人 Gregor Vand 在节目介绍中被写明是安全方向的技术人，此前在网络安全、网络保险和通用软件工程公司担任过 CTO。（原文锚点：`Gregor Vand is a security-focused technologist`）

### 从 FingerprintJS 到 Fingerprint：开源内核与商业分界

公司脉络：FingerprintJS 起源于 2012 年，是 CTO 兼联合创始人 Valentin 创建的开源项目；按她在节目里的说法，大约"2019，或者可能 2020"年做成了产品和完整的 SaaS 公司，成为去掉"JS"的 Fingerprint——去掉后缀是因为业务早已不止网站和浏览器。（原文锚点：`Fingerprint started out as FingerprintJS way back in 2012`；`our CTO and Co-Founder Valentin created the open-source project`；`he actually made it into a product and a full-on SaaS company`；`we do more than just websites and browsers`）

开源版与商业版的关系：开源版给了商业产品最核心的那部分能力，商业版在其上扩展；开源版完全是客户端的，商业版多了服务端组件和一整套 smart signals。（原文锚点：`The open-source version is all client side`；`It also includes a server-side component and a whole bunch of smart signals`）

技术原理是看浏览器的各种特征——画特定图像的方式、装了哪些字体和插件、屏幕分辨率、操作系统——把这些拼成一个哈希，之后用它来认出你。用途是双向的：正面是"记住我的设备"，比如登录银行时少输几次密码；反面是反欺诈——上次这个设备或浏览器用过被盗信用卡，就别让它再回来。（原文锚点：`It basically looks at the different characteristics of your browser`；`the way you draw certain images, the types of fonts, or plug-ins you've got installed`；`put them together into a hash that can then be used to identify you later`；`they used a stolen credit card`）

### 为什么反欺诈不能靠 cookie

她的核心论点：做对了的指纹识别不需要 cookie。cookie 的麻烦在于随时会丢——被清掉、被删掉，或者一开始就被拦住不让设。个性化场景里这也许无所谓，但反欺诈与反滥用的对手恰恰会主动删 cookie：一删，你就彻底跟丢了这个人，连一点可疑与否的信号都没有了。指纹识别（她强调不只是她家的产品）的本质，是不依赖任何"谁都能随手改掉"的存储数据。（原文锚点：`Fingerprinting, when it's done right, at least, doesn't require a cookie`；`The cookie can get cleared, it can get deleted, or it can be blocked`；`doesn't require or rely on storing data that anyone could just manipulate`）

主持人补充了一个舆论语境：就在几周前，Hacker News 上还有人对"指纹识别"这个概念本身持负面看法——不是针对这家公司，而是这项技术。他把本期节目的立场摆在前面：指纹有很多正面用例，包括帮公司分清该服务真人还是"非真人"。（原文锚点：`something on Hacker News, maybe a couple of weeks ago`）

### 接入方式与信号体系：一百多个数据点、smart signals 与 suspect score

接入是标准的开发者路径：网页端加几行 JavaScript 客户端 agent，想在什么时候识别访客就调一个简单的 get 函数，拿回一个 event ID 和访客 ID；最佳实践是把结果发到自己的后端去确认拿到的是可信数据，后端侧有覆盖各框架各语言的 SDK——说到底就是一个 JSON API。返回的属性包括：这个人在不在篡改浏览器？走不走代理？在不在某处的黑名单上？有没有克隆你的 App？是不是在冒充多个人？全部以布尔值和对象的形式回来，没有需要迁就的专有工具链。（原文锚点：`add our JavaScript client agent`；`You call a simple get function and we return back to you an event ID`；`best practice is you're to send it to your backend`；`it's just a JSON API`；`is this person tampering with their browser`；`Are they cloning your app`；`There's no proprietary tooling you have to finagle with`）

信号侧，这份 JSON 响应里有一百多个数据点（官网 demo 可以看到你自己浏览器的完整输出）。客户的用法大致三种：第一种把全部原始数据倒进自己的机器学习模型；第二种看 smart signals——从原始属性推导出的二次信号，比如"在不在用 VPN"，还会拆出为什么判断在用 VPN：时区对不上？某个特定出口节点？第三种没工夫挑信号，直接用 suspect score，把所有信号揉成一个数字——数字越高，触发的信号越多、越可疑。她把 Fingerprint 定位成一家"数据公司"：给你能做决策的数据，怎么用由你。（原文锚点：`there's over a hundred different data points`；`Some customers will just dump everything into their own machine learning models`；`Those are more of like a derived signal`；`We'll break it down by why we think they're using a VPN`；`Is there a time zone mismatch`；`suspect score that bungles all of them up together into just one number`）

### 默认不拦截：VPN 单个信号说明不了什么

她强调产品开箱即不做任何自动拦截或放行，规则由客户用 rules engine 自定义——只有当你所在的行业有地区合规要求时，VPN 才可能属于该拦的情形；对普通网站，用 VPN 已经是常态，信息给你，怎么处置看你的业务和用例。（原文锚点：`We out of the box don't automatically block, or allow anything`）

她给了一个规模参照：去年做了超过 230 亿次识别；在这些识别里，VPN 标志升到大约 17%——她紧接着补了一句"大概是这个数，别引用我"，差不多五分之一。她的结论是 VPN 单独说明不了什么，关键问题是它对你的业务是不是欺诈信号；Fingerprint 也提供配套工具，把你标记过的欺诈数据喂回去对比各信号，告诉你对你的欺诈类型而言哪些信号最常出现。（原文锚点：`We did over 23 billion identifications last year`；`I think we saw VPN raised to 17%`；`Don't quote me`；`You can give us your fraud flagged data`）

主持人的亲历恰好是反面教材：他住在新加坡、常要处理英国政府网站的事务，在公共场所挂着 Mullvad 就被拦，下了 VPN 又因为"你在新加坡"接着被拦。她的回应是方法论：VPN 永远不该单独用作拦截依据，要看其他信号——同时还篡改浏览器？可疑程度上升；只有 VPN？大概率没事，最多加一步额外验证确认是你。（原文锚点：`I live in Singapore, but I like to access sites for things in the UK`；`I'm using Mullvad`；`it's not just a signal to use by itself to block somebody`；`Were they also tampering with their browser`）

### 欺诈用例图谱：从账户安全到 SMS pumping

主用例围绕账户安全：账户接管、免费试用滥用、新账户欺诈、账户共享；再往外是支付欺诈——拒付、争议；另有少量个性化场景。她把产品的适用面概括成一个问题：这个设备以前做过什么？围绕它有哪些风险信号？覆盖从封禁规避到付费墙执行的一整段光谱。（原文锚点：`account takeover, free trial abuse, new account fraud, account sharing`；`payment fraud as well, charge back, dispute`；`ban evasion to paywall enforcement`；`what has this device done before`）

她入职 Fingerprint 约三年，说每周都会学到新的欺诈花样，举的例子是 SMS pumping：登录时下发的一次性验证码短信是要花钱的，尤其发给按条计费的运营商号码时，费用算在发起下发的那家公司头上；灰产或欺诈运营商会靠这套机制赚分成，于是有人反复触发验证码下发——公司不发验证码不行（真用户要登录），却又被刷出巨额短信费。这类场景下光有 bot 检测不够，得看清是哪些设备在干这事，而不能只靠 IP 限流保住登录页。（原文锚点：`somebody was solving the problem of SMS pumping`；`You end up paying for that text message to be sent`；`spamming these one-time passcodes over and over and over again`；`besides just an IP rate limit`）

### AI token 欺诈：换标签的老滥用

问到 AI token 欺诈，她的判断是：本质就是同一批滥用贴上了新标签。免费额度滥用——注册一堆假账号去薅免费 token 和额度，就是 AI 版的免费试用滥用；用被盗信用卡买 token 配额，是老问题换了标的物；用账户接管手段进别人的账号、烧别人的额度，还是账户接管。变化只在标的物变成了"又热又值钱"的 token。（原文锚点：`AI token fraud is really just the same types of abuse with a new label`；`racking up a bunch of fake accounts to try and use it all up`；`using stolen credit cards to buy`；`using account takeover tactics to hack into somebody else's account`）

### Firefox/Tor 隐私漏洞：IndexedDB 返回顺序如何变成跨站追踪

本期最受关注的段落是 Fingerprint 研究团队的一次发现。她先声明自己不是研究者、只做力所能及的转述：问题具体出在 Firefox 私密浏览模式，同样适用于 Tor 浏览器，围绕的是 IndexedDB。IndexedDB 是网站在浏览器里存数据的又一种方式（结构化格式，一个网站可以建一到多个数据库），通常用于维持状态或离线应用。（原文锚点：`it was specifically within the Firefox private browsing`；`which also applied to Tor browser as well`；`The idea here was around the index DB`；`Index DB is another way to store data`）

漏洞机制的关键在"取回数据库列表的顺序"。假设一个站建了 A 到 P 一串数据库，哪怕按顺序创建，浏览器返回的顺序也不一样——带有随机性，她的理解是基于 UUID 和哈希方式。这个"随机出来的独特顺序"本身就能当作浏览器标识。更糟的是，这个顺序可以被其他站点读到：不同网站都建同名的一串数据库时，UUID 相同、随机顺序也相同，于是可以拿这份"固定下来的随机序"从站到站追踪你。而且只有彻底退出整个进程（不是关标签页）才会换一个新顺序。（原文锚点：`the actual order that they get returned back to me is not the same order`；`based on the UUIDs and the way that the hashing worked`；`that ordering of the databases can be accessed by other sites`；`same randomized order to track you from site to site`；`only if you fully close, like fully quit the process`）

### 披露的边界：站内识别与跨站追踪

她顺势讲清了 Fingerprint 自己的隐私立场：不喜欢被跟踪、不喜欢别人给我们建数据画像，产品设计上就让跨站追踪没法用——客户 A 认出你的手机得到一个访客 ID，客户 B 得到的是完全不同的 ID。这个 Firefox/Tor 的问题则不同：它可以在任何网站上使用，于是成了要披露的对象。（原文锚点：`At fingerprint, we do not like being tracked`；`If customer A identifies my phone`；`Customer B is getting a completely different visitor ID`）

至于一个信号"该不该追踪"的判断，按她的转述大致是：凡是能拿来跨互联网追踪人的，一概不愿支持——尤其在 Tor 浏览器或 Firefox 私密模式里，用户可能在做政务或异见相关的活动，这类追踪能力不该轻易落到多个网站手里。"这个人在你站点上有什么访问权限、在你的业务里做什么"，这个可以谈；跨整个互联网给人建画像，不行。另外信号强度也是考量：变化太频繁、不够稳定可靠的信号，未必会去共享或披露。而一旦判定是真安全问题——就像这次的 Firefox/Tor 问题——就一定会披露。这类披露不常发生，"做过几次"；判断维度归结为"我们是否认同其隐私影响？它是不是真的好信号？"（原文锚点：`to track people across the Internet`；`especially in something like Tor browser, or Firefox private mode`；`how this person has access to your site and what they're doing in your business`；`not try and build profiles on people, or track them across the entire Internet`；`the strength of the signal goes into it as well`；`Whenever we feel like it's actually a security issue`；`do we believe in the privacy aspect`）

### 声音与画布：指纹信号的熵从哪来

主持人问到的"声音特征"确实存在——她的说法是音频指纹：播放一段用户听不见、浏览器里也不显示为正在播放的噪声，你的硬件播放这段声音的方式是独特的；她提到官方博客有专文介绍。同理还有视觉 canvas：你的电脑画某个形状、渲染某段文本的方式，由操作系统、硬件、显卡共同决定，非常独特。这些都是往设备标识里加熵的途径，而 Fingerprint 总共看一百多个特征，各自强弱不同，关键在组合：改一处（比如升级浏览器）不应让整个指纹散架，指纹要比单一特征稳定才行。（原文锚点：`audio canvassing, or audio fingerprinting`；`You don't hear the noise`；`The way your computer draws a certain shape`；`very unique based on your operating system, your hardware, your graphics card`；`if you change one thing, if you upgrade your browser, that shouldn't cause the whole Fingerprint to disintegrate`）

### 识别 AI Agent：web bot auth 与"没报名字"的盲区

进入 agent 话题。主持人把浏览器侧的 agent 分成两类：基于浏览器自动化的 agent（他称之为 agent V1，前沿实验室正把这类能力铺到各处），以及直接发 HTTP 请求、更像一个应用而非浏览器的 agent。她的回答是分层叠加：原有的 bot 检测启发式（bot 的特征、活动模式、已知浏览器的知识）继续用，再叠加 web bot auth 这类新技术——让 agent 对自己的请求头做密码学签名，从而验证"这真的是 ChatGPT 或 Claude"。（原文锚点：`browser automation-based agent`；`We layer a bunch of different techniques together`；`things like web bot auth, which allow these agents to cryptographically sign`）

难点是并非所有 AI agent 与 AI 助手都会自报家门。她以当时所知举例：Meta 的 muse（至少截至节目时她所知）并不公告自己的身份。这类流量大概率是真人想正常使用你的网站，不能直接拦，只能叠加信号判断：对象特征的启发式、工作频率和速度、web bot auth，结果仍以那个简单 JSON 返回——判定是"好 bot"还是"坏 bot"由后台完成，她解释对"坏 bot"主要指"没报名字"的：不一定是坏，只是没表明身份。Fingerprint 会告诉你"这是 Claude""这是个 Perplexity 浏览器"之类的信息与细节，怎么处置由你。（原文锚点：`at least as of today, as far as I know`；`Meta's muse does not necessarily announce itself`；`how often, how fast is it working`；`we mostly mean it didn't announce itself`；`This is Claude, or it's a Perplexity browser`）

她预告即将推出一个 agent 评估（她原话是"下个月"）：逐项检查你能不能看到这些 bot、分清是哪类 agent、能不能给合法 agent 一条好走的路径——能下单吗、能订房吗——同时仍在防欺诈、能查授权。主持人补充了产业侧现状：前沿实验室正找上门来说"我们想在你平台上买东西"，公司的回应是"行，但我们怎么确认是你？"她把当下形容为"狂野西部"：过去的问题是"是不是 bot"，现在的问题是"我们想要其中一些 bot"，人们正忙着弄清如何在拦住欺诈的同时放行想用 agent 访问站点的人。（原文锚点：`coming out in the next month, actually, a assessment`；`Can they make a purchase? Can they make a booking?`；`But how do we know it's you`；`is it a bot or is it not a bot`；`Now it is like the wild, wild west`）

### web bot auth：正在成形的标准与免费测试页

web bot auth 还是 IETF 草案（主持人点明），她称之为"还在成形中的标准"，并提到各家都在搞自己的方案——Google 在做一些东西、Visa 在做一些东西，尤其电商方向——但她认为 web bot auth 是一个相当扎实的起点。机制分两层：第一层，bot 对自己发送的请求头做密码学签名，对照注册表确认"是的，它是它自称的那个 bot"；第二层由 Fingerprint 补充——自称是谁不等于就是谁，他们实际核验过某些 bot 确实归属其声称的公司，"我们核实过这些具体的就是 ChatGPT、Claude 等"。（原文锚点：`It's a draft on IETF`；`it's still an emerging standard`；`cryptographically sign your headers that your bot is sending`；`there's a registry that we can compare to`；`We verify that these specific ones are ChatGPT, Claude, etc`）

配套的 web bot auth 测试页是免费工具：把你的 agent 指过去，它会告诉你密码学签名配置对不对、缺不缺请求头，"认得你"还是"你得修一下"——目的是让合法的 agent 和 bot 提前备好这类标准。它专为 bot 设计，用浏览器打开普通网页拿不到结果。主持人试过后专门推荐了它的界面，形容为"赛博朋克 CLI"。web bot auth 只是 Fingerprint 识别手段之一。（原文锚点：`It's a free tool anyone can use`；`if you've configured your cryptographic signatures appropriately`）

### 不进浏览器的 bot 与 automation intelligence API

很多 bot 并不走浏览器：直接发 HTTP 请求，甚至根本不加载 JavaScript。为此 Fingerprint 还有一个处于 preview 的新特性，以及即将推出的 automation intelligence API，作为额外一层帮你找到"不加载页面"的那批请求——部署在边缘、可加进中间件，速度很快。照例：信息给你，决策归你。（原文锚点：`Many of these bots are not using browsers to fetch information`；`maybe they're not even loading JavaScript`；`We also have a automation intelligence API coming out as well`；`You can add it to your middleware`）

### 没有 CAPTCHA 的体验，与 CAPTCHA 的失效

整套识别发生在后台，终端用户什么都看不到、不被挑战——没有拖拼图、没有点消防栓，也无须做任何事来证明自己不是 bot。在她看来反欺诈和用户体验是一体两面：bot 检测保护你的页面、登录和表单，而能轻松判断"你不是 bot"，就不必让人做谜题进门。主持人对此很有共鸣，讲了他被某 VPN 服务商"在 Google 上无限循环验证码"逼去用 ChatGPT 搜索的往事，并许愿等着再也用不上验证码的那天。她的回应颇为釜底抽薪：如今 bot 自己就能解掉很多验证码——"这些验证码到底拦住了谁？"（原文锚点：`All of this is happening in the background`；`There's no drag the puzzle piece, or click on the fire hydrants`；`The bot stuff helps you protect your pages, your logins, your forms`；`bots can solve many of these captchas anyways`；`Who are we really stopping with these`；`never have to do one of these puzzles ever again`）

### 面向 AI 的工具链：MCP server、CLI 与 AI 安装页

产品侧最近一串动作都指向"让 AI 工具接上 Fingerprint"。MCP server（主持人提到三月底上线、应该已 GA；她确认 MCP server 是第一块，内含一个上手的 onboarding skill）主打数据分析：用自然语言追问"那次 bot 攻击怎么回事、从哪来、有没有设备集群欺诈更多"，不必自己拉 SQL 做分析，后续还会继续扩展。（原文锚点：`launched an MCP implementation back in March`；`The MCP server, that was the first piece we did`；`It does include an onboarding skill to get you started`；`It helps you dig into that with natural language`；`without having to pull up a SQL`）

之后是新发的 Fingerprint CLI：问你要解决什么用例、帮你从零建号配置，几分钟跑通并把 Fingerprint 直接集成进项目——比如"我要保护登录页"，它就给你配在那里，还内接了 AI；配套的 skills 陆续推出（先是各 quick starts，按用例的 skills 在下季度）。本周还上线了 AI 安装页：不管你是 vibe coder 还是资深工程师，只要在用 AI 工具，就把接入 Fingerprint 做到最容易。（原文锚点：`we've launched our CLI`；`You can get off and running in a few minutes`；`this week launched a new page for AI installation`；`if you're a vibe coder, or if you're a senior engineer`）

### 上手路径：demo、playground 与两份报告

想先看效果，她指的路是 demo.fingerprint.com：playground 里能看到前述 smart signals 和给你的原始 JSON 输出，直接来自你当前浏览器，可自行拆解；另有各用例的交互 demo（账户接管、拒付、付费墙、账户共享等），可以自己"试着接管一个账号"体验识别过程，也能随时重置。（原文锚点：`demo.fingerprint.com`；`This is where you can see all those different smart signals`；`the raw JSON output that we would give you`）

报告方面，她点名 device intelligence report（她自己提议做的那个，颇为自豪）：逐项拆解这些信号是什么、检测什么、出现频率如何——VPN 是五分之一，不算大事；移动端 App 克隆占比小得多（节目原话 "much smaller take"），反而是"有事发生"的更强信号。另有面向金融服务的 AI 流量调查等行业报告（金融、旅行与酒店业都做过），以及一系列网络研讨会。（原文锚点：`financial services AI traffic survey`；`It breaks it down piece by piece`；`The VPN, we saw it's one in five`；`app cloning on a mobile device, much smaller take`）

## 来源与定位

- 原始节目：[Fraud Prevention in the Age of AI Agents](https://softwareengineeringdaily.com/podcasts/fraud-prevention-in-the-age-of-ai-agents/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 嘉宾从行为健康分析到 Tableau、Algolia 再到 Fingerprint（原文锚点：`I actually started out as an analyst in behavioral health`；`I started there as a sales engineer`；`I left Tableau to go to Algolia as a PM`；`That's how I ended up at Fingerprint`）
  - DevRel 的自我定义（原文锚点：`can you actually help people use your product`）
  - 主持人背景（原文锚点：`Gregor Vand is a security-focused technologist`）
  - FingerprintJS 2012 起源与约 2019/2020 年公司化（原文锚点：`Fingerprint started out as FingerprintJS way back in 2012`；`our CTO and Co-Founder Valentin created the open-source project`；`he actually made it into a product and a full-on SaaS company`；`we do more than just websites and browsers`）
  - 开源版与商业版分界（原文锚点：`The open-source version is all client side`；`It also includes a server-side component and a whole bunch of smart signals`）
  - 指纹原理与"记住设备/拒绝欺诈设备"两个方向（原文锚点：`It basically looks at the different characteristics of your browser`；`the way you draw certain images, the types of fonts, or plug-ins you've got installed`；`put them together into a hash that can then be used to identify you later`；`they used a stolen credit card`）
  - 指纹与 cookie 的差异（原文锚点：`Fingerprinting, when it's done right, at least, doesn't require a cookie`；`The cookie can get cleared, it can get deleted, or it can be blocked`；`doesn't require or rely on storing data that anyone could just manipulate`）
  - 舆论语境：Hacker News 上的负面看法（原文锚点：`something on Hacker News, maybe a couple of weeks ago`）
  - 接入方式：JS agent、后端核验与 JSON API（原文锚点：`add our JavaScript client agent`；`You call a simple get function and we return back to you an event ID`；`best practice is you're to send it to your backend`；`it's just a JSON API`；`is this person tampering with their browser`；`Are they cloning your app`；`There's no proprietary tooling you have to finagle with`）
  - 一百多个数据点与三种用法（原文锚点：`there's over a hundred different data points`；`Some customers will just dump everything into their own machine learning models`；`Those are more of like a derived signal`；`We'll break it down by why we think they're using a VPN`；`Is there a time zone mismatch`；`suspect score that bungles all of them up together into just one number`）
  - 默认不拦截与规模参照：230 亿次识别、VPN 约 17%（原文锚点：`We out of the box don't automatically block, or allow anything`；`We did over 23 billion identifications last year`；`I think we saw VPN raised to 17%`；`Don't quote me`；`You can give us your fraud flagged data`）
  - VPN 不应单独作为拦截依据（原文锚点：`it's not just a signal to use by itself to block somebody`；`Were they also tampering with their browser`）
  - 主持人 VPN 与地区封锁亲历（原文锚点：`I live in Singapore, but I like to access sites for things in the UK`；`I'm using Mullvad`）
  - 主用例图谱（原文锚点：`account takeover, free trial abuse, new account fraud, account sharing`；`payment fraud as well, charge back, dispute`；`ban evasion to paywall enforcement`；`what has this device done before`）
  - SMS pumping 案例（原文锚点：`somebody was solving the problem of SMS pumping`；`You end up paying for that text message to be sent`；`spamming these one-time passcodes over and over and over again`；`besides just an IP rate limit`）
  - AI token 欺诈=老滥用新标签（原文锚点：`AI token fraud is really just the same types of abuse with a new label`；`racking up a bunch of fake accounts to try and use it all up`；`using stolen credit cards to buy`；`using account takeover tactics to hack into somebody else's account`）
  - Firefox/Tor 漏洞的定位：私密浏览与 IndexedDB（原文锚点：`it was specifically within the Firefox private browsing`；`which also applied to Tor browser as well`；`The idea here was around the index DB`；`Index DB is another way to store data`）
  - 漏洞机制：返回顺序的随机性（原文锚点：`the actual order that they get returned back to me is not the same order`；`based on the UUIDs and the way that the hashing worked`）
  - 跨站可读与进程级重置（原文锚点：`that ordering of the databases can be accessed by other sites`；`same randomized order to track you from site to site`；`only if you fully close, like fully quit the process`）
  - Fingerprint 自身的访客 ID 隔离原则（原文锚点：`At fingerprint, we do not like being tracked`；`If customer A identifies my phone`；`Customer B is getting a completely different visitor ID`）
  - 披露准则：不助跨站追踪、信号强度与安全问题时必披露（原文锚点：`to track people across the Internet`；`especially in something like Tor browser, or Firefox private mode`；`how this person has access to your site and what they're doing in your business`；`not try and build profiles on people, or track them across the entire Internet`；`the strength of the signal goes into it as well`；`Whenever we feel like it's actually a security issue`；`do we believe in the privacy aspect`）
  - 音频指纹与视觉 canvas 的熵来源及稳定性设计（原文锚点：`audio canvassing, or audio fingerprinting`；`You don't hear the noise`；`The way your computer draws a certain shape`；`very unique based on your operating system, your hardware, your graphics card`；`if you change one thing, if you upgrade your browser, that shouldn't cause the whole Fingerprint to disintegrate`）
  - AI agent 识别的分层方法（原文锚点：`browser automation-based agent`；`We layer a bunch of different techniques together`；`things like web bot auth, which allow these agents to cryptographically sign`）
  - "不报名字"的难点与 muse 例子（原文锚点：`at least as of today, as far as I know`；`Meta's muse does not necessarily announce itself`；`how often, how fast is it working`；`we mostly mean it didn't announce itself`；`This is Claude, or it's a Perplexity browser`）
  - agent 评估预告与"狂野西部"现状（原文锚点：`coming out in the next month, actually, a assessment`；`Can they make a purchase? Can they make a booking?`；`But how do we know it's you`；`is it a bot or is it not a bot`；`Now it is like the wild, wild west`）
  - web bot auth 机制：IETF 草案、签名、注册表与二层核验（原文锚点：`It's a draft on IETF`；`it's still an emerging standard`；`cryptographically sign your headers that your bot is sending`；`there's a registry that we can compare to`；`We verify that these specific ones are ChatGPT, Claude, etc`）
  - web bot auth 免费测试页（原文锚点：`It's a free tool anyone can use`；`if you've configured your cryptographic signatures appropriately`）
  - 不走浏览器的 bot 与 automation intelligence API（原文锚点：`Many of these bots are not using browsers to fetch information`；`maybe they're not even loading JavaScript`；`We also have a automation intelligence API coming out as well`；`You can add it to your middleware`）
  - 后台化体验与 CAPTCHA 失效（原文锚点：`All of this is happening in the background`；`There's no drag the puzzle piece, or click on the fire hydrants`；`The bot stuff helps you protect your pages, your logins, your forms`；`bots can solve many of these captchas anyways`；`Who are we really stopping with these`；`never have to do one of these puzzles ever again`）
  - MCP server 与数据分析（原文锚点：`launched an MCP implementation back in March`；`The MCP server, that was the first piece we did`；`It does include an onboarding skill to get you started`；`It helps you dig into that with natural language`；`without having to pull up a SQL`）
  - CLI、skills 与 AI 安装页（原文锚点：`we've launched our CLI`；`You can get off and running in a few minutes`；`this week launched a new page for AI installation`；`if you're a vibe coder, or if you're a senior engineer`）
  - demo 与 playground（原文锚点：`demo.fingerprint.com`；`This is where you can see all those different smart signals`；`the raw JSON output that we would give you`）
  - 报告：device intelligence report 与金融服务 AI 流量调查（原文锚点：`financial services AI traffic survey`；`It breaks it down piece by piece`；`The VPN, we saw it's one in five`；`app cloning on a mobile device, much smaller take`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语。
- 节目页面标注本期由 Fingerprint 赞助（"Full Disclosure: This episode is sponsored by Fingerprint"）；嘉宾 Keshia Rose 任职于 Fingerprint 开发者关系，文中关于产品能力、数字、上线计划与效果的表述均为供方口径，未经独立验证。
- 无法独立验证的数字与细节（去年超 230 亿次识别、VPN 约 17%——受访者自言"别引用我"、公司化年份"2019 或可能 2020"、Meta muse 不自报身份、MCP 三月上线为主持人转述、"下个月"的 agent 评估与 automation intelligence API 属预告等）仅作为节目中的观点或案例呈现。
- 本期主持人为 Gregor Vand，嘉宾为 Keshia Rose（Fingerprint 开发者关系）。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
