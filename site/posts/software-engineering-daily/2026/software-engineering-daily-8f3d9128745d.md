---
item_id: software-engineering-daily-8f3d9128745d
title: '即时利用时代的软件安全：零日时钟加速、AI 攻防与防御者的上下文优势'
date: '2026-10-17'
published_at: '2026-10-06'
transcribed_at: '2026-10-17'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/security-in-the-age-of-instant-exploits/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1959-Wiz-2026.txt'
summary: 'Wiz AI 与威胁研究副总裁 Alon Schindel 对话主持人 Gregor Vand：AI 把漏洞从披露到利用的时间从一年压到数小时，扫描暴露密钥、挖掘复杂缺陷也变得人人可为；但掌握环境上下文的防御者仍占先机——零日时钟、红绿代理、开源维护者困境与"漏洞末日"的另一种结局。'
tags: [安全, AI Agent, 企业 AI]
---

# 即时利用时代的软件安全：零日时钟加速、AI 攻防与防御者的上下文优势

> 节目：[Software Engineering Daily](/podcasts/software-engineering-daily/)
>
> 节目发布：2026-10-06 · 逐字稿获取：2026-10-17 · 笔记整理：2026-10-17
>
> 全文共 19492 字 · 阅读约 49 分钟
>
> 标签：[安全](/tags/%E5%AE%89%E5%85%A8/) [AI Agent](/tags/AI%20Agent/) [企业 AI](/tags/%E4%BC%81%E4%B8%9A%20AI/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/security-in-the-age-of-instant-exploits/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/08/SED1959-Wiz-2026.txt)

## 速读

Wiz AI 与威胁研究副总裁 Alon Schindel 对话主持人 Gregor Vand：AI 把漏洞从披露到利用的时间从一年压到数小时，扫描暴露密钥、挖掘复杂缺陷也变得人人可为；但掌握环境上下文的防御者仍占先机。

最值得带走的三点：一是"零日时钟"的加速——从漏洞被发现到被利用，2021 年约一年，2025 年一个月，2026 年已到一天（主持人在节目中更新为实际已到两小时），网站预测 2027 年逼近一小时；二是防御者的上下文优势——攻击者只能广撒网，防御者知道自己环境里什么最重要，且公开 CVE 中"确认在野被利用"的比例从 2021 年的 2.2% 降到 2026 年的 0.25%，同时 AI 找到的多数漏洞其实无法被利用；三是自动化修复的现实边界——从红代理（攻击模拟）到绿代理（响应修复）的闭环"没人有完美方案"，补丁后的自动测试仍是缺口，而开源维护者正被 AI 生成的重复报告压垮。

## 主题正文

### 嘉宾与起点：一条幼儿园友谊牵出的路

按节目开场介绍，Alon Schindel 是 Wiz 的 AI 与威胁研究副总裁，Wiz 是一个云安全平台，于 2026 年被 Google 收购——此处按节目口径呈现。主持人 Gregor Vand 是 CTO 与创始人，工作横跨通信、安全与 AI，常驻新加坡，最新创业项目是 Wyntk.ai。（原文锚点：`acquired by Google in 2026`；`His latest venture, Wyntk.ai`）

Alon 自述小学三四年级起做网站，从此对"我的网站怎么被黑"着迷，此后二十多年只要能选就选安全方向。真正把他带进 Wiz 的是一位幼儿园就认识的发小——Wiz 的第一批工程师之一；发小入职几个月后公司要扩张，一条消息把他叫来聊"新机会"，那已经是约五年半前。他提到 Wiz 如今成立六年，一切变化太快，感觉像去年才刚开始。（原文锚点：`one of the first engineers at Wiz, who is one of my childhood friends`；`around five and a half years ago`；`Wiz now is six`）

