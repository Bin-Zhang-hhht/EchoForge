---
item_id: software-engineering-radio-0bd9e489b729
title: Apache Iceberg：把数据沼泽改造成湖仓的"USB-C"开放表格式
date: '2026-09-17'
published_at: '2026-09-03'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://se-radio.net/2026/09/se-radio-736-sahil-walia-on-apache-iceberg/'
source_name: 'Software Engineering Radio'
input_type: video_agent_kit_asr
summary: 'Snowflake 高级技术架构师 Sahil Walia 逐层拆解 Apache Iceberg：从 OLTP/OLAP 切换判据与湖仓演进，到 catalog→metadata JSON→manifest 的三层元数据树、时间旅行与乐观并发，再到引擎与目录生态为何正在收敛到这张"开放表格"。'
tags: [数据库, 开放标准, 数据工程]
---

# Apache Iceberg：把数据沼泽改造成湖仓的"USB-C"开放表格式

> 节目：[Software Engineering Radio](/podcasts/software-engineering-radio/)
>
> 节目发布：2026-09-03 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 4938 字 · 阅读约 13 分钟
>
> 标签：[数据库](/tags/%E6%95%B0%E6%8D%AE%E5%BA%93/) [开放标准](/tags/%E5%BC%80%E6%94%BE%E6%A0%87%E5%87%86/) [数据工程](/tags/%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B/)
>
> 🎧 [收听原节目](https://se-radio.net/2026/09/se-radio-736-sahil-walia-on-apache-iceberg/)

## 速读

Snowflake 高级技术架构师 Sahil Walia 与主持人 Robert Blumen 用一整期把 Apache Iceberg 从"为什么需要"讲到"怎么工作"：数据仓库像文件柜、数据湖像自助仓储，而 Iceberg 是让廉价对象存储长出表语义的开放表格式——spec、多语言实现、REST catalog 三件套，让 Spark、Trino、Snowflake、Databricks 安全地读写同一张表。

最值得带走的三点：Iceberg 丰富的文件级元数据把 S3 列表调用从成百上千次压到十几次，既绕开限流也决定查询速度；每次提交都是快照，误删数百万行的作业可以按快照秒级回滚——主持人与嘉宾都认为这对 Agent 直连数据库的时代格外及时；写路径以 metadata JSON 的 compare-and-swap 收尾，乐观并发下输家只需重写元数据而非数据文件。

## 主题正文

### 何时离开 OLTP:判据与湖仓演进

Walia 先给了一组务实的切换判据：延迟预算以毫秒计、要主键约束和频繁单行写，留在 OLTP;预算放宽到秒和分钟、以分析和 ML 为主、读多聚合多、宽表场景，就该考虑 OLAP。数据规模从 GB 到 TB、PB 都有——他把 PB 量级换算成"大约两亿两千万首歌"，并提到 Netflix 在 PB 规模上对 Iceberg 做过基准验证。（`00:02:01–00:03:47`）

背景概念他用了两个比喻：数据仓库是文件柜——schema-on-write、精心策划、为 BI 优化；数据湖是自助仓储——云端对象存储什么都往里放，append-only、读取时再管理，结果常常变成没人管得了的数据沼泽。湖仓一体的思路是把文件柜放进自助仓储：享受廉价存储，同时拿回仓库级的结构与事务保证。（`00:04:09–00:07:11`）

### Headless 基础设施与 Iceberg 的三件套

主持人用 Postgres 点出旧世界的本质：存储引擎与计算引擎紧耦合、互为彼此设计，你不会拿"Postgres 的文件格式"去跑 Oracle。Walia 引 Confluence 博客的说法把这股变化称为 headless data infrastructure：数据与计算分离后可以独立扩展，同一份 S3 数据被多个引擎直接访问、无需维护多副本，Spark、Databricks、Snowflake 想接谁接谁。（`00:07:11–00:09:34`）

Iceberg 就是为这套架构铺路的开放表格式：它定义数据文件与元数据文件的组织方式，让多个引擎安全地读写同一张表。组成上是三件套——spec(委员会定的"规则文档",各引擎遵循以达成互操作)、各语言实现(Java、Python、Go、Rust,或许还有 C++,但他的经验是团队很少自己投入实现，功夫都花在与 catalog 的集成上)、以及 REST catalog(标准化的 HTTP API,引擎经它访问表)。他给的两个类比都好记：像 XML 那样的开放格式与多语言 binding;更像 USB-C——一个通用接口,MacBook、手机都能插。历史上它起于 Netflix 的 PB 级痛点(当时 Hive 的元数据管理撑不住)，早期有 Apple 等公司贡献，成熟后捐给 Apache 软件基金会孵化并转正。（`00:09:34–00:14:38`）

### 解耦会牺牲性能吗:基准收敛与 S3 限流的元数据解法

主持人替所有人问了那个尖锐的问题：旧式紧耦合是为了物理 IO 优化，把数据放 S3 是不是就要牺牲性能？Walia 的回答分时间线：Iceberg 现在是 V3 spec,早期各引擎基准结果分歧很大——封闭引擎天然更懂自己的文件；但近三四五年厂商收敛明显，各家都在让自己的引擎对 Iceberg 跑得更快，近期基准显示"持平甚至有时更好"。至于锁定：你确实逃离了厂商锁定，但 S3 便宜(节目口径约每 TB 23 美元)、数据归你自己管，将来换引擎只是换计算层，不必再做那种伤筋动骨的迁移。（`00:15:31–00:17:25`）

S3 的真实瓶颈是列表操作的限流：Hive 时代要列目录、成百上千次 API 调用；Iceberg 的元数据做到了文件级，查询时只需十来次调用就能定位目标文件，既绕开限流也直接决定读速度。他同时强调这是元数据与算力的合力,二者要放在一起优化。（`00:19:00–00:20:52`）

### 快照与时间旅行:秒级回滚,和一场关于 GDPR 的现场商榷

Iceberg 的每次提交都是一个带 ID 的快照，时间旅行因此是查询语法层面的事:`timestamp as of` 回到某时刻,`version as of` 回到某快照。最生动的用例是误删回滚：一个本想删 500 行的作业删掉了 200 万行,回滚到上一快照，数据几秒内复原。主持人顺势联系时事——现在到处是让 AI Agent 直连数据库的故事，这类"删得太宽"的事故只会更多；Walia 说很多 AI 工作负载确实格外看重这个特性，"没人想解释自己没细看就执行了过宽的删除"。（`00:22:37–00:26:44`）

值得保留的是这段里的一次现场商榷：Walia 先用 GDPR"被遗忘权"举例，主持人追问后他指出这未必是贴切的例子——合规删除要求把数据文件和元数据链接真正清掉，而不是靠时间旅行"演示记录曾经存在";主持人再补了一句：审计场景下你能证明"五天前记录在、今天不在"，但磁盘上数据可能仍在，只是没有链接可达。这段一来一回把时间旅行的能力边界讲清楚了，本文按节目原样保留双方观点。（`00:24:09–00:25:40`）

### 两种写入模式、Parquet 与一次读的完整旅程

Iceberg 面向分析负载,写入以批量为主而非柜员式事务写。改一条记录有两种代价模型：copy-on-write 重写整个新文件,读最快;merge-on-read 保留原文件、给记录贴"删除便签",读取时由计算引擎现场扣除——按工作负载选。（`00:26:44–00:28:38`）

底下的 Parquet 是列式文件格式(类比 .xlsx 之于 Excel):按列连续存储、压缩后小得多(节目口径三到四倍)、自描述(schema 在文件 footer)、支持谓词下推——按 row group 直达目标块，不用全扫描——还支持 struct、array、map 等复杂类型。（`00:28:49–00:31:33`）

Iceberg 的元数据是一棵三层树:顶端 catalog 回答"表 X 在哪"，指向最新一版 metadata JSON;JSON 里的快照指向 manifest list(Avro 文件,含分区信息，第一层剪枝);manifest list 指向 manifest 文件(Avro,逐文件统计每列 min/max、行数);树的最底层才是 Parquet 数据文件。一次 `select * from events where date = '2025-07'` 的旅程就是：catalog 给出最新 V5.metadata JSON → 快照找到 manifest list → manifest 按 min/max 跳过不含七月的数据文件 → 只读底部那几个 Parquet。时间旅行则是在 metadata JSON 的 snapshot log 时间线上取历史 cutoff。（`00:31:55–00:35:54`）

### 写路径的乐观并发、表维护与生态落地

写与读互为镜像：引擎先按目标文件大小把数据文件写进对象存储(此时其他引擎看不见)，再写 manifest、manifest list,最后写 metadata JSON——这一步是 compare-and-swap,若期间元数据已被别人改过就重做新版，否则写入 version+1 使其成为当前版本。并发模型因此是：读隔离锁在你开始读取的快照上；写采用乐观并发，先提交者赢，输家收到拒绝后只需重写元数据——数据文件原样不动。崩溃留下的孤儿文件没有任何元数据引用，不会造成脏读，只需要偶尔清理存储。（`00:36:16–00:40:05`）

日常维护两件事：快照过期(按工作负载配置保留窗口，过期即不可再回溯)和数据合并(把周末攒出的小文件合并成适合读取模式的大文件，类比 Postgres 的 vacuum full;托管引擎多带此服务，也可以自己跑)。（`00:40:05–00:41:46`）

生态的分工边界是本期的另一半要点：join 支持没问题(Iceberg 表之间，乃至经由引擎与自定义表格式互通)，但查询规划是引擎的事——Iceberg 只提供做 join planning 的统计信息，不规定执行方式。引擎侧开源有 Spark、Flink、Trino,商业有 Snowflake、Databricks、BigQuery,凡兼容 spec 皆可用；catalog 的选项包括 AWS Glue(新近兼容 Iceberg REST)、Snowflake Horizon、Databricks Unity Catalog 和在云端已少用的 Hive Metastore。选型看三点：对 spec 版本的支持程度(当前 GA 的 V3 已支持纳秒时间戳)、跨引擎的治理与 RBAC 如何传递、以及凭据如何下发到存储。（`00:41:46–00:46:00`）

他给出的落地案例串起了全套栈：点击流先落 Postgres(OLTP),经 Apache Pulsar 批住约 15 分钟后推进 Snowflake 做清洗与加工，ML 团队则用 Spark 直接读 Snowflake 写在 S3 上的同一批表——多团队共享数据、免冗余存储、也免掉为不同团队重复做几乎相同的变换。AI 场景的新玩法是数据分支：用 Nessie 这类 catalog 把训练数据 branch 出 A/B 两支，分别训练对比。收尾的判断是行业性的：V4 spec 已在协作中尚未定稿，厂商正从私有格式收敛到 Iceberg,"现在是 adoption 的好时机",他也建议想深入的人去读 Apache Iceberg 的 dev list。（`00:46:00–00:50:39`）

## 来源与定位

- 原始节目：[SE Radio 736: Sahil Walia on Apache Iceberg](https://se-radio.net/2026/09/se-radio-736-sahil-walia-on-apache-iceberg/)
- 定位：时间戳取自 ASR 逐字稿。
  - OLTP/OLAP 切换判据与 PB 规模的换算（00:02:01–00:03:47）
  - 数据仓库、数据湖、数据沼泽与湖仓一体的比喻（00:04:09–00:07:11）
  - 存储与计算耦合的旧世界、headless data infrastructure（00:07:11–00:09:34）
  - Iceberg 定义、spec/实现/REST catalog 三件套与两个类比（00:09:34–00:14:38）
  - 早期基准分歧、近年收敛与 S3 的成本与锁定权衡（00:15:31–00:17:25）
  - S3 列表限流与文件级元数据把调用压到十几次（00:19:00–00:20:52）
  - 快照、timestamp/version as of 与误删回滚（00:22:37–00:26:08）
  - GDPR 例子的现场商榷与能力边界（00:24:09–00:25:40）
  - 批量写入与 copy-on-write / merge-on-read（00:26:44–00:28:38）
  - Parquet 列存、自描述与谓词下推（00:28:49–00:31:33）
  - catalog→metadata JSON→manifest list→manifest 的三层树与读路径实例（00:31:55–00:35:54）
  - 写路径 compare-and-swap、乐观并发与孤儿文件（00:36:16–00:40:05）
  - 快照过期与数据合并（00:40:05–00:41:46）
  - join 与查询规划的归属、引擎与 catalog 生态选型（00:41:46–00:46:00）
  - 点击流落地案例、Nessie 数据分支与 V4 收尾（00:46:00–00:50:39）

## 整理说明

- 本文基于节目内容与本地 ASR 转写整理，时间戳和关键事实按可用材料核查。
- 嘉宾人名（Sahil Walia）按节目出版方元数据核正；ASR 中的少量专名变体已按此校准。
- "两亿两千万首歌""每 TB 约 23 美元""压缩三到四倍"等数字均为节目中的口径或举例，本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
