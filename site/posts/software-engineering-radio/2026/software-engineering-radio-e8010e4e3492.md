---
item_id: software-engineering-radio-e8010e4e3492
title: Polars 双人谈："为速度而来，为 API 而留"，以及一次把 15 万欧元算力账单砍到 3.5 千的迁移
date: '2026-09-17'
published_at: '2026-07-02'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/07/se-radio-727-jeroen-janssens-and-thijs-nieuwdorp-on-using-polars/'
source_name: 'Software Engineering Radio'
input_type: video_agent_kit_asr
summary: '《Python Polars 权威指南》两位作者 Jeroen Janssens 与 Polars 团队的 Thijs Nieuwdorp 对谈：表达式这一心智模型、eager/lazy 与查询优化器、join_asof 与滚动窗口，以及荷兰电网公司把 15 万欧元计算成本降到 3.5 千的逐步迁移案例。'
tags: [数据工程, Python, 性能]
---

# Polars 双人谈："为速度而来，为 API 而留"，以及一次把 15 万欧元算力账单砍到 3.5 千的迁移

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-07-02 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 5365 字 · 阅读约 14 分钟
>
> 标签：[数据工程](/tags/%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B/) [Python](/tags/Python/) [性能](/tags/%E6%80%A7%E8%83%BD/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/07/se-radio-727-jeroen-janssens-and-thijs-nieuwdorp-on-using-polars/)

## 速读

《Python Polars: The Definitive Guide》的两位作者——Posit 开发者关系负责人 Jeroen Janssens 与 Polars 公司开发者关系工程师 Thijs Nieuwdorp——做客 SE Radio,把 Polars 从 Richie Vink 的一个 Rust 副业项目讲到 1.0 之后的时代。社区那句话是本期最好的索引:"为速度而来,为 API 而留"。

最值得带走的三点:理解了"表达式是一棵描述如何构造一个或多个序列的操作树",就掌握了 Polars API 的八成;lazy 模式下谓词与投影下推配合列式存储,才是性能的真正来源;而那个荷兰电网案例证明了迁移方法论——从输入输出做黑盒等价、按性能关键部分逐块替换,能把 15 万欧元的计算成本砍到 3.5 千。

## 主题正文

### 起源:一个对 pandas join 不满的人学了 Rust

Polars 的诞生被 Jeroen 讲成一个个人故事:五年前,Richie Vink 为客户项目做两张表的 join,对 pandas 的速度不满意,于是自己动手用 Rust 实现——一开始比 pandas 还慢,但"Richie 就是 Richie",一路改进至今。如今大家来用 Polars 还是为了原始速度,留下来却是因为那套有表现力的 API。三人的缘分也在这段历史里:两位嘉宾与 Richie 曾同在 Xomnia(包括主持人后来也提到的这家荷兰咨询公司),那正是 Polars 的出生地,也是 Thijs 和 Jeroen 第一次把它写进客户生产代码的地方。如今 Polars 早已过 1.0,书也出了。（`00:01:24–00:03:34`）

概念铺垫很简洁:data frame 就像数据库里的一张表、电子表格里的一个 sheet——行列矩形结构,同列同类型;Polars 核心用 Rust 写,绑定到 Python、Node.js 与 R,其中 Python 绑定最完整、最流行。（`00:03:47–00:10:32`）

### 三句文档口号与列式存储

主持人从 Polars 文档里挑了三句话请嘉宾拆解。"fast, designed close to the machine, without external dependencies":性能关键路径——从 IO 到变换再回到 IO——全部握在自己手里,不假手第三方库,才能榨干整条管线。"Intuitive API"的定义也很工程化:开发者不读文档就能猜对怎么用——join、group by 这些领域术语都在,关键字参数行为符合预期,默认值对常见场景正确,"没有 footgun"。"Out-of-core"指的是 streaming 引擎:把数据切块处理、压低峰值内存,可以处理超过内存的数据集;sort 这类需要全量数据的操作,未来会支持把中间结果落盘(以运行时间为代价保证能跑完)。（`00:04:27–00:07:27`）

列式的直观解释来自 Thijs 的档案柜比喻:行式存储像每个抽屉装一笔销售的全部信息——查"谁买了什么"方便,但分析查询往往只要一两列,却不得不打开所有抽屉;列式把抽屉按字段排列,取"姓名+商品"只需开两个抽屉。Polars 建立在 Apache Arrow 之上,而 Arrow 同时是一份内存布局规范——同样实现它的库(pandas 也有 Arrow 后端)可以近乎零拷贝地互换数据。（`00:07:27–00:10:01`）

### 表达式:一棵描述"如何构造序列"的操作树