这六年他概括为"几乎什么都见过了"：从 2021 年的 Log4J——他称之为见过的最大漏洞之一——到如今 Shai-Hulud 等供应链蠕虫浪潮；而 AI 对安全的冲击让他觉得一切像重新开始。他给出本期讨论的框架：AI 与安全有两个视角——用 AI 做安全，以及保护 AI 自身、应对 AI 打开的新攻击面；他把当下的变化形容为"新的物理学"。（原文锚点：`since Log4J in 2021`；`Shai-Hulud and other similar data worms`；`two different perspectives, how you can use AI for security and also securing AI`；`like having new rules of physics today`）

主持人顺带提到，这是 Wiz 嘉宾第二次上节目，上一次他对话的是 Rami McCarthy，约在两年前。（原文锚点：`I spoke to one of your colleagues, Rami McCarthy`）

### 零日时钟：从一年、一个月、一天到两小时

节目开场把现状概括为：AI 模型如今读到漏洞报告就能几乎立刻生成可用的 exploit，并能以任何人类团队都无法匹敌的规模扫描整个互联网上暴露的密钥。（原文锚点：`generate a working exploit almost instantly`；`scan the entire Internet for exposed secrets at a scale no human team could match`）

主持人先给出一组开场数据：Firefox 团队曾说 2026 年 4 月单月修复的安全 bug 比之前一整年还多，归因于当时发布的 Anthropic 模型 Mythos；他同时补充了条件——该模型一度下线，按他们的理解在录制前约六天重新上线，播出时是否仍在线则无法保证。（原文锚点：`fixed more security bugs in April 2026 than in the entire previous year`；`come back online about six days before we recorded`）

Alon 的回应是：Mythos 只是"一记响亮的警钟"，趋势更早——Wiz 去年 12 月就办过 AI 漏洞挖掘竞赛，前排队伍大多已在用 AI 找漏洞，比 Mythos 发布早约四到五个月；他点名的 Opus 4.6、Gemini、GPT-5.5 等模型同样展现找漏洞的能力。（原文锚点：`a loud wake up call for the industry`；`we launched AI vulnerability competition`；`most of the teams that finished in the highest positions in this competition use AI`；`around four months, five months before Mythos was announced`；`they all show great capabilities in finding vulnerabilities`）

主持人推荐了 zerodayclock.com 的下行曲线：从漏洞被发现到被利用的时间，2021 年约一年，2025 年已降到一个月，2026 年到达一天；网站预测 2027 年逼近一小时、甚至一分钟。他在节目尾声再次查看后更新：实际已经降到两小时。（原文锚点：`it took one year to go from something has been discovered to the time it was breached`；`it's already dropped to one month`；`we also reached in 2026 one day`；`They at least are projecting one hour by 2027`；`we are actually down to two hours on the time to exploit`）

Alon 从自己的漏洞响应工作印证这一趋势：过去一年他们"背靠背"地响应新漏洞，因为 exploit 出现得越来越快。他回忆加入 Wiz 早期的一个 Apache HTTP 服务器严重漏洞，从披露到出现 exploit 大约两三天；而最近的 MongoDB 漏洞，公开报告发给别人（他现场以 Claude 举例）就能拿回完整 exploit——这是他对行业状态的描述，不是操作指引。（原文锚点：`a critical Apache HTTP server vulnerability`；`it took around two or three days until we saw the exploit`；`the vulnerability in MongoDB`；`you could have just send it to Claude and get the full exploit back`）

### 黑客民主化与 AI 规模的暴露面扫描

Alon 说当下讨论的现实是"黑客民主化"：找漏洞、尤其是 Web 攻击的门槛越来越低。他自嘲说，如果自己十岁时就有哪怕不是 Mythos 的模型，也能拿去扫描互联网上暴露的数据，或那些一触发就返回密钥的 lambda 函数。攻击工作第一次变得可扩展：过去 nation state 级别的能力需要时间、精力和技能，如今一个人在家就能跑大规模扫描。（原文锚点：`hacking is democratized`；`The barrier to get into cybersecurity is becoming lower and lower`；`lambda functions that whenever you trigger them, they just get you secrets back`；`even a single person just from home can run these large operations`）

