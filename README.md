# EchoForge

**EchoForge · 技术播客**：从公开 Podcast RSS 发现技术访谈，在本地保存完整逐字稿并生成可追溯的中文精编，通过 GitHub Pages 提供个人技术信息雷达。

> 文档基线：v0.9 · 2026-09-12。M1、M2 已完成统一 Docker 环境的本地验证；M3 已完成三篇真实内容的本地处理、复核与站点构建，最终验收仍等待远端 Pages / Actions、私有备份恢复和用户阅读验证。未观察到的远端或用户侧结果不记为成功。v0.9 将 `data/items` 与 `site/posts` 改为按「播客来源 / 发布年份」分片，站点新增标签页。

## 阅读顺序

1. [产品文档](docs/product.md)：目标、首版边界、内容质量与处理预算。
2. [审查与决策记录](docs/decisions.md)：关键取舍及 v0.8 调整理由。
3. [架构文档](docs/architecture.md)：目录、文件契约、检查与发布流程。
4. [执行计划](docs/implementation-plan.md)：M1～M3 实施顺序和验收标准。
5. [Podcast RSS 来源清单](docs/podcast-sources.md)：人工维护的来源池及首批五个 Feed。

文档文件名统一使用英文，正文保留中文。日常规则以产品文档为准，具体契约和验收分别见架构文档与执行计划。

## 开发与测试环境

本地测试统一使用 Docker，与 GitHub Actions 调用相同的镜像阶段和 Compose 服务；不使用本机安装的 Node/Python 依赖作为验收依据。

```bash
docker compose run --rm site-build
docker compose run --rm collector-test
docker compose run --rm content-check
docker compose run --rm collect
docker compose run --rm pending --limit 10
```

`site-build` 生成 VitePress 产物，`collector-test` 运行采集器和 M3 测试，`content-check` 检查公开内容与 Git 边界，`workflow-lint` 检查 Actions，`collect` 只获取 RSS 元信息并写入挂载的输出目录，`pending` 验证并列出候选。Compose 服务把当前工作区的脚本、配置、测试或站点内容只读挂入锁定依赖镜像，因此直接运行与先构建后运行都检查当前文件。`scripts/test-in-docker.sh` 是本地和 `.github/workflows/test.yml` 共同使用的完整测试入口。Docker 是开发测试基线，不是网站或采集器的长期运行服务。

## 工作流与边界

- GitHub Actions 只收集元信息，不下载正文或音频，不调用模型。
- 本地任务优先复用或获取可用完整逐字稿；官方材料不可用时，在预算内通过 Video Agent Kit 转写。残缺材料不生成整期精编。
- 文章帮助读者决定是否回听，并理解有依据、有适用条件的重点观点，不承诺替代完整收听。
- 机器精编通过确定性检查与源材料复核后可发布；自查不等于独立事实认证。公众号和视频草稿必须人工核查与改写后再发布。
- `local-library/` 保存逐字稿和编辑材料，不入 Git，纳入私有独立备份并验证恢复。临时音频仅在逐字稿保存、可用性通过且必要回听疑点解决后清理。
- 初始每批最多生成 3 篇文章、最多新做 1 期 ASR，待转写音频总时长不超过 120 分钟。预算不足保持 `pending`，允许积压，不建设评分或调度系统。

## 实施路线

| 阶段 | 目标 | 状态 |
| --- | --- | --- |
| M1 | VitePress 默认主题网站和 GitHub Pages 发布 | 已完成本地验证，Pages 待部署验证 |
| M2 | 首批五个 RSS 的元信息采集与状态保留 | 已完成 Docker 本地验证，Actions 待验证 |
| M3 | 三篇真实笔记、逐字稿资产、质量门与一次用户阅读验收 | 三篇内容已完成本地闭环；远端部署、备份恢复与用户阅读验收待完成 |

当前可通过 Docker 构建包含一篇演示和三篇真实精编（含标签页）的 VitePress 站点、运行 37 项测试、检查公开内容、采集五个 Feed 并查看剩余 16 条待处理项。M3 本批使用两份官方 transcript 和一次 Video Agent Kit ASR，三篇文章均经过完整源材料复核；私有逐字稿、音频和批次记录未进入 Git。远端工作流和部署状态只有实际运行后才会更新，私有备份恢复与用户阅读验收也必须由相应环境实际完成。
