# EchoForge — 架构文档

> 版本：v0.9 · 2026-09-12
> 依据：[产品文档](product.md)
> 状态：M1、M2 已完成统一 Docker 环境的本地验证；M3 的 transcript archive、ASR 预约、内容检查和三篇真实文章已完成本地闭环。远端 Pages / Actions、私有备份恢复及用户阅读验收待验证。项目正式命名为 **EchoForge**，建议仓库及本地目录名统一为 `echoforge`。v0.9 将公开数据与文章改为按来源和年份分片存储。

## 1. 总体结构

```text
GitHub Actions                   用户本地 ZCode                         GitHub Actions
collect.yml                                                            deploy.yml
    │                               │                                      │
读取 RSS → 过滤                    Transcript Resolver                    VitePress 构建
    │                              ├─ 已有 transcript                       │
    │                              └─ Video Agent Kit ASR                  │
    │                               │                                      │
    │                       local-library/ 长期逐字稿                        │
    │                               │                                      │
    └── data/items/<source>/<year>/*.json ──Git──→ GLM 机器精编 ── site/posts/<source>/<year>/*.md ─push─→ Pages
                                    │
                                    ├─ wechat-draft.md ──人工审核→ 手动发布
                                    └─ video-script.md ──人工审核→ 后续视频制作
```

只有一个 `main` 分支。`data/` 是普通目录，不是分支；不用 worktree、跨分支 dispatch、双 SHA 发布协议或数据晋升流程。网站通过 Pages artifact 部署，不再创建 `gh-pages` 发布分支。

**本地长期资产与 Git 仓库严格分层：** `local-library/` 保存逐字稿和人工编辑材料；`.cache/` 只放临时音频和可随时重建的中间文件；两者都不提交 Git。

## 2. 技术与目录

采集使用 Python 和现成 RSS 解析库；网站使用 VitePress 默认主题。依赖选兼容的稳定版本并锁定，不把框架预览版作为必需条件。本地测试与 GitHub Actions 统一通过项目 Dockerfile 和 Compose 服务运行，使用相同基础镜像、锁文件和命令；不以本机 Node/Python 环境作为验收依据。Docker 用于构建、测试和批次任务，不建设常驻容器服务。

```text
echoforge/
├── .github/workflows/
│   ├── collect.yml               # 每日采集，只写元信息
│   └── deploy.yml                # main 更新后构建、部署网站
├── config/
│   └── sources.yaml              # 当前实际启用的 RSS 白名单和简单过滤条件
├── data/items/
│   └── <source_id>/<year>/
│       └── <item_id>.json        # 每期一个文件，包含处理状态；按来源与发布年份分片
├── scripts/
│   ├── collect.py                # RSS 读取、去重、过滤、保存
│   ├── pending.py                # 输出待处理条目及数量
│   ├── archive_transcript.py       # 审核确认、格式转换、完整性与归档幂等检查
│   ├── reserve_asr.py              # 转写前原子预约本批唯一 ASR 名额
│   ├── check.py                    # 少量数据、文章及安全检查
│   └── build-index.mjs           # 从 Markdown 生成文章列表与标签页
├── prompts/
│   └── process-podcasts.md       # 本地闲时任务操作说明
├── templates/
│   └── post.md                   # GitHub 机器摘要模板
├── site/
│   ├── .vitepress/
│   │   ├── config.mts            # 导入生成的侧边栏数据
│   │   ├── theme/                # 扩展默认主题：文章元信息卡样式
│   │   │   ├── index.mts
│   │   │   └── custom.css
│   │   └── sidebar.data.json     # 构建生成的侧边栏配置，不提交 Git
│   ├── index.md                  # 构建生成的首页（统计与节目卡），不提交 Git
│   ├── public/
│   │   └── logo.svg              # 站点标识与 favicon
│   ├── posts/
│   │   ├── index.md              # 构建生成，不提交 Git
│   │   ├── demo-vitepress-site.md  # M1 演示文章，直接位于 posts 根目录
│   │   └── <source_id>/
│   │       ├── index.md          # 构建生成的节目页，不提交 Git
│   │       └── <year>/
│   │           └── <item_id>.md  # 正式公开文章，按来源与发布年份分片
│   └── tags/
│       └── index.md              # 构建生成的标签页，不提交 Git
├── docs/
│   ├── product.md
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── decisions.md
│   └── podcast-sources.md         # 人工维护的来源池，不是运行时自动发现模块
├── local-library/                # 本地长期内容资产，不提交 Git
│   └── <source_id>/<item_id>/
│       ├── metadata.yaml
│       ├── transcript.md         # 人工阅读用完整逐字稿
│       ├── transcript.json       # 有结构化时间戳时保留；没有则不伪造
│       ├── transcript.vtt        # 来源/工具提供时原样保留，可选
│       ├── machine-summary.md    # 可选，本地机器精编工作稿
│       ├── editorial-notes.md    # 人工核查与编辑笔记，可选
│       ├── wechat-draft.md       # 公众号人工草稿，可选
│       └── video-script.md       # 视频人工草稿，可选
├── .cache/                       # 临时音频和可重建中间文件，不提交 Git
├── AGENTS.md                     # 项目操作边界
├── README.md
├── package.json
├── package-lock.json
└── requirements.txt
```