防御一侧用的是同样的能力。Wiz 早期的 AI 落地是"红代理"——一个 AI 自动化攻击者：先从内部扫描环境，识别敏感数据与组织最重要的"皇冠上的珠宝"，按敏感度和关键性排定优先级，再像外部攻击者一样扫描网页、但带着内部提示；它分析 HTML 与 JavaScript 文件，寻找暴露。这个功能以极快速度铺到数千客户，是他见过采用最快的功能之一。他说 Wiz 由此在外部发现了数千个漏洞与严重暴露——如果不是他们先找到，就会是攻击者找到：网页里偶尔嵌着 GitHub PAT 之类的令牌，任何人都可读取并登入组织系统，进而窃取数据，甚至借令牌向该公司产出的软件包注入恶意脚本、感染下游客户。（原文锚点：`the AI automated attacker`；`crown jewels of your organization`；`prioritize the resources according to their sensitivity`；`We scan the page from the outside like an attacker`；`We scan it, we analyze the HTML file, the JavaScript file`；`enable it to thousands of customers`；`Probably one of the features that we saw the fastest adoption speed for`；`We actually found thousands of vulnerabilities and critical exposures just out there`；`GitHub PAT tokens, other tokens that are just accidentally embedded in these web pages`；`infect the downstream customers`）

### 防御者的牌：上下文优势与回落的利用比例

Alon 的乐观论证核心是上下文：上下文是 AI 的关键，模型没有上下文就工作不了，上下文越好结果越好。防御者知道自己环境里有什么、什么重要；攻击者可以暴力猜测、广撒网，但在真正进入之前不知道什么才是重要的。他明确摆出前提——假设攻防双方拿到同样的模型，防御者拥有更好的上下文，因此他认为防御方能守住优势。他也承认这是立场而非定论：长期未必更糟，蓝军一侧同样有大机会。（原文锚点：`Context is the key for AI`；`the models, they can't work without context`；`they don't know what's really important, until they actually get in`；`the defenders have better context`；`It doesn't necessarily mean that things will be worse in the long term`；`on the blue side, there are also great opportunities there`）

主持人补充了一个支持性数据：同一来源显示，公开 CVE 中确认在野被利用的比例（相对 CVE 总量）实际在下降——2026 年为 0.25%，低于 2021 年的 2.2%。他认为这印证了 Alon 的正面论点。（原文锚点：`percentage of all published CVEs that are confirmed exploited in the wild`；`the exploit rate is down to 0.25%`；`that's down from 2.2% in 2021`）

Alon 同时给出重要限定：发现漏洞不等于能利用它——他们用 AI 找到的多数漏洞其实无法被利用；更弱的模型做不到从发现到可用 exploit 的跨越，这是他预期接下来模型会改进的方向。（原文锚点：`finding a vulnerability doesn't necessarily mean that it's easy to exploit it`；`most of the vulnerabilities that we find with AI, we can't really exploit`）

### 负责任披露的新难题：开源维护者被压垮

Alon 说 Wiz 把遵守各平台披露规则当作重要原则：系统标记为极危的发现，会像其他报告一样通过安全邮箱上报，或直接联系安全团队。但规模带来了新问题：开源项目和小维护者每周可能收到几十、上百份来自不同公司的报告。他举了录制前一周的例子：一个开源项目披露漏洞时，记得有 15 家公司或研究者重复上报同一问题——因为所有人都在用 AI 扫开源项目，分诊（triage）成了难题。还有维护者公开表示不回应 AI 生成的报告（因为能看出 AI 的痕迹）；也有维护者在业余时间凭爱好做贡献，却因响应不够快而被羞辱，而他们并没有资源。（原文锚点：`it's an important principle to comply with the different disclosure rules`；`We also try to reach out either through the security email`；`dozens, hundreds of reports from different companies every week`；`15 different companies, or researchers who reported this issue`；`everyone scans these open-source projects with AI, but it creates a problem with triage`；`they won't respond to reports that were AI generated reports`；`with their hobby on their free time, they do something great for everyone's good`；`sometimes even shamed from not responding fast enough`）

