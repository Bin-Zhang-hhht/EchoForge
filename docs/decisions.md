# EchoForge — 产品审查与决策记录

> 版本：v0.8 · 2026-09-11
> 本版记录 M3 的实际实现、审查修复和三篇真实内容本地闭环；个人信息雷达目标、材料可用性、两道发布检查、批次预算、本地备份与 M3 验收边界不变。

## 1. 项目命名决策

正式项目名确定为 **EchoForge**。

- 英文项目名：`EchoForge`
- 中文展示名：`EchoForge · 技术播客`
- 建议 GitHub 仓库名：`echoforge`
- 建议本地项目目录：`echoforge/`

命名含义：`Echo` 对应播客、声音和访谈；`Forge` 对应提炼、重组和再创作。相比包含 `pod` / `cast` 的名称，EchoForge 不把产品锁死在 Podcast，未来可以自然承接访谈录音、视频或其他长内容。

**命名变化不改变当前产品范围。** 首版仍然只做 Podcast RSS、逐字稿资产、机器精编和 VitePress 发布；公众号与视频继续遵守人工发布门。

## 2. 已确定的核心方案

| 事项 | 当前决定 |
| --- | --- |
| 仓库与分支 | 只维护 `main`，按目录区分代码、元信息和公开文章 |
| 发布 | 本地正常 push main → VitePress 构建 → Pages artifact 部署 |
| 提醒 | 暂不做飞书/微信提醒；只看 Actions 摘要或本地待处理列表 |
| 内容来源 | 只做公开 Podcast RSS，不实现 YouTube 模块 |
| RSS 来源管理 | `podcast-sources.md` 保存人工调研的来源池；`config/sources.yaml` 只保存当前实际启用源 |
| 首批 RSS | M2 先启用 Recsperts、Data Skeptic、Latent Space、Practical AI、Software Engineering Daily 共 5 个 |
| 元信息标识 | `item_id` 统一用于 JSON 字段、文件名、文章 frontmatter 和本地资产路径；以 `source_id + ':' + GUID/episode URL` 的 SHA-256 前 12 位生成后缀 |
| 采集规则 | published 优先、updated 后备并统一 UTC；仅收最近 30 天，每源最多 3 条未知日期；关键词不区分大小写子串匹配，排除优先，未知时长不拒绝 |
| 转录策略 | Transcript-first；RSS → Publisher，均需可用性检查；无可用完整稿时在许可和预算内调用 Video Agent Kit ASR |
| 本地逐字稿 | 完整逐字稿是长期资产，放 `local-library/`，不提交 Git，不随缓存清理 |
| 临时音频 | 仅在逐字稿已保存、可用性通过且必需回听疑点解决后删除 |
| GitHub 内容 | Machine Digest，可在本地检查通过后直接发布到 VitePress / Pages |
| 公众号 / 视频 | 机器只能生成草稿；必须人工核查、改写和确认后再发布，不做自动同步 |
| 网站 | VitePress 默认主题 + 内置本地搜索 |
| 测试环境 | 本地与 GitHub Actions 统一使用项目 Dockerfile / Compose 服务，相同镜像阶段、依赖锁和命令；不以宿主 Node/Python 结果作为验收依据 |
| 首版范围 | M1 网站、M2 采集、M3 本地逐字稿与机器摘要三步闭环 |

## 3. 新的核心内容分层

项目不再把“转录”和“文章”看成一次性流水线，而是明确三层：

```text
Source
  完整逐字稿 / 时间戳 / metadata
  → 本地长期保存，不公开

Machine Digest
  GLM 自动精编
  → GitHub Pages，可自动发布

Editorial Content
  微信公众号文章 / 视频脚本
  → 人工选题、核查、重组、改写后发布
```

这意味着逐字稿不是 `.cache/`。缓存可以删除，逐字稿不能因为机器摘要已经生成就被自动清理。

## 4. 为什么保留完整逐字稿

完整逐字稿不仅用于第一次机器总结，还承担后续人工编辑的对照材料作用；ASR 逐字稿不是已核验的原始内容，转写错误仍可能存在：

- 人工核查机器摘要是否丢失上下文、数字或限定条件；
- 微信公众号编辑时回到原始语义，而不是在机器摘要上继续二次转述；
- 视频选题时利用时间戳定位原节目片段；
- 后续重新整理同一期内容时，不必重新转写。

因此本地优先保存 `transcript.md`；如果来源或 Video Agent Kit 实际提供时间戳、speaker、VTT / JSON 等结构化输出，也一并保留。缺失信息不补造。

音频只放 `.cache/`，仅在逐字稿已保存、可用性通过且所有必需回听疑点解决后删除；这样避免删掉仍需核对的唯一音频输入。`local-library/` 用现有私有备份机制保留独立副本，包含逐字稿、节目元信息和编辑备注，首次实际恢复一期节目材料及备注。独立副本防止本地唯一资产丢失，但不引入备份服务。

