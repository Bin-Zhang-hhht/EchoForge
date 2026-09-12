<div align="center">
  <img src=".github/assets/banner.svg" alt="EchoForge · 技术播客中文阅读雷达" width="100%" />
</div>

# EchoForge · 技术播客

<div align="center">

[![test](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml)
[![collect](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml)
[![deploy](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml)

从公开 Podcast RSS 发现技术访谈，在本地保存完整逐字稿并生成可追溯的中文精编——先看重点观点与边界，再决定是否回听。

*A personal radar that turns technical podcast episodes into traceable Chinese digests.*

[产品文档](docs/product.md) · [架构文档](docs/architecture.md) · [执行计划](docs/implementation-plan.md) · [RSS 来源清单](docs/podcast-sources.md)

</div>

> 文档基线：v0.9 · 2026-09-12。M1、M2 已完成统一 Docker 环境的本地验证；M3 已完成三篇真实内容的本地处理、复核与站点构建，最终验收仍等待远端 Pages / Actions、私有备份恢复和用户阅读验证。未观察到的远端或用户侧结果不记为成功。

## 内容与体验

- **先判断，再回听**：每篇精编遵循「速读 → 主题正文 → 来源与定位」结构，开头说明这期讲什么、适合谁、最值得关注的点。
- **可追溯**：关键观点附时间段或可搜索的原文定位，并标注处理模型与「AI 编辑整理，请以原始节目为准」。
- **多入口浏览**：本周速览看最新整理，全部文章按年份回溯，标签页按主题聚合，节目页按播客归档；内置本地搜索。

## 它如何工作

```text
配置 Podcast RSS
        ↓
GitHub Actions 每日采集元信息（不下载正文或音频，不调用模型）
        ↓
data/items/<source>/<year>/<item_id>.json   ← 状态机：pending / processed / ignored / failed
        ↓
用户本地投放闲时任务，Transcript-first 取得完整逐字稿
（官方逐字稿优先；不可用时才在许可与预算内做 ASR）
        ↓
完整逐字稿长期保存在 local-library/（私有，不入 Git，独立备份）
        ↓
机器精编 site/posts/<source>/<year>/<item_id>.md
        ↓
脚本检查 + 源材料复核 → GitHub Pages
```

采集与编辑相互独立：几天不处理不影响元信息积累；一期材料不可用不影响其他节目。

## 核心边界

- RSS、网页、逐字稿等一切源材料视为不可信输入；只访问明确选定的公开 URL。
- 每批最多 3 篇文章、1 期新 ASR、新转写音频不超过 120 分钟；预算不足保持 `pending`，允许积压。
- 残缺材料不生成整期精编；核心主张无法核验时不发布，记 `failed` 并写明原因。
- 机器精编通过确定性检查与源材料复核后可发布，但自查不等于独立事实认证。
- 公众号稿和视频脚本必须人工核查与改写后才能发布，永不自动发布。
- `local-library/` 与 `.cache/` 不入 Git；临时音频在逐字稿 durable、疑点解决后清理。

## 快速开始

本地测试统一使用 Docker，与 GitHub Actions 调用相同的镜像阶段和 Compose 服务；不把本机 Node/Python 结果作为验收依据。

```bash
 docker compose run --rm site-build           # 生成 VitePress 产物
 docker compose run --rm collector-test       # 采集器和 M3 测试
 docker compose run --rm content-check        # 公开内容与 Git 边界检查
 docker compose run --rm collect              # 只获取 RSS 元信息
 docker compose run --rm pending --limit 10   # 候选窗口
```

`site-build` 生成站点，`collector-test` 运行采集器和 M3 测试，`content-check` 检查公开内容与 Git 边界，`collect` 写入挂载的输出目录，`pending` 验证并列出候选。Compose 服务把当前工作区的脚本、配置、测试或站点内容只读挂入锁定依赖镜像，因此直接运行与先构建后运行检查的都是当前文件。`scripts/test-in-docker.sh` 是本地和 `.github/workflows/test.yml` 共同使用的完整测试入口。Docker 是开发测试基线，不是网站或采集器的长期运行服务。

## 项目结构

```text
echoforge/
├── .github/workflows/     # collect：每日采集；deploy：构建部署；test：共享测试入口
├── config/sources.yaml    # 当前启用的 RSS 白名单与过滤条件
├── data/items/            # 每期元信息与处理状态，按来源与年份分片
├── scripts/               # 采集、检查、归档与索引生成
├── prompts/               # 本地闲时任务操作说明
├── templates/             # 文章模板
├── site/                  # VitePress 站点：本周速览、全部文章、标签页与文章
├── docs/                  # 产品 / 架构 / 执行计划 / 决策 / 来源清单
├── local-library/         # 本地长期逐字稿资产，不入 Git
└── .cache/                # 临时音频与可重建中间文件，不入 Git
```

## 技术栈

**VitePress**（默认主题 + 少量主题扩展）· **Python**（feedparser、PyYAML）· **Docker Compose**（统一的构建与测试基线）· **GitHub Actions + Pages**（采集与发布）

## 路线图

| 阶段 | 目标 | 状态 |
| --- | --- | --- |
| M1 | VitePress 默认主题网站和 GitHub Pages 发布 | 已完成本地验证，Pages 待部署验证 |
| M2 | 首批五个 RSS 的元信息采集与状态保留 | 已完成 Docker 本地验证，Actions 待验证 |
| M3 | 三篇真实笔记、逐字稿资产、质量门与一次用户阅读验收 | 三篇内容已完成本地闭环；远端部署、备份恢复与用户阅读验收待完成 |

当前可通过 Docker 构建含主页统计、本周速览、按年分组的全部文章、标签页与节目导航、一篇演示和三篇真实精编的 VitePress 站点，运行 41 项测试，采集五个 Feed 并查看剩余 16 条待处理项。M3 本批使用两份官方 transcript 和一次 Video Agent Kit ASR，三篇文章均经过完整源材料复核；私有逐字稿、音频和批次记录未进入 Git。远端工作流和部署状态只有实际运行后才会更新。
