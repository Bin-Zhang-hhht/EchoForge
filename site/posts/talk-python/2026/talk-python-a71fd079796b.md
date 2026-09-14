---
item_id: talk-python-a71fd079796b
title: '把数据湖元数据放回数据库：DuckLake 的 SQL Catalog 与小文件解法'
date: '2026-09-14'
published_at: '2026-09-10'
transcribed_at: '2026-09-14'
model: 'GPT-5.6'
source_url: 'https://talkpython.fm/episodes/show/562/ducklake-the-lakehouse-thats-just-sql-and-parquet'
source_name: 'Talk Python To Me'
input_type: official_transcript
transcript_url: 'https://talkpython.fm/episodes/show/562/ducklake-the-lakehouse-thats-just-sql-and-parquet.vtt'
summary: 'DuckLake 把数据湖元数据交给 SQL 数据库、数据保留为 Parquet，以一次 catalog 查询替代多层元数据文件；本期也讲清 catalog 选型、小文件优化与生产边界。'
tags: [数据库, 开放标准, 分布式系统]
---

# 把数据湖元数据放回数据库：DuckLake 的 SQL Catalog 与小文件解法

> 节目：[Talk Python To Me](/podcasts/talk-python/)
>
> 节目发布：2026-09-10 · 逐字稿获取：2026-09-14 · 笔记整理：2026-09-14
>
> 全文共 4426 字 · 阅读约 12 分钟
>
> 标签：[数据库](/tags/%E6%95%B0%E6%8D%AE%E5%BA%93/) [开放标准](/tags/%E5%BC%80%E6%94%BE%E6%A0%87%E5%87%86/) [分布式系统](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/)
>
> 🎧 [收听原节目](https://talkpython.fm/episodes/show/562/ducklake-the-lakehouse-thats-just-sql-and-parquet) · 📄 [查看官方逐字稿](https://talkpython.fm/episodes/show/562/ducklake-the-lakehouse-thats-just-sql-and-parquet.vtt)

## 速读

DuckLake 把数据湖元数据交给 SQL 数据库、数据保留为 Parquet，以一次 catalog 查询替代多层元数据文件；本期也讲清 catalog 选型、小文件优化与生产边界。嘉宾 Pedro Holanda 是 DuckLake 的主要开发者，Guillermo Sanchez Dionis 参与 DuckLake 与 Quack 协议开发。这期适合正在评估 Iceberg、Delta 等开放表格式，或想用 DuckDB 搭建轻量分析基础设施的工程师。

最值得带走的不是“SQL 加 Parquet”这一句口号，而是几组清楚的取舍：对象存储、catalog 与计算引擎仍然分层；本地 DuckDB catalog 简单但只允许一个写入者，生产多写入者通常转向 Postgres；Quack 的服务端重试展示出高并发潜力，但录制时仍属实验阶段。嘉宾还给出 data inlining、compaction 与 frozen DuckLake 三种不同工作负载下的方案，并明确区分 DuckLake 已可生产使用与 Quack 暂不宜生产使用。

## 主题正文

### 从元数据文件链，缩成一次 SQL 查询

开放表格式的基本价值，是给 Parquet 数据及其元数据提供公开规范，使不同引擎可以实现读写器，理论上减少对单一数据库或云平台的锁定。其元数据至少要描述哪些文件构成一张表、schema 是什么，还可加入文件级统计信息，以支持事务式、原子的数据操作。（`00:14:31–00:16:38`）

DuckLake 的关键改动是：对象存储中只留下 Parquet 数据文件，把 metadata 放进真正的 SQL 数据库。Pedro 解释，Iceberg 需要穿过 JSON、Avro 等多层元数据文件才能找到目标 Parquet；DuckLake 则向 catalog 发出 SQL 查询，直接取得某个 snapshot 要读的文件清单。Guillermo 将其概括为“一次 SQL 查询”，认为这降低了读写引擎实现格式时的复杂度。（`00:36:33–00:38:49`，`00:43:30–00:43:56`）

完整架构仍有三个独立部分。storage 可以是 S3、GCS 或 Azure Blob Storage，保存 Parquet；catalog service 保存文件清单、schema、统计和 snapshot 等元数据，DuckDB 的 DuckLake 扩展可连接 MySQL、Postgres、SQLite、DuckDB 与 Quack；compute 则负责实际读取文件和执行查询，可以是 DuckDB，也可以是实现了该格式的其他引擎。节目提到已有 DataFusion 实现，以及 MotherDuck 因客户 ETL 需求开发的 Spark writer；因此 DuckLake 并不等于“只能由 DuckDB 使用”。（`00:41:45–00:44:05`，`00:47:48–00:48:50`，`01:01:55–01:02:50`）

### Catalog 选型取决于写入并发，而非数据总量

catalog 要扩展的是元数据规模，不是 Parquet 数据本身的规模。Pedro 带有保留地说，catalog 只需支持 timestamp、varchar、integer 与 primary key，满足这些能力的系统理论上都可承载 DuckLake catalog；对象存储仍负责扩展实际数据容量。主持人也提醒，“可扩展”不等于单次查询一定快：多次对象存储往返即使能稳定扩到更多用户，基础延迟仍然存在。（`00:39:48–00:41:24`）

选择 catalog 时，最具体的边界是写入模式。DuckDB 进程内方案适合本机开发、个人数据湖或单写入者，但一个 DuckDB catalog 同时只能连接一个 writer；Pedro 称他在生产场景看到的多数用户会选 Postgres，以允许多个客户端写入。Quack 则把 DuckDB 暴露为可自托管的 client-server 服务，使用 HTTP，并能在服务端加载 DuckLake；但嘉宾明确说录制时 Quack 仍是实验项目，不要用于生产，首个稳定版本预计随 DuckDB 2.0 到来。这里的时间表是受访者在 2026-08-31 录制时的预期，不是本文独立确认的发布承诺。（`00:34:10–00:35:16`，`00:49:36–00:50:40`）

Quack 的潜力体现在冲突重试的位置。Pedro 给出的高争用测试条件约为 20 个 writers：以 Postgres 作 catalog 时，snapshot ID 冲突要回到应用端重算并重新发送，他称结果约为每秒 5 个事务；DuckDB 加 Quack 可在服务端完成重试，他称约为每秒 200 个事务。Guillermo 补充，这类开放表格式原本偏向批处理而非事务负载，200 TPS 是他们在高争用环境中的结果；Postgres 理论上也可通过 stored procedure 做类似优化，但当时尚未实现。因此这些数字只能视为嘉宾对特定实现与测试条件的报告，不能外推为所有部署的通用吞吐量。（`00:50:42–00:53:35`）

### 小文件问题有三种不同层次的处理方式

Parquet 文件大小不是格式常量。Guillermo 举例可把目标设为 512 MB，批量写入时按该目标与 row group 大小生成文件；频繁小写入则会产生大量小文件，通常需要 compaction，把许多小文件合并为较大的文件。原因不是“小文件不能读”，而是引擎不愿为上千个 5 KB 文件反复承担请求延迟，更大的文件仍可并行读取。512 MB、1000 个与 5 KB 都是嘉宾用于说明机制的示例，不是通用配置建议。（`00:45:32–00:46:30`）

DuckLake 的 data inlining 进一步把尚未长大的数据暂存在 catalog 内的表中，而不是每次小插入都立刻创建 Parquet。Pedro 举例说，小批可能是 10、100 或 1000 行；等 inline table 足够大，再移出并生成真正的数据文件。这样既保留 snapshot 与事务语义，也减少小文件及远程对象存储往返。他引用自己的博客基准称，相对“raw Iceberg 与 raw DuckLake”的对比约快 1000 倍，但当场也明确了比较对象；节目没有展开硬件、数据集与完整基准方法，所以这个数字只能作为该实验结果，不能当作普遍加速比例。（`00:56:07–00:59:26`）

另一种场景是 frozen DuckLake：若数据一天只批量更新一次，可以把 DuckDB catalog 文件拉到本地更新、把数据写到 S3，再把 catalog 文件上传回去。此后任意数量的客户端可从对象存储只读访问，无需持续运行 Postgres 或 Quack 服务。它换取的是近乎无 catalog 服务运维的读取方式，条件则是单批写入、发布后只读，并不适合持续多写入者事务。（`00:54:24–00:56:05`）

### DuckLake 已称可生产，Quack 仍需等待

Pedro 说，团队从 DuckLake 0.4 到 1.0 曾暂停增加新功能，集中修 bug，并只在修 bug 所需时改 schema；他认为自 2026 年 4 月起 DuckLake 应已具备生产条件，但同时承认软件仍有 issue 与 bug report。团队为长期运行补齐 checkpointing 相关能力，包括 compaction、把 deletion 合并进重写的数据文件、清理 orphan files 与旧文件，目标是避免数据持续增长后系统停滞。Guillermo 以已有公司把软件建立在 DuckLake 上作为采用证据，不过这仍是嘉宾陈述，不等于本文对这些生产部署做了独立验证。（`01:03:04–01:04:11`，`01:05:10–01:06:36`）

规格与实现的演进速度也被刻意分开：catalog schema 的 specification 尽量冻结，只有真正必要时发布破坏性变更；DuckDB extension 则可继续加入性能优化与非破坏性功能。团队还在增强与 Iceberg 的互操作，希望能读取和导出 Iceberg，避免用户再次被锁在 DuckLake 自己的格式里。（`01:03:55–01:05:07`）

入门建议很保守：先从进程内 DuckDB 开始，因为无需先配置 Postgres 服务；看官网示例与教程，按自己的写入、共享和运维需求验证是否合适。若报告问题，Pedro 建议提交可复现的完整脚本、数据生成方式与具体故障，以缩短团队复现和修复路径。不要因为 DuckLake 被称为 production ready，就把同一期仍被标为 experimental 的 Quack 一并视为生产就绪。（`01:06:42–01:07:36`，`01:08:46–01:09:09`）

## 来源与定位

- 原始节目：[#562: DuckLake: The Lakehouse That's Just SQL and Parquet](https://talkpython.fm/episodes/show/562/ducklake-the-lakehouse-thats-just-sql-and-parquet)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - 开放表格式的组成、规范与可迁移性（00:14:31–00:16:38）
  - DuckLake 把 metadata 放入数据库、以 SQL 查询取得文件清单（00:36:33–00:38:49）
  - storage、catalog service、compute 三层架构与支持的实现（00:41:45–00:44:05）
  - 数据规模与 catalog 元数据规模的区别（00:39:48–00:41:24）
  - Quack 的自托管方式、HTTP 协议与服务形态（00:34:10–00:35:16）
  - DuckDB、Postgres 与实验阶段 Quack 的 catalog 选择边界（00:49:36–00:50:40）
  - 约 20 writers 高争用下 5 TPS 与 200 TPS 的嘉宾测试陈述（00:50:42–00:53:35）
  - 512 MB 目标文件、5 KB 小文件与 compaction 示例（00:45:32–00:46:30）
  - data inlining 的机制与约 1000 倍 raw benchmark 限定（00:56:07–00:59:26）
  - frozen DuckLake 的每日批量更新与任意只读连接条件（00:54:24–00:56:05）
  - DuckLake 生产就绪判断、维护功能与仍存在 bug 的限定（01:03:04–01:06:36）
  - 规格冻结、扩展演进及 Iceberg 互操作方向（01:03:55–01:05:07）
  - 从进程内 DuckDB 开始及可复现问题报告建议（01:06:42–01:09:09）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- 吞吐量、加速比例、文件与批次大小均保留了嘉宾归属和节目给出的测试或示例条件；本文未独立复现实验，也不把录制时的版本时间表视为发布承诺。
- 整理模型：GPT-5.6
- AI 编辑整理，请以原始节目为准。