`local-library/` 是逻辑默认路径，实际使用时也可以将它放在项目外部长期目录，但首版不为此开发存储抽象层。

只把 `site/` 作为 VitePress 内容根目录。项目文档、元信息、本地资产和缓存不加入站点构建；这不代表公开仓库里的 `data/` 是私密数据。

`.gitignore` 至少排除 `local-library/`、`.cache/`、`.env`、依赖目录、VitePress 构建/缓存目录和生成的文章列表。不提交媒体、完整转录、人工草稿、凭据及带私密令牌的订阅地址。

## 3. 文件约定

### 3.1 来源配置

所有实际采集来源在 `config/sources.yaml` 维护，不为一种来源拆一套配置系统。经过人工调研的来源池单独记录在 [Podcast RSS源清单](podcast-sources.md)；运行时不读取该文档，也不自动发现新源。

M2 首次联调只加入 5 个 Feed：Recsperts、Data Skeptic、Latent Space、Practical AI 和 Software Engineering Daily。其他来源是否加入，只通过后续人工修改 `sources.yaml` 完成。

```yaml
sources:
  - id: example-podcast
    name: Example Podcast
    url: https://example.com/feed.xml
    enabled: true
    include_keywords: []
    exclude_keywords: []
    min_duration_minutes: null
```

包含词为空表示接受该来源的所有候选，否则对清洗后的标题与简短简介做不区分大小写的子串匹配，命中任一词即可。排除词优先。已知时长低于 `min_duration_minutes` 才过滤，时长未知不因缺失而丢弃；支持秒数和 `HH:MM:SS` 等常见格式，无法解析则视为未知。首版每次只接收最近 30 天的节目，已入库的待处理条目不会因此被删除；日期优先使用 published，缺失时使用 updated，统一为 UTC ISO-8601，无法解析的日期视为未知。每个来源最多接收 3 条未知日期条目，按 Feed 顺序处理；历史回填以后再做。

每个新 Feed 进入 `sources.yaml` 前做一次最小 smoke test：能访问、能被所选 RSS 解析库解析、能读到节目/单集标题，并能获得 GUID、episode URL 等至少一种稳定标识。Podcast Feed 若提供 enclosure/audio URL 或 transcript URL，则正常提取；缺失字段不由采集器猜测。采集器只访问 Feed 本身，不跟进音频或 transcript URL。

### 3.2 单期元信息

稳定 `item_id` 优先以 `source_id + ':' + RSS GUID` 的 SHA-256 前 12 位生成后缀，GUID 缺失时使用节目页面链接；两者都没有就跳过并记录日志。完整 ID 为 `<source_id>-<hash>`。不使用标题作为唯一标识，不使用可能变化的音频地址作为首选标识；同一输入必须始终得到相同 ID。

```json
{
  "item_id": "example-podcast-a1b2c3d4",
  "source_id": "example-podcast",
  "source_name": "Example Podcast",
  "guid": "episode-123",
  "title": "An interview about AI agents",
  "url": "https://example.com/episodes/123",
  "published_at": "2026-09-10T08:00:00Z",
  "description": "来自 RSS 的简短节目介绍。",
  "audio_url": "https://example.com/episode-123.mp3",
  "transcript_url": null,
  "duration_seconds": 3600,
  "status": "pending",
  "reason": null
}
```

缺失字段用 `null`。简介转为纯文本并限制长度，首版上限 1,000 字符；不保存完整 Feed 响应或内嵌全文。文件名使用与 `item_id` 相同的程序生成安全 ID。

