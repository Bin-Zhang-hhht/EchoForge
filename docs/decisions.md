# EchoForge — 关键决策

> 只保留仍然有效的决策结论。产品定位见[产品文档](product.md)，实现细节与当前行为见[架构文档](architecture.md)。

## 核心方案

| 事项 | 决定 |
| --- | --- |
| 仓库与分支 | 只维护 `main`，按目录区分代码、元信息和公开文章 |
| 发布 | 本地正常 push `main` → VitePress 构建 → Pages artifact 部署，不创建 `gh-pages` 分支 |
| 提醒 | 暂不做；只看 Actions 摘要或本地待处理列表 |
| 内容来源 | 只做公开 Podcast RSS，不实现 YouTube 模块 |
| RSS 来源管理 | [Podcast RSS源清单](podcast-sources.md) 保存人工调研的来源池；`config/sources.yaml` 只保存当前实际启用源 |
| 启用来源 | Recsperts、Data Skeptic、Latent Space、Practical AI、Software Engineering Daily 共 5 个，全部全量收集 |
| 元信息标识 | `item_id` 统一用于 JSON 字段、文件名、文章 frontmatter 和本地资产路径；以 `source_id + ':' + GUID/episode URL` 的 SHA-256 前 12 位生成后缀 |
| 采集规则 | published 优先、updated 后备并统一 UTC；默认仅收最近 30 天，本地可用 `--lookback-days` 加大窗口做冷启动或补采；每源每次运行最多新收 3 条未知日期条目（已入库条目不占配额）；采集侧只做无损过滤，关键词整词匹配仅作高流量源粗闸，主题取舍在本地候选梳理，未知时长不拒绝 |
| 转录策略 | Transcript-first；RSS → Publisher，均需可用性检查；无可用完整稿时在许可和预算内调用 Video Agent Kit ASR，不接入其他转写服务 |
| 本地逐字稿 | 完整逐字稿是长期资产，放 `local-library/`，不提交 Git，不随缓存清理 |
| 临时音频 | 仅在逐字稿已保存、可用性通过且必需回听疑点解决后删除 |
| GitHub 内容 | Machine Digest，可在本地检查通过后直接发布到 VitePress / Pages |
| 公众号 / 视频 | 机器只能生成草稿；必须人工核查、改写和确认后再发布，不做自动同步 |
| 网站 | VitePress 默认主题 + 内置本地搜索 |
| 测试环境 | 本地与 GitHub Actions 统一使用项目 Dockerfile / Compose 服务；不以宿主 Node/Python 结果作为验收依据 |

## 资产分片与定位

`data/items`、`site/posts` 与私有归档 `local-library/` 统一按 `<source_id>/<year>/<item_id>` 两层分片，年份取条目 `published_at`，无日期进 `unknown`；公开与私有资产共用同一条定位规则。文件名保持 `<item_id>`，状态变化不移动文件。演示文章 `demo-vitepress-site.md` 是唯一允许平铺在 `site/posts/` 根目录的正式文章；`.batches/` 是批次簿记，保留在 `local-library/` 根。

## 其他有效约定

- 标签复用优先、单篇 2～4 个，不为单期发明一次性标签；生成器不自动清理历史标签目录，清理旧派生产物属于构建维护步骤。
- 文章篇幅 1,000～3,000 字、正文 3～5 个关键主题均只是指导，不是发布门槛；完整材料优先于凑够文章数。
