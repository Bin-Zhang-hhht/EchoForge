# EchoForge · 技术播客

[![test](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/test.yml) [![collect](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/collect.yml) [![deploy](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml/badge.svg)](https://github.com/Bin-Zhang-hhht/EchoForge/actions/workflows/deploy.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

从公开 Podcast RSS 发现技术访谈，在本地保存完整逐字稿并生成可追溯的中文精编——先看重点观点与边界，再决定是否回听。

*A personal radar that turns technical podcast episodes into traceable Chinese digests.*

[浏览文章](https://bin-zhang-hhht.github.io/EchoForge/) · [产品文档](docs/product.md) · [架构文档](docs/architecture.md) · [执行计划](docs/implementation-plan.md) · [RSS 来源清单](docs/podcast-sources.md)

<img src=".github/assets/banner-workflow.png" alt="播客信号汇入本地私有保存的完整逐字稿，再提炼成关联原文、经过核查的中文精编" width="100%" />

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

## 闲时任务提示词模板

在 ZCode 客户端 **Automations → Idle-time task** 提交，项目选 EchoForge；权限模式按需放开（无人值守需免确认）。任务在全新会话中运行，因此提示词必须自包含。一次一个批次，跑完即停。以下模板已含各材料路径（官方稿 / 出版方转写 / ASR）的完整规则：

```text
按照 AGENTS.md 与 prompts/process-podcasts.md 处理一个播客批次。本任务只跑一批，完成后输出批次报告并停止，不要循环。

【分支】确认在 main 且工作区干净（有未提交改动则停止报告）；git pull --rebase 同步远端，出现冲突立即停止并说明，不要强行继续。

【预算（硬约束）】本批最多 3 篇文章、最多 1 次新 ASR、新增 ASR 音频实测时长 ≤120 分钟。超预算或材料未就绪的条目保持 pending 并写明原因；ignored 仅用于标题+简介明显不相关的条目，必须写 reason。

【材料策略】Transcript-first：先复用 local-library 已有材料，再查 RSS transcript_url 与出版方官方逐字稿（确认是逐字稿而非摘要、无截断、可读，时间戳覆盖与时长相符）。确认无完整可用官方稿时，按预算走 ASR：
- 先用 ffprobe 实测音频时长，与条目元数据出入明显时停止分析，不要硬跑；
- 用 asr-reserve 预约名额（日期式 batch-id；若该 batch-id 已有同条目的有效预约则直接复用），预约失败则该期保持 pending；
- 音频只下载到 .cache/audio/；同条目音频已存在则直接复用；
- 用 Video Agent Kit 转写，英文条目用英文模式；转写工具不可用时该期保持 pending 并在报告说明，不要改用其他未授权途径；
- 转写完成后，把 ffprobe 实测时长作为 audio_duration_seconds 字段写入转写 JSON（归档器对账必需）；
- 对转写中不确定的专有名词、数字、因果句，重转写对应片段并结合上下文交叉核实，全部解决后才加 --listening-resolved，并在 notes 记录核实了哪些内容；
- 归档用 transcript-archive：--input-type video_agent_kit_asr --source-kind video_agent_kit，--source-url 必须精确等于条目的 audio_url，--batch-id 使用预约记录的 batch-id。

【执行要求】
1. 全程在仓库根目录通过 Docker Compose 服务执行，不以宿主 Node/Python 作为验收依据。
2. 本机是 Windows：所有写文件的 Compose 运行用 sh -c '<命令>; sync' 包装，并在宿主机核对文件确实存在。
3. 拉候选窗口用：COLLECT_OUTPUT_DIR=./data/items docker compose run --rm pending --limit 10；先梳理整个窗口（明显不相关标 ignored 并写 reason），再从其余候选按预算选篇。
4. 文章在对照归档的完整逐字稿分段通读后写作，按 templates/post.md 结构；逐条核对核心观点、数字、因果、条件、归因和定位；不可核实的核心断言不发布，该期标 failed 并写明原因。
5. 依次跑 docker compose run --rm content-check 和 sh scripts/test-in-docker.sh；全绿才提交本批相关文件并推 main，禁止 force-push。
6. 推送后用 GitHub API 确认 test 与 deploy 工作流结果，并访问站点验证文章页可达；没观察到成功就不报告"已上线"。
7. ASR 音频只在逐字稿已落盘宿主机、可用性检查通过、疑点核实完成后才从 .cache/ 删除。

【批次报告】结束时输出：
- processed / ignored / failed / pending（延期原因）各自条数与逐条原因；
- 每篇文章路径；ASR 条目的 batch-id、实测时长、疑点核实记录；
- 需要人工抽查的建议：ASR 文章中的关键数字与专有名词各 2–3 处，附时间戳；
- 测试与检查结果、推送 commit、工作流状态与站点验证结果。
```

定向处理某一期时，在【材料策略】末尾追加一行指定条目并让文章预算为它让路。批次报告中的「人工抽查建议」是 ASR 质量闭环的一部分：真正的回听核查由人完成，不要跳过。

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

VitePress · Python· Docker Compose · GitHub Actions · GitHub Pages