他给出的行业方向是：前沿实验室应当参与扫描那些支撑整个互联网的关键开源项目，赶在攻击者之前找出漏洞——他说 Google、OpenAI、Anthropic 都已有投入，而且这件事必须在这些能力扩散到红队一侧之前做。（原文锚点：`scan these critical open-source projects that are the backbone of everything`；`both Google, OpenAI, Anthropic, they all invest efforts there`；`before these capabilities propagate to the red site`）

### 从红代理到绿代理：自动修复闭环的真实边界

主持人把话题引向连续自动修复——他形容这曾是"圣杯"：无需人参与，漏洞一披露就有代理去处理。Alon 的回答坦率：这是"发现—分析—自动修复"的循环，他不认为谁有完美方案，尤其很多系统里还有多年积累的遗留代码，没人该因为"没做到完美"而愧疚。（原文锚点：`this needs to start involving a lot more continuous automated remediation`；`it's kind of a circle where you find an exposure and you need to analyze it and remediate it automatically`；`I don't think that anyone has the perfect solution`；`they have their legacy code`）

Wiz 的方法论分层进行。第一层是宽而浅的连续扫描（红代理式的攻击面扫描），且攻击面不止 Web 资产——还包括 GitHub 仓库、CI/CD 流水线等一切可能被攻破的资源，用 AI 连续扫描、赶在攻击者之前找到暴露。第二层是理解风险，首选是减少暴露：很多场景里问题不只是漏洞本身，而是存在本不该暴露的资源。第三层才是修复，绿代理从这里开始：先找根因。他指出，把一个暴露关联到组织内的所有者、关联到来源代码文件向来困难；而 AI 若同时能访问暴露数据与代码仓库，就能做他们所称的"云到代码"（cloud to code）定位。（原文锚点：`very wider and shallow scans`；`you also have to scan your GitHub repos`；`scan it continuously with AI, try to find these exposures before the attackers do`；`how do you reduce exposure`；`the problem is a resource that shouldn't have been exposed`；`the green agent, which is on the response side`；`finding the root cause`；`connecting it to the owner in your organization`；`what we call the cloud to code`）

绿代理随后规划修复步骤，有时给出多个备选方案；还可以给代理写入指令与偏好——总是优先打补丁，或优先通过修改 terraform 文件来减少暴露、聚焦代码之外的部分。他强调 AI 不只擅长攻击，在构建与理解软件上同样出色。但闭环还差一环：补丁之后的自动测试——如何自动测试新代码、确保变更不影响系统其他部分，是下一步；自动打补丁本身也仍是行业在摸索的问题。更根本的解法有时是调整架构，例如采用安全镜像，帮组织以更好的架构更快闭合这个端到端循环。（原文锚点：`plans the remediation, or also sometimes offers different remediation plans`；`always prioritize patching`；`prioritize reducing exposure by changing to your terraform files`；`AI is not only good in hacking`；`how do you automatically test the new code`；`how you can do automated patching`；`using, for example, secure images is one solution`；`close this end-to-end loop faster with better architecture`）

主持人点出开发者视角的代价：加固镜像或加固容器意味着接受工具链上的约束，或对容器做特殊改动——想让整条供应链更安全的团队需要权衡是否接受。（原文锚点：`hardened images, or hardened containers`；`accept some constraints on your tool chain`）

### 供应链与 SBOM：流行的包可能是"定时炸弹"

Alon 说 Wiz 也在扫描公开仓库、CI/CD 流水线与 GitHub Actions，并与维护者负责任地协作；确实有不少项目存在暴露。他的判断是：一个被众多组织使用、存在暴露、又缺乏安全卫生的流行项目，就是定时炸弹。减少暴露还包括审核开源依赖、使用更安全的 SBOM（官方逐字稿写作 "S bomb"，按语义理解）——即"左移"、从源头做更安全的选择；他承认这不容易，没有哪个开发者想停用流行库。（原文锚点：`We also find, we try to scan these public repos, try to scan CI/CD pipelines and GitHub actions`；`some libraries and some packages are not maintained well`；`You can see this package as a ticking bomb`；`vetting your open-source code`；`using more secure S bomb`）