从 pandas 迁移最大的心智转变是:放下行索引(Polars 不用它做数据操作)、告别满屏方括号;从 SQL 来的人则会觉得自然——Polars 是声明式的,你只描述结果长什么样,优化器去决定执行方式。Jeroen 的类比是 R 的 ggplot2:声明"散点图,颜色按这一列",而不是写循环给每个分组上色。（`00:11:34–00:14:43`）

表达式是 Polars 的核心心智模型,重要到写书时原计划一章,最后写了三章、近 100 页;理解了表达式,"就掌握了 Polars API 的八成"。他们与 Richie 本人讨论后给出的定义是:表达式是一棵描述如何构造一个或多个序列(series,同类型值的序列,通常就是一列)的操作树。`pl.col("x")` 本身就是表达式——它什么都不做,只是描述;`pl.col("x") + pl.col("y")` 把两个小表达式组合成新表达式,树就这样长出来。因为选择列、新建列、过滤、排序、聚合全是表达式,写 Polars 代码处处都在构建它们,方法链让代码像菜谱一样从上往下读——Jeroen 的原话是"写 Polars 代码说实话相当快乐"。（`00:14:55–00:19:48`）

### joins、concat 与 pivot/unpivot:按值组合还是按形状组合

Thijs 用"月度最佳员工"的例子讲 join:销售表里只有 employee ID,要 enriched 上员工姓名,就拿 ID 与员工表 join——left join 保留左侧全部行、匹配不上的填 null;inner join 则两边都匹配才保留;还有 anti join、cross join 等"另一罐虫子"。concat 解决的是另一类问题:January 与 February 两张同 schema 的表拼成 Q1——纵向拼接,Polars 会做 schema 检查,新出现的列可以选择报错、填 null 或补齐。pivot/unpivot 则关乎 tidy data 的形状(主持人补了一句:这来自 2014 年《Journal of Statistical Software》的 Tidy Data 论文):成绩表的"数学、英语、历史"各占一列是宽格式,学生一多测试就得多加列,此时 unpivot 成"学生-课程-分数"三列长格式;pivot 再翻转回去。两位嘉宾当场承认总要查文档才记得哪个是哪个,还笑称 R 的 tidyverse 直接叫 pivot_longer/pivot_wider 更省脑子,Thijs 说他工位就挨着 Richie,可以试试去"拱"个改名。（`00:24:25–00:30:03`）

### eager/lazy、时间序列与类别类型:性能从哪来

lazy 模式不立刻执行,而是先构建逻辑计划(整张蓝图),再由查询优化器找最快路径——两个关键技巧是谓词下推(把过滤尽量靠近数据源)与投影下推(只读真正需要的列),后者正是列式存储的主场。eager 模式是默认,适合探索性分析;切到 lazy 只需把 read_csv 换成 scan_csv,而 Parquet 因为同为列式,比 CSV 更适合 lazy 读取;lazyframe 要 collect 或 sink 才物化。格式支持面很广:CSV、JSON、Excel、数据库、Parquet、Apache Iceberg、PyArrow datasets,数据变大时 Parquet 的压缩尤其值回票价。（`00:30:33–00:36:10`）

时间序列是 Polars 的强项(用户多来自金融):date/datetime/time/duration 类型齐备,join_asof 解决"不完全匹配"——卖出的时间戳对不上最近的行情 tick 时,向前搜索最近的一个价格配对;group_by_dynamic 按时间窗分组而非按 ID;再配上重采样、上采样加填充,以及滚动窗口——Thijs 用自家阳台温度传感器举例:人走过遮住传感器造成的骤降,用过去一小时的滚动平均抹平。类别类型则是空间与速度的双赢:T 恖尺寸只有五档,与其为 10 万行存变长字符串(各种标记长度起止的簿记开销),不如存"五个字符串 + 一个 u8 整数映射"。（`00:35:56–00:40:43`）

UDF 的优先级阶梯要记牢:先用内建表达式(Rust 优化过的金标准);不够再写插件(Rust+Python,保留原生性能——他们跟着 Marco Gorelli 的教程做过地理插件,算 haversine 距离、判断点是否在多边形内,搭起来费劲但值得进生产);Python UDF 是最后手段——慢得多,还会破坏 Polars 赖以成名的并行执行。（`00:40:43–00:43:22`）

### GPU、基准测试与那个 98% 的案例