## 5. 为什么 GitHub 可以机器发布，而公众号 / 视频不能

GitHub Pages 的定位是个人信息雷达：帮助用户判断是否值得收听并理解关键技术观点，不替代完整收听，也不追求覆盖每个话题。文章速读回答“讲了什么、适合谁、有什么价值”；正文通常 3–5 个关键点但不设配额，保留证据、案例、条件、分歧与真实来源定位。1,000～3,000 字只是指导，不是硬门槛。

发布有两道检查：脚本核对元数据、状态、正文、链接格式及禁止的可执行 Markdown 和不应 staged/tracked 的文件；模型复核数字、因果、建议、归属、限定条件、不确定性与来源定位，删除不可验证的外围主张，核心主张无法解决则失败不发布，并标明模型新增解释。自检不是独立事实认证。

公众号和视频代表更强的编辑判断与个人表达，需要额外完成：

```text
是否值得讲
→ 原话和上下文是否准确
→ 哪些观点需要解释
→ 如何重新组织叙事
→ 人工确认最终表述
```

所以 `wechat-draft.md`、`video-script.md` 只能视为机器辅助草稿。当前和未来默认都不允许从 Machine Digest 直接自动同步发布，除非用户以后明确重新修改这一原则。

## 6. Video Agent Kit 的定位

逐字稿采用 Transcript-first：先 RSS，再 Publisher，最后在许可和预算内 ASR。必须验证节目身份、非简介、无明显截断和基本可读性；不设固定字数比例，也不要求广告/音乐转写。官方稿不完整时先尝试补全；ASR 不可用记为失败，预算不足保持 `pending`，不使用部分文本生成整期摘要。未知时长先取得实际时长，无法确认则随批次报告保持 pending。每批最多 3 篇文章、1 期新 ASR，音频总计不超过 120 分钟；已有可用逐字稿复用，`ignored` 仅用于明确无关或不值得处理。

当前不扩展视频抽帧、TTS、时间线编辑或自动视频生成功能。有时间戳和节目时长时对照覆盖范围，但不以固定字数比例判断完整性：节目语速、静音、广告和音乐差异很大；“官方”标签也不能替代材料可用性检查。

批次上限控制初期处理成本，完整材料优先于凑够文章数。允许积压并沿用当前排序，不建设评分或调度器。预算不足不是内容失败，不记为 `failed` 或 `ignored`；`processed` 仅表示材料可用且内容复核与基本检查通过，不代表部署成功或独立事实认证。

也不额外引入 Groq、独立 Whisper 服务等 ASR 依赖。项目利用用户已有的 ZCode / 闲时任务工作方式，减少新增费用和服务配置；但文档不把宿主当前的免费政策写成永久保证。

## 7. RSS 来源选型

本轮继续沿用 v0.4 的来源分层，完整地址见 [Podcast RSS源清单](podcast-sources.md)。

核心来源覆盖：

- 推荐系统：Recsperts、Data Skeptic；
- AI Engineering / Agent：Latent Space、Practical AI、The Cognitive Revolution、Agentic Conversations；
- 软件工程 / 系统：Software Engineering Daily、Software Engineering Radio、Developer Voices、The Changelog。

候选来源包括 No Priors、Oxide and Friends、Gradient Dissent、Dwarkesh Podcast、Interconnects 和 Talk Python To Me。

这里的分层只是人工维护策略，不新增 `source_score`、推荐算法、自动探索器或数据库。首批只启用 5 个 Feed，是为了优先验证采集器，而不是因为其余来源质量不足。

## 8. 参考项目的使用范围

已有调研继续作为实现参考：

- `cast2md`：Transcript-first，ASR fallback；
- `Podsidian`：转录到 Markdown、本地材料和模板化输出；
- `AI Daily News`：Actions 采集、处理、生成、发布的简单组织；
- `Radiofeed`：RSS 抓取稳定性与条件请求；
- `rec-sys-daily`：来源管理、RSS 清理、确定性过滤、独立发布。

只吸收适合当前项目的小设计，不迁移数据库、向量检索、多容器服务、复杂任务队列和自动多平台发布。

## 9. 保留的核心边界

GitHub Actions 的采集阶段只处理元信息；本地人工投放 ZCode 闲时任务；没有真实逐字稿就不生成正式文章。完整逐字稿、音频、人工草稿和凭据不入 Git。

保留少量必要检查，但删除通用 CLI 框架、复杂状态机、专门证据库、缓存生命周期服务和发布事务设计。不是用新名字重新引入旧复杂度。

新增 `local-library/` 只是把“长期资产”和“缓存”语义拆清楚，不建设新的数据库或内容管理系统。

## 10. 未来计划只记录，不展开

AI 配音、AI 动画、“三分钟带你学习……”视频、微信公众号推文仍然是未来方向。允许当前在 `local-library/` 中积累人工草稿，但不为这些方向提前建设自动发布模块、平台 API、状态机或复杂数据结构。