AI 也在加重这个盲区：用编码代理写代码时，依赖常由代理添加，你甚至不知道代码里有什么。他希望编码代理未来会把最安全的架构与更安全的 SBOM 作为内置优先级。（原文锚点：`you don't even know what's inside it`；`that were added by the coding agent`；`I hope that coding agents will also understand`；`more secure S bomb for your environment`）

### SAST 之后：AI 能找什么漏洞，以及多代理工程的难题

AI 代码分析是本期技术上最密的一段。SAST 不是新名词，产品已存在多年，目标是在应用层找代码漏洞，经典例子是 SQL 注入；过去它难在理解语言——依赖语言处理、构建控制流图（CFG），被他称为真正的学术难题。现在的变化是 LLM 本就擅长文本，而代码也是带结构与规则的文本；他观察到自去年 12 月起，模型在理解代码上的巨大跃升。主持人列出 AI 能找到而传统工具难找的类别：复杂逻辑缺陷、IDOR（不安全的直接对象引用）、链式漏洞与不安全的应用流程。（原文锚点：`These products have been around for years`；`a SQL injection`；`building a graph flow, CFG`；`code is also text with structure`；`since December, a great leap in capabilities of AI models in understanding code well`；`complex logic flaws`；`insecure direct object reference`；`The reason that we have a great opportunity now is that AI can actually understand the code`）

Alon 区分两类漏洞：内存类漏洞与代码/应用层漏洞，Wiz 内部也分成两条线——一个团队做聚焦内存漏洞的深度漏洞引擎，另一个代理是 AI SAST、将进入产品。工程挑战包括：客户环境有数百个仓库，要跨仓库找到所有引用、凑齐完整上下文。Wiz 的做法是把人类手工找漏洞的流程建模为多代理协作——先收集引用数据，然后真的去尝试攻击，再测试、验证，甚至引入评审（judge）；不同模型各有所长（他提到 Claude、Gemini、GPT），一个卡住就调用另一个，就像不同研究员擅长不同领域。（原文锚点：`memory vulnerabilities`；`very deep vulnerability engine that focuses on the memory vulnerabilities`；`Another agent that is more the AI SAST`；`organizations with hundreds of different repos`；`find all the references from these different repositories`；`separating different tasks to different agents`；`then really try to hack it, then test it, validate it, even a judge`；`Claude has different advantages, Gemini has different advantages, GPT has different advantages`；`When we see that a model is maybe stuck`）

另一个关键工程问题是误报与分级：LLM 发现什么都说极危，他认为这是训练问题，必须压误报、评估真实严重度。他对 Mythos 的定位也很克制：它确实是参数量大一个数量级的超大模型，但重要的不只是模型，还有 harness——用好的 harness 组织非 Mythos 级的前沿模型协作，可以得到与 Mythos 几乎相似的结果。（原文锚点：`they usually flag it as super critical`；`that's part of a training issue`；`understand the real criticality of the issue`；`it's not only about the model, it's also the harness`；`almost similar results to what you see with Mythos`）

### 概率性与可复现性：诚实的边界

主持人追问可复现性：AI 发现的漏洞能说明是什么、影响可能是什么，但要让别人复现就更难。Alon 的回答坦率：LLM 基于概率过程，当然存在随机因素，目标是尽可能确定性，但"诚实的答案是：我们还没做到"。作为厂商，可能给出不同答案的东西不好卖；不过他观察到安全行业对随机性的容忍度在上升——人们正在习惯给你不同答案的 AI 系统。（原文锚点：`there is of course some random factor there`；`they are based on probabilistic processes`；`make them as deterministic as possible`；`the honest answer is that we're not there yet`；`hard to sell something that might give different answers`；`There is maybe slightly more tolerance than what we used to see before in cybersecurity`；`people are getting used to AI systems that give you different answers`）