单期元信息按来源和发布年份分片保存：`data/items/<source_id>/<year>/<item_id>.json`。年份取 `published_at` 的前 4 位，日期未知时存入 `unknown` 目录。采集器按同一布局写入新文件；文件名保持 `<item_id>.json`，不随分片改变。

**Collector 只新增文件；已有文件原样保留。** 本地任务只更新选中条目的状态及原因，必要时修正失效链接。暂不实现定期元信息刷新或跨节目模糊去重。

`pending.py` 直接扫描这些文件，按发布时间从新到旧列出 `pending`；未知日期排在后面。无需另存 `pending.json` 或独立队列数据库。

### 3.3 本地逐字稿资产

每期处理成功后，在 `local-library/<source_id>/<item_id>/` 至少保留：

- `metadata.yaml`：最小记录，包括来源获取方式、URL、获取时间、可用性说明和内容检查结论；不建设 evidence 数据库；
- `transcript.md`：完整逐字稿，供人工阅读、公众号编辑和视频选段；
- 时间戳 / speaker 等结构化文件：来源或转写工具实际提供时保存，例如 `transcript.json`、`transcript.vtt`，缺失时不伪造。

逐字稿获取遵循 transcript-first：先获取完整且可用的官方 / RSS transcript；只有无法取得完整 transcript、且允许使用 ASR 并未超出本批预算时，才下载音频并转写。官方稿和 ASR 都必须检查期次身份、确实是逐字稿而非摘要、是否有明显截断或不可读内容，以及在可取得时的时间戳覆盖与节目时长是否相符；“成功”或文件存在本身不算通过。完整但不可用的材料记为失败；因预算跳过记为 pending 并说明原因。不能用部分材料生成整期总结，也不能用标题或简介替代正文。

ASR 后对不确定的专有名词、关键术语、数字和因果表述回听核对；回听疑点未解决前不得清理音频。音频清理是所有任务的共同收尾动作，且仅在逐字稿已保存、可用性检查通过并完成所需回听后进行，不得提前删除。

本地逐字稿是可复用资产，**不因 GitHub 文章已经发布而删除**。机器摘要、人工笔记和渠道草稿可以继续挂在同一期目录下，但首版不要求所有文件都存在。项目必须使用用户已有的私有备份机制，保留独立于工作目录的副本，覆盖逐字稿和编辑笔记；不建设备份服务。首次恢复验证至少检查逐字稿和编辑笔记均能恢复。

### 3.4 GitHub 文章

文章保存为 `site/posts/<source_id>/<year>/<item_id>.md`，按来源与发布年份和元信息同轴分片，其 `item_id` 对应 `data/items/<source_id>/<year>/<item_id>.json`。演示文章 `demo-vitepress-site.md` 是唯一允许直接位于 `site/posts/` 根目录的正式文章。例如：

```yaml
---
item_id: example-podcast-a1b2c3d4
title: 从一次访谈看 Agent 的实际落地难点
date: '2026-09-10'
published_at: '2026-09-08'
transcribed_at: '2026-09-10'
model: GLM
source_url: https://example.com/episodes/123
source_name: Example Podcast
input_type: official_transcript
tags: [Agent]
---
```

必填 `item_id`、`title`、`date`、`source_url`。其余字段按实际情况填写；`input_type` 可记录 `official_transcript` 或 `video_agent_kit_asr`。`date` 是笔记整理日期；`published_at` 是节目原始发布日期，必须与单期元信息一致（元信息无日期时省略该字段）；`transcribed_at` 是逐字稿获取日期，来自私有归档 manifest 的 `retrieved_at`，只公开日期本身；`model` 记录实际生成该篇精编的处理模型。四者不得混为一谈。

正文 H1 下方紧跟一个元信息引用块（四段，以空 `>` 行分隔；站点样式表把它渲染为浅底信息卡）：

```text
> 节目发布：YYYY-MM-DD · 逐字稿获取：YYYY-MM-DD · 笔记整理：YYYY-MM-DD
>
> 全文 N 字 · 预计阅读 M 分钟 · 处理模型：<模型>
>
> 标签：[标签](/tags/标签/) [标签](/tags/标签/)
>
> AI 编辑整理，请以原始节目为准。
```

三个日期必须与 frontmatter 对应字段一致；`处理模型` 必须与 frontmatter `model` 一致；N 为正文字符数（按确定性规则：去除元信息引用块固定行、链接 URL 和空白后计数，代码块计入），M = max(1, ceil(N/400))。`check.py` 按同一算法复核字数与时长，声明不一致即失败。标签行按 frontmatter `tags` 的顺序列出，每项链接到 `/tags/<标签>/`（链接目标中的空格写作 `%20`，校验按解码后比较）。演示文章不要求元信息引用块、标签行与 model。