基准测试是"非常微妙的艺术",对具体用例测才有意义;核心指标是峰值内存与总运行时间,云上还要看 CPU 利用率与网络带宽来做实例 right-sizing——Thijs 最近测过"一台大机 vs 一组小机",后者又快一倍又便宜一半。GPU 侧,书出版后他们与 Dell、Nvidia 合作做了 CPU vs GPU 的基准:数据传输到 GPU 有开销,数据集够大时提速惊人,join 密集(大量哈希与匹配)的场景最佳,Nvidia 自己的基准最高到 13 倍;但也有一两个查询在 GPU 上更慢——"没有免费的午餐,永远要实测"。新的 streaming 引擎是架构级重写:读盘时就把数据切成 morsel 微批并行处理,比内存引擎快 3 到 7 倍,未来会成为默认;未实现的算子会"慷慨地"逐节点回退到旧引擎。（`00:43:22–00:48:48`）

应用侧的一个小彩蛋是向量搜索:文本嵌入就是"文本变数组",Polars 的 array 类型(定长序列)算高维点之间的距离很高效,这背后的 Rust 底座省的就是开销。（`00:48:48–00:51:16`）

本期最有分量的故事是两人合作过的荷兰公用事业公司迁移:把一个 Python(pandas)+R 的大型代码库搬到 Polars——"很可能是第一次有公司把 Polars 跑在生产上"。业务是配电网的"最后一段铜线":能源转型让只供过热水器的小线缆突然要给特斯拉充电,他们要为 3.5 万个 subnet 模拟需求、排定升级优先级。原始系统跑一次要数小时、最高吃 700GB 内存;迁移后计算成本从约 15 万欧元降到 3.5 千欧元——98% 的削减,还压在了 5 千欧的预算线以下。方法论比数字更可复制:不做逐行翻译(pandas 与 Polars 差异太大),只看输入输出、把管线当黑盒做等价;先争到一周"创新时间",把一段 30 秒的 pandas 管线改写成 1 到 2 秒,以此说服客户;然后优先替换性能关键部分,直到全部迁完。正确性靠单元测试守门:用 from_wrapper 把打印出来的小样本数据直接粘回代码构造 DataFrame,再用 assert 断言 frame 相等;pandas 时代合理的逐行操作在 Polars 列式存储下恰恰是要改掉的心智——"成千上万列"很快变得不划算。（`00:51:16–00:58:10`）

收尾的资源清单:书 site polarsguide.com(第一章免费)、官方文档与 polars.rs(他们笑称 polars.com 被人 5 万美元挂着不卖)、API 参考里藏着 300 多个表达式;Discord 社区对新老用户都很友好。Polars 官方正在做 Cloud 与本地 Kubernetes 的分布式引擎,方向是"统一 API,从单机一路扩到大数据",并声称在托管 Spark 方案面前继续保持性能领先。（`00:58:20–00:59:47`，`01:00:09–01:01:07`）

## 来源与定位

- 原始节目：[SE Radio 727: Jeroen Janssens and Thijs Nieuwdorp on Using Polars](https://se-radio.net/2026/07/se-radio-727-jeroen-janssens-and-thijs-nieuwdorp-on-using-polars/)
- 定位：时间戳取自 ASR 逐字稿。
  - Richie Vink 的起源故事、Xomnia 与"为速度而来"（00:01:24–00:03:34）
  - data frame 概念与多语言绑定（00:03:47–00:10:32）
  - 三句文档口号：贴近机器、直觉 API、out-of-core（00:04:27–00:07:27）
  - 档案柜比喻与 Apache Arrow 互操作（00:07:27–00:10:01）
  - 放下行索引、声明式与 ggplot2 类比（00:11:34–00:14:43）
  - 表达式定义、表达式树与三章的由来（00:14:55–00:19:48）
  - join 与 concat 的适用场景（00:24:25–00:27:21）
  - tidy data、pivot/unpivot 与命名吐槽（00:27:35–00:30:03）
  - lazy 模式、谓词/投影下推与 Parquet（00:30:33–00:36:10）
  - join_asof、group_by_dynamic、滚动窗口与类别类型（00:35:56–00:40:43）
  - UDF 优先级阶梯与插件（00:40:43–00:43:22）
  - 基准测试、GPU 13 倍与流式引擎 3-7 倍（00:43:22–00:48:48）
  - 向量搜索小彩蛋与荷兰电网案例：98% 成本削减（00:48:48–00:58:10）
  - 资源清单、polars.rs 与分布式引擎方向（00:58:20–01:01:07）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 嘉宾姓名（Jeroen Janssens、Thijs Nieuwdorp）与主持人（Gregory Kapfhammer）、Polars 创始人（Richie Vink）按节目出版方元数据与公开身份核正。
- "15 万欧元降到 3.5 千欧元""700GB 内存""GPU 13 倍、流式引擎 3-7 倍"等数字均为节目口述口径，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