未来启用新渠道时，默认沿用 Human-in-the-loop Publishing Gate：机器生成草稿，人核查后发布。

## 11. M3 实施与审查决定

M3 使用普通脚本和 Compose 服务实现，不增加 Agent runtime 或数据库。`archive_transcript.py` 负责格式转换、人工确认、来源约束、自动时间覆盖和幂等归档；`check.py` 负责公开文章、状态、链接、目录和 Git 私有资产边界。

首次实现审查后作出以下修正：

- 时间戳覆盖不能只信 `--timestamp-coverage passed`。归档器实际解析 VTT/SRT/JSON 的 start/end，拒绝倒序、缺失 end、首尾覆盖不足和超过 10 分钟的内部空洞，并把 cue 数、首尾与最大空洞写入私有 manifest。
- ASR 批次预算不能依赖调用者传入可重置的累计值。转写前由 `asr-reserve` 用媒体探测时长原子预约 `local-library/.batches/<batch_id>/asr.json`；同批第二期在调用模型前失败，归档时再比较预约、RSS 时长和 ASR JSON 实测时长。
- `site/posts/` 和 `data/items/` 只允许直接子文件；文章章节必须是真实独占行 Markdown 标题。私有目录名在 tracked path 的任何层级出现都拒绝。
- Compose 直接命令必须检查当前工作区代码和内容。脚本、配置、测试和站点使用只读挂载，依赖仍来自锁定 Docker 镜像；站点在容器可写层复制当前内容后生成索引。

本地内容批次实际处理三期：Practical AI 官方 VTT、Data Skeptic 唯一一次 Video Agent Kit ASR、Recsperts 官方无时间戳长篇 transcript。三份完整稿均通读；三篇公开精编经过逐项来源复核，Data Skeptic 修正 7 处、Recsperts 修正 5 处后通过，Practical AI 首轮通过。最终共享 Docker 入口构建一篇演示和三篇真实文章，36 项测试、content-check 与 workflow lint 通过；19 个 item 中 3 个 processed、16 个 pending。

这些是本地结果。远端 Pages / Actions、用户私有备份恢复和用户阅读验收尚未观察到，不写成已完成。ASR 音频和中间文件因此继续保留在 `.cache/`，不提前清理。

## 12. 本轮交付

文档文件名继续使用英文，产品、架构、执行与决策规则已同步到 v0.8。M1、M2 本地验证保持有效；M3 的处理基础设施、审查加固、三份私有逐字稿和三篇公开内容已完成本地闭环。没有完整逐字稿、音频、批次预约、人工草稿或凭据进入 Git；未执行的远端及用户侧验收继续明确列为待完成。

## 13. 公开内容按来源与年份分片（v0.9）

M3 验收期间用户提出三点结构要求：根目录太乱、`data/items` 平铺不利于长期存储、站点内容堆在一起不利于检索。逐项决策如下：

- 根目录只做最小整理。删除遗留的 `out/`、`.video_agent/`、`.pytest_cache/` 缓存目录；`package.json`、`requirements.txt` 留在根目录，因为它们是 Dockerfile 与 Compose 的构建输入，移动只会增加构建链路改动而不减少实际杂乱。
- `data/items` 与 `site/posts` 统一按「播客来源 / 发布年份」两层分片：`data/items/<source_id>/<year>/<item_id>.json`、`site/posts/<source_id>/<year>/<item_id>.md`。文件名保持 `<item_id>` 不变，`item_id` 稳定，站点 URL 在 Pages 尚未部署前调整零成本。按来源分是因为播客是长期实体，且与 `local-library/` 已有的组织方式同轴；按年份细分应对单播客长期积累。明确不按状态分目录，状态变化不应移动文件、污染 diff。日期未知的条目存入 `unknown` 目录，保持"未知日期排在最后"的既有语义。
- v0.8 "公开目录只允许直接子文件"的规则由分片布局校验取代：`check.py` 现在强制 `<source_id>/<year>/<item_id>` 精确深度，并校验文章所在分片与元信息的来源、年份一致；演示文章 `demo-vitepress-site.md` 是唯一允许平铺的正式文章。
- 站点检索由 VitePress 本地全文搜索承担，分片不影响它；浏览与发现通过两条增量改进解决：文章 frontmatter 已有的 `tags` 现在生成 `site/tags/index.md` 标签页（构建产物，不提交 Git），导航加入口；文章索引与标签页由 `build-index.mjs` 递归扫描生成。

迁移通过 `git mv` 保留历史，19 个 item 与 3 篇文章全部落在 2026 分片；采集、候选、归档、检查、索引脚本与测试同步更新，collect.yml 的 `git add data/items` 天然覆盖子目录，工作流与 Dockerfile 无需修改。以上均为本地 Docker 验证结果，不涉及远端状态。