正文采用“速读 → 主题正文 → 来源与定位”的结构。来源与定位的 `- 定位：` 是列表，一个时间点或可搜索短语一行，与文章核心断言一一对应；不允许把全部定位挤成一行。关键证据直接放在文章对应段落或文末，不额外建设 evidence 数据库。完整逐字稿不复制到公开文章或 Git 仓库。

### 3.5 人工编辑内容

`wechat-draft.md`、`video-script.md` 等只属于本地编辑资产，不能被机器任务直接视为“可发布”。机器可以生成初稿，但必须经过人工：

```text
选题确认 → 对照逐字稿核查 → 重新组织 / 改写 → 人工确认 → 发布
```

首版不为这些草稿新增 GitHub 状态、自动发布器或平台 API。

## 4. 两个 GitHub 工作流

### 4.1 collect.yml

每天一次 `schedule`，另保留 `workflow_dispatch` 手动运行。执行顺序：

```text
拉取 main → 安装采集依赖 → 读取来源 → 保存新增元信息
→ 输出采集摘要 → 有变化才提交并推送 main
```

摘要包括各来源是否成功、本次新增、过滤数量和当前待处理数量，写到 Actions 运行摘要，不向飞书等外部渠道发送消息。

使用内置 `GITHUB_TOKEN`，权限只需 `contents: write`。同类采集任务串行执行。单一来源请求失败时记录原因并继续其他来源；所有启用来源都失败时工作流报错，不能把它报告为“今日没有更新”。

只新增元信息的提交不需要更新阅读站点。`GITHUB_TOKEN` 的普通 push 不会再触发另一个 push 工作流，本设计不依赖它触发部署。[G1]

### 4.2 deploy.yml

通过本地正常 Git 身份推送 `main` 时触发，另支持在 Actions 页面手动运行。初版不必配置复杂路径过滤。

```text
拉取代码和文章 → 安装依赖 → 检查文章 → 生成文章列表
→ 构建 VitePress → 上传一个 Pages artifact → 部署
```

沿用 VitePress 官方 Pages 工作流的基本结构；权限为 `contents: read`、`pages: write`、`id-token: write`，部署任务串行。产物目录为 `site/.vitepress/dist`，仓库 Pages 发布源设为 GitHub Actions。[V1]

如果使用项目站点路径，正确配置 `base: '/仓库名/'`；自定义域名或根站点按实际路径配置。[V1]

部署失败时，文章提交和 `processed` 状态不回滚。修复后手动重跑部署即可。没有实际看到部署成功，不把“已推送”报告成“已上线”。

## 5. 本地闲时任务

本项目只提供操作文档和小脚本，由 ZCode 执行，不再开发 Agent runtime、模型路由或自动调度器。闲时任务的可用性和设备要求以宿主为准，不把当前免费政策写成永久系统承诺。[Z1]

每批初始上限为最多 3 篇文章、最多 1 次新 ASR，新增 ASR 音频总时长不超过 120 分钟；优先复用本地已有可用材料。`pending.py --limit 10` 只是候选窗口，不是处理配额。预算不足的条目保持 `pending`，并在批次报告说明原因；只有明确不相关或不值得处理才标记 `ignored`。不做评分系统，积压按当前顺序处理。

新 ASR 必须在转写前通过 `asr-reserve` Compose 服务预约：传入稳定 `batch_id`、item 和媒体探测得到的实际时长。预约写入私有 `local-library/.batches/<batch_id>/asr.json`，使用原子目录创建阻止同一批第二期 ASR；归档时再比较预约、RSS 时长和 Video Agent Kit JSON 的 `audio_duration_seconds`。带时间戳材料由归档器自动检查 cue 顺序、首尾覆盖和最大内部空洞，并把统计写入私有 manifest；人工确认不能替代这些确定性检查。

ZCode 在本地处理链中的职责：

```text
pending item
   ↓
检查期次身份与完整可用性
   ↓
获取完整官方 / RSS transcript
   ├─ 可用 → 保存并继续
   └─ 不完整 / 不可用 → 若允许且预算足够，下载音频并 ASR
                         ├─ 可用 → 保存并继续
                         └─ 不可用 / 预算不足 → failed 或 pending，写明原因
   ↓
写入 local-library/ 长期逐字稿
   ↓
必要时回听 ASR 疑点，再清理临时音频
   ↓
GLM 阅读 / 精编
   ↓
GitHub Machine Digest
```