Wiz 引擎的对策是把同一问题多次复现验证；而内存类漏洞本身就是概率性的——平均十次运行才成功一次，两个概率机制叠加让验证更难；他说前沿实验室也在投入让模型更确定。主持人总结这份容忍的"解锁"逻辑：接受不那么确定，换来的是如果必须完全确定性就永远不会被发现的问题——其中一些确实是 SAST 多年没抓到的严重缺陷。（原文锚点：`reproduce the issue multiple times`；`just one out of 10 runs will succeed`；`making the models more deterministic`；`would just never have been found if this had to be a completely deterministic system`；`crazily problematic things that SAST haven't picked up for many years`）

### 展望：漏洞洪峰之后，曲线会向下吗

Alon 的短期预期是：被发现的漏洞会越来越多，但大多数不可利用；中期会到达一个拐点——大多数开源软件都被扫描过，只要模型侧不再出现另一次巨大跃升，大多数问题就会被直接修掉。他给安全团队的务实提醒是：接下来要打很多补丁、处理很多 CVE，工作是辛苦的；但架构层面的改变会降低被利用的可能性，之后漏洞数量会开始下降。有人把这称为"漏洞末日"（vulnerability apocalypse），他的看法是：如果社区现在就协力在攻击者之前找到并修复这些问题，一两年后回头看能越过这道坎，最终建成一个攻击者更快、防御者也更快（但更快的是防御者）的更安全世界。（原文锚点：`more and more vulnerabilities that are being discovered, but most of them won't be exploitable`；`most of the open-source software will be scanned`；`As long as we don't see another huge leap of advancement on the LLM side`；`most of the issues will be just fixed`；`There will be many CVEs that will need to patch`；`reduce the likelihood of exploitation`；`some people call the vulnerability apocalypse`；`if we do great work now as a community`；`if you're looking a year or two from now, after we are past that`；`we can make our life easier`；`fast attackers, but also faster defenders`）

想跟进的读者可到 wiz.io/blog（Alon 预告即将发布一篇关于用 AI 找漏洞的博客），或在 LinkedIn、X 上搜索他的名字。（原文锚点：`wiz.io/blog`）

## 来源与定位

