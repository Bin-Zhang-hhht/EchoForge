# EchoForge · 技术播客

[![test](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml) [![collect](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml) [![deploy](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

从公开 Podcast RSS 发现技术访谈，在本地保存完整逐字稿并生成可追溯的中文精编——先看重点观点与边界，再决定是否回听。

*A personal radar that turns technical podcast episodes into traceable Chinese digests.*

[浏览文章](https://bin-zhang-hhht.github.io/EchoForge/) · [产品文档](docs/product.md) · [架构文档](docs/architecture.md) · [关键决策](docs/decisions.md) · [RSS 来源清单](docs/podcast-sources.md)

<img src=".github/assets/banner-workflow.png" alt="播客信号汇入本地私有保存的完整逐字稿，再提炼成关联原文、经过核查的中文精编" width="100%" />

## 内容与体验

- **先判断，再回听**：每篇精编遵循「速读 → 主题正文 → 来源与定位」结构，开头说明这期讲什么、适合谁、最值得关注的点。
- **可追溯**：关键观点附时间段或可搜索的原文定位，并标注处理模型与「AI 编辑整理，请以原始节目为准」。
- **多入口浏览**：首页直接展示最近整理，全部文章按年份回溯，标签页按主题聚合，节目页按播客归档；内置本地搜索。

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

## 快速开始

本地测试统一使用 Docker，与 GitHub Actions 调用相同的镜像阶段和 Compose 服务；不把本机 Node/Python 结果作为验收依据。

```bash
 docker compose run --rm site-build           # 生成 VitePress 产物
 docker compose run --rm collector-test       # 采集器和测试
 docker compose run --rm content-check        # 公开内容与 Git 边界检查
 docker compose run --rm collect              # 只获取 RSS 元信息
 docker compose run --rm pending --limit 10   # 候选窗口
```

Compose 服务把当前工作区的脚本、配置、测试或站点内容只读挂入锁定依赖镜像，因此直接运行与先构建后运行检查的都是当前文件。`scripts/test-in-docker.sh` 是本地和 `.github/workflows/test.yml` 共同使用的完整测试入口。Docker 是开发测试基线，不是网站或采集器的长期运行服务。

## 本地处理批次

元信息采集之后的内容处理（取得逐字稿 → 写作精编 → 检查发布）由你在本地投放 ZCode 闲时任务完成：客户端 **Automations → Idle-time task**，项目选 EchoForge；一次跑一批，跑完即停。每批预算：最多 3 篇文章、最多 1 次新 ASR、新增 ASR 音频实测 ≤120 分钟。操作规则、材料策略与检查要求以 `AGENTS.md` 和 `prompts/process-podcasts.md` 为准，提示词只需指向它们并声明单批约束，例如：

```text
按照 AGENTS.md 与 prompts/process-podcasts.md 处理一个播客批次。本任务只跑一批：最多 3 篇文章、最多 1 次新 ASR、新增 ASR 音频实测 ≤120 分钟；定向处理某一期时指明该条目并让文章预算为它让路。完成后输出批次报告（processed / ignored / failed / pending 条数与原因、文章路径、检查与部署验证结果）并停止，不要循环。
```

## 项目结构

```text
echoforge/
├── .github/workflows/     # collect：每日采集；deploy：构建部署；test：共享测试入口
├── config/sources.yaml    # 当前启用的 RSS 白名单与过滤条件
├── data/items/            # 每期元信息与处理状态，按来源与年份分片
├── scripts/               # 采集、检查、归档与索引生成
├── prompts/               # 本地闲时任务操作说明
├── templates/             # 文章模板
├── site/                  # VitePress 站点：首页最近整理、全部文章、标签页与文章
├── docs/                  # 产品 / 架构 / 关键决策 / 来源清单
├── local-library/         # 本地长期逐字稿资产，不入 Git
└── .cache/                # 临时音频与可重建中间文件，不入 Git
```

## 技术栈

VitePress · Python· Docker Compose · GitHub Actions · GitHub Pages