一次任务的操作顺序：

1. 确认工作区没有不相关改动，拉取 `main`，执行 `pending.py --limit 10` 取得候选，但按本批预算选定不超过 3 篇文章和 1 次新 ASR；未知音频长度时先建立实际时长，若无法在预算内确定则延期为 `pending` 并报告。
2. 先核对期次身份并获取完整官方 / RSS transcript；检查其不是摘要、没有明显截断且可读，在有时长和时间戳时检查覆盖。无法取得完整可用稿时，才在允许且预算足够时使用 ASR，并对 ASR 做同样检查。
3. 完整可用材料失败则标记 `failed` 并写原因；预算跳过则保留 `pending`；不得从部分材料生成整期总结。通过检查后，将完整逐字稿及实际存在的时间戳 / speaker 信息写入 `local-library/`，并写最小 `metadata.yaml`。
4. 长文本按章节或片段阅读后再合并笔记，不只读开头；文章以信息雷达为主，帮助决定复听，通常提炼 3–5 个关键主题但不把数量当硬门槛，保留证据、限制、条件和不确定性。1000–3000 字只是指导范围，不是发布门槛。
5. 对 ASR 中不确定的术语、数字和关键因果回听；只有逐字稿已保存、可用性通过且所需疑点已解决，才可清理 `.cache/` 音频。音频清理不得提前发生。
6. 逐期保存结果。文章和对应基本检查通过后标为 `processed`；不相关标为 `ignored`；完整材料不可用或执行失败标为 `failed`；预算延期标为 `pending` 并写原因。
7. 如生成公众号稿或视频脚本，只保存为本地草稿并明确 `needs_human_review` 语义，不执行自动发布。
8. 执行本地检查和站点构建，提交本次 GitHub 文件；同步远端新增提交，检查无误后推送 `main`。

发布前有两个互补门：确定性的 `check.py` 检查 metadata/status/body/link 格式、禁止可执行 Markdown 内容，以及不应被提交或暂存的文件；ZCode 另行复核核心观点、数字、因果、建议、条件、不确定性、归因和真实来源定位，并将补充解释标为补充内容而非来源原话。删除无法验证的外围断言；核心断言无法解决时不发布，标记失败并记录原因。`processed` 仅表示材料可用且内容 / 基本检查完成，不表示部署成功或独立事实认证。

首版只支持一个本地编辑任务。单条失败可以继续下一条；Git 冲突、权限问题或站点构建失败时停止发布，保留本地产物，不做无限重试和强制推送。

采集与本地编辑可能同时发生：提交前后使用正常 Git 同步流程。工作区干净时可以 `pull --rebase`；出现冲突就停止并交由用户处理。采集器不改已有条目，已足以降低首版冲突概率，不再建设锁服务。

完整转录不因“中文改写”而公开。没有可用 transcript 且 Video Agent Kit 转写失败时，记录 `failed`，不根据标题和简介生成文章。

## 6. 网站实现

VitePress 按 Markdown 文件生成页面；使用默认导航、页面目录、`home` 布局和阅读样式，不制作自定义主题组件。[V2]

首页 `site/index.md` 由 `build-index.mjs` 生成：精编数、待处理数、覆盖节目和收录总时长等统计在构建时从 `data/items` 与文章现算；节目卡按精编数排序，无精编的节目显示收录情况；横幅图自动探测 `site/public/banner.*`（png/jpg/jpeg/webp/avif/svg），存在时写入 `hero.image`。首页统计是最近一次构建的快照，随文章更新同批生效。首页与文章列表、标签页、节目页、侧边栏一样都是派生产物，不提交 Git，不由 Agent 手工维护。

`build-index.mjs` 在构建前递归扫描 `site/posts/`（含 `<source_id>/<year>/` 子目录）的 frontmatter，按整理日期生成 `site/posts/index.md`。`site/tags/index.md` 是标签总览页：一行一个标签、附文章数，按文章数排序；同时为每个标签生成 `site/tags/<标签>/index.md`，列出该标签下的文章，与文章页元信息块中的标签行互链。它同时为每个有已发布文章的来源生成节目页 `site/posts/<source_id>/index.md`（按年份分组、整理日期倒序），并把侧边栏配置写入 `site/.vitepress/sidebar.data.json`：导航组（全部文章、标签）加节目组（按文章数排序），由 `config.mts` 导入并应用到 `/posts/` 与 `/tags/` 路径。节目页、文章列表、标签页与侧边栏都是可重复生成的派生产物，不提交 Git，不由 Agent 手工维护。