- 原始节目：[Security in the Age of Instant Exploits](https://softwareengineeringdaily.com/podcasts/security-in-the-age-of-instant-exploits/)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 节目开场对主题与嘉宾的介绍（原文锚点：`acquired by Google in 2026`；`generate a working exploit almost instantly`；`scan the entire Internet for exposed secrets at a scale no human team could match`）
  - 主持人 Gregor Vand 背景（原文锚点：`His latest venture, Wyntk.ai`）
  - 嘉宾起点与加入 Wiz 的机缘（原文锚点：`one of the first engineers at Wiz, who is one of my childhood friends`；`around five and a half years ago`）
  - Wiz 六年与 Log4J、Shai-Hulud（原文锚点：`Wiz now is six`；`since Log4J in 2021`；`Shai-Hulud and other similar data worms`）
  - 此前一期 Wiz 嘉宾（原文锚点：`I spoke to one of your colleagues, Rami McCarthy`）
  - 两个视角与"新物理学"（原文锚点：`two different perspectives, how you can use AI for security and also securing AI`；`like having new rules of physics today`）
  - Firefox/Mythos 开场数据与下线说明（原文锚点：`fixed more security bugs in April 2026 than in the entire previous year`；`come back online about six days before we recorded`）
  - Wiz AI 漏洞竞赛与各家模型能力（原文锚点：`a loud wake up call for the industry`；`we launched AI vulnerability competition`；`most of the teams that finished in the highest positions in this competition use AI`；`around four months, five months before Mythos was announced`；`they all show great capabilities in finding vulnerabilities`）
  - 零日时钟各时间点与两小时更新（原文锚点：`it took one year to go from something has been discovered to the time it was breached`；`it's already dropped to one month`；`we also reached in 2026 one day`；`They at least are projecting one hour by 2027`；`we are actually down to two hours on the time to exploit`）
  - Apache 与 MongoDB 的披露到利用案例（原文锚点：`a critical Apache HTTP server vulnerability`；`it took around two or three days until we saw the exploit`；`the vulnerability in MongoDB`；`you could have just send it to Claude and get the full exploit back`）
  - 黑客民主化（原文锚点：`hacking is democratized`；`The barrier to get into cybersecurity is becoming lower and lower`；`lambda functions that whenever you trigger them, they just get you secrets back`；`even a single person just from home can run these large operations`）
  - 红代理与 AI 规模暴露扫描（原文锚点：`the AI automated attacker`；`crown jewels of your organization`；`prioritize the resources according to their sensitivity`；`We scan the page from the outside like an attacker`；`We scan it, we analyze the HTML file, the JavaScript file`；`enable it to thousands of customers`；`Probably one of the features that we saw the fastest adoption speed for`；`We actually found thousands of vulnerabilities and critical exposures just out there`；`GitHub PAT tokens, other tokens that are just accidentally embedded in these web pages`；`infect the downstream customers`）
  - 上下文优势论证（原文锚点：`Context is the key for AI`；`the models, they can't work without context`；`they don't know what's really important, until they actually get in`；`the defenders have better context`；`It doesn't necessarily mean that things will be worse in the long term`；`on the blue side, there are also great opportunities there`）
  - 利用比例回落的数据（原文锚点：`percentage of all published CVEs that are confirmed exploited in the wild`；`the exploit rate is down to 0.25%`；`that's down from 2.2% in 2021`）
  - 发现不等于可利用（原文锚点：`finding a vulnerability doesn't necessarily mean that it's easy to exploit it`；`most of the vulnerabilities that we find with AI, we can't really exploit`）
  - 披露规则与开源分诊难题（原文锚点：`it's an important principle to comply with the different disclosure rules`；`We also try to reach out either through the security email`；`dozens, hundreds of reports from different companies every week`；`15 different companies, or researchers who reported this issue`；`everyone scans these open-source projects with AI, but it creates a problem with triage`；`they won't respond to reports that were AI generated reports`；`with their hobby on their free time, they do something great for everyone's good`；`sometimes even shamed from not responding fast enough`）
  - 前沿实验室扫描关键开源（原文锚点：`scan these critical open-source projects that are the backbone of everything`；`both Google, OpenAI, Anthropic, they all invest efforts there`；`before these capabilities propagate to the red site`）
  - 自动修复的圣杯与"没有完美方案"（原文锚点：`this needs to start involving a lot more continuous automated remediation`；`it's kind of a circle where you find an exposure and you need to analyze it and remediate it automatically`；`I don't think that anyone has the perfect solution`；`they have their legacy code`）
  - 连续扫描与减少暴露（原文锚点：`very wider and shallow scans`；`you also have to scan your GitHub repos`；`scan it continuously with AI, try to find these exposures before the attackers do`；`how do you reduce exposure`；`the problem is a resource that shouldn't have been exposed`）
  - 绿代理、根因与云到代码（原文锚点：`the green agent, which is on the response side`；`finding the root cause`；`connecting it to the owner in your organization`；`what we call the cloud to code`）
  - 修复方案、偏好与自动测试缺口（原文锚点：`plans the remediation, or also sometimes offers different remediation plans`；`always prioritize patching`；`prioritize reducing exposure by changing to your terraform files`；`AI is not only good in hacking`；`how do you automatically test the new code`；`how you can do automated patching`；`using, for example, secure images is one solution`；`close this end-to-end loop faster with better architecture`）
  - 加固镜像的代价（原文锚点：`hardened images, or hardened containers`；`accept some constraints on your tool chain`）
  - 供应链风险与 SBOM（原文锚点：`We also find, we try to scan these public repos, try to scan CI/CD pipelines and GitHub actions`；`some libraries and some packages are not maintained well`；`You can see this package as a ticking bomb`；`vetting your open-source code`；`using more secure S bomb`）
  - 编码代理带来的依赖盲区（原文锚点：`you don't even know what's inside it`；`that were added by the coding agent`；`I hope that coding agents will also understand`；`more secure S bomb for your environment`）
  - SAST 的历史与新能力类别（原文锚点：`These products have been around for years`；`a SQL injection`；`building a graph flow, CFG`；`code is also text with structure`；`since December, a great leap in capabilities of AI models in understanding code well`；`complex logic flaws`；`insecure direct object reference`；`The reason that we have a great opportunity now is that AI can actually understand the code`）
  - 内存漏洞引擎与 AI SAST 双线（原文锚点：`memory vulnerabilities`；`very deep vulnerability engine that focuses on the memory vulnerabilities`；`Another agent that is more the AI SAST`）
  - 多代理与多模型工程（原文锚点：`organizations with hundreds of different repos`；`find all the references from these different repositories`；`separating different tasks to different agents`；`then really try to hack it, then test it, validate it, even a judge`；`Claude has different advantages, Gemini has different advantages, GPT has different advantages`；`When we see that a model is maybe stuck`）
  - 误报、分级与 harness（原文锚点：`they usually flag it as super critical`；`that's part of a training issue`；`understand the real criticality of the issue`；`it's not only about the model, it's also the harness`；`almost similar results to what you see with Mythos`）
  - 概率性与确定性的现状（原文锚点：`there is of course some random factor there`；`they are based on probabilistic processes`；`make them as deterministic as possible`；`the honest answer is that we're not there yet`；`hard to sell something that might give different answers`；`There is maybe slightly more tolerance than what we used to see before in cybersecurity`；`people are getting used to AI systems that give you different answers`）
  - 多次复现与内存漏洞的概率性（原文锚点：`reproduce the issue multiple times`；`just one out of 10 runs will succeed`；`making the models more deterministic`）
  - 容忍度换发现面的"解锁"（原文锚点：`would just never have been found if this had to be a completely deterministic system`；`crazily problematic things that SAST haven't picked up for many years`）
  - 短期洪峰与拐点条件（原文锚点：`more and more vulnerabilities that are being discovered, but most of them won't be exploitable`；`most of the open-source software will be scanned`；`As long as we don't see another huge leap of advancement on the LLM side`；`most of the issues will be just fixed`；`There will be many CVEs that will need to patch`；`reduce the likelihood of exploitation`）
  - "漏洞末日"与长期图景（原文锚点：`some people call the vulnerability apocalypse`；`if we do great work now as a community`；`if you're looking a year or two from now, after we are past that`；`we can make our life easier`；`fast attackers, but also faster defenders`）
  - 跟进入口（原文锚点：`wiz.io/blog`）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 原节目未提供可靠时间戳，全部定位使用可搜索原文短语；归档逐字稿中的行内时间标记按无时间戳处理，正文不引用推算时间。
- 无法独立验证的数字与断言仅作为节目中的观点或案例呈现，包括：zerodayclock.com 的各时间点与预测、公开 CVE 在野利用率 2.2% 到 0.25% 的下降、Firefox 2026 年 4 月修复量对比、Mythos/Fable 模型及"下线后约六天恢复上线"的说明、Wiz AI 漏洞竞赛名次与"提前四五个月"的时间口径、Apache 漏洞"两三天出现 exploit"的回忆、MongoDB 漏洞报告可让 Claude 返回完整 exploit 的举例、开源项目"15 家公司或研究者"重复上报、红代理"数千客户"的采用速度等，均为受访者或主持人口径。官方逐字稿中的 "S bomb"（应为 SBOM）、"red site"（应为 red side）等转写痕迹按原文保留为锚点，语义理解以上下文为准。本期嘉宾为 Alon Schindel，主持人为 Gregor Vand；开场介绍称 Wiz 为"2026 年被 Google 收购的云安全平台"，按节目口径呈现。本文不含可操作的攻击指引。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