搜索直接启用 `themeConfig.search.provider: 'local'`，使用 VitePress 自带能力，不引入 Pagefind、外部搜索服务或向量库。[V3]

约定三个 npm 入口：`site:dev`、`site:build`、`site:preview`。前两个先生成文章列表，`site:build` 再执行 `vitepress build site`。初版只需默认主题下的标题/正文检索，不扩展中文搜索算法工程。

## 7. 只保留必要检查

`check.py` 只做确定性检查：metadata/status/body/link 格式、文章与 `item_id` 对应关系、来源链接、真实 Markdown 标题结构、禁止可执行 Markdown 内容、公开数据与文章目录必须使用 `<source_id>/<year>/<item_id>` 分片布局（文章仅演示页可直接位于 `site/posts/` 根目录），以及任何层级不应提交或暂存的私有文件。它不证明观点准确。ZCode 在标记 `processed` 前还须对照完整本地逐字稿，复核核心观点、数字、因果、建议、条件、不确定性、归因和真实定位；补充解释要明确标为补充内容而非来源原话。无法验证的外围断言应删除；未解决的核心断言不得发布，标记 `failed` 并记录原因。

本地处理额外做两个前置检查：正式文章生成前确认本期存在完整且通过可用性检查的官方 transcript 或 ASR 逐字稿资产；音频清理前确认逐字稿已保存、检查已通过、需要回听的疑点已解决。检查不进入 GitHub CI，因为 CI 不应依赖本地私有资产。`processed` 只表示可用材料和内容 / 基本检查完成，不表示已部署，也不是独立事实认证。

文章只允许普通 Markdown 与规定的 frontmatter，不允许引入脚本、Vue 组件或可执行页面配置；引用材料里的模板表达式应作为字面文本转义。VitePress 支持在 Markdown 内使用 Vue，不能把任意抓取内容直接当可信页面编译。[V4]

外部 RSS、网页和转录只当材料，不能当操作指令。内容任务不得擅自修改工作流、依赖或凭据。网络请求设置超时和有限重试，只访问允许的公开 HTTP(S) 来源，不绕过访问限制。

## 8. 参考项目的吸收原则

参考项目用于减少重复造轮子，但不改变“单仓库 + Actions 轻采集 + ZCode 本地重处理”的核心边界。

当前优先吸收的设计思想：

- `cast2md` / `Podsidian`：Transcript-first，ASR 作为 fallback；
- `Podsidian`：转写与 Markdown 模板化、本地材料保留；
- `AI Daily News`：采集、处理、生成、发布的简单分层；
- `Radiofeed`：RSS 条件请求、ETag / Last-Modified 等轻量采集优化；
- `rec-sys-daily`：来源配置、RSS 清理、确定性过滤和发布分离。

不照搬数据库、向量库、复杂队列、Docker 多服务、自动跨平台发布等结构。

## 9. 参考依据

核查日期：2026-09-11；参考仓库为核查时的 `main`，未运行其代码。

- [RSS1] [Podcast RSS源清单](podcast-sources.md)
- [R1] [rec-sys-daily README 与来源配置](https://github.com/Bin-Zhang-hhht/rec-sys-daily)
- [R2] [rec-sys-daily / collect.py](https://github.com/Bin-Zhang-hhht/rec-sys-daily/blob/main/pipeline/recsys_daily/collect.py)
- [R3] [rec-sys-daily / filtering.py](https://github.com/Bin-Zhang-hhht/rec-sys-daily/blob/main/pipeline/recsys_daily/filtering.py)
- [R4] [rec-sys-daily / site-only.yml](https://github.com/Bin-Zhang-hhht/rec-sys-daily/blob/main/.github/workflows/site-only.yml)
- [V1] [VitePress：部署与 GitHub Pages](https://vitepress.dev/guide/deploy)
- [V2] [VitePress：文件路由](https://vitepress.dev/guide/routing)
- [V3] [VitePress：内置本地搜索](https://vitepress.dev/reference/default-theme-search)
- [V4] [VitePress：在 Markdown 中使用 Vue](https://vitepress.dev/guide/using-vue)
- [G1] [GitHub：工作流触发与 GITHUB_TOKEN](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [Z1] [ZCode：闲时任务](https://zcode.z.ai/en/docs/idle-time-tasks)
