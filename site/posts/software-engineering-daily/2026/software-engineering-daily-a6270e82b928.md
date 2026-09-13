---
item_id: software-engineering-daily-a6270e82b928
title: 'Marimo 的响应式 notebook：从 hidden state 到可复现、可执行、可分享'
date: '2026-09-13'
published_at: '2026-03-10'
transcribed_at: '2026-09-13'
model: 'GLM-5.3 Flash'
source_url: 'https://softwareengineeringdaily.com/podcasts/reinventing-the-python-notebook-with-akshay-agrawal/'
source_name: 'Software Engineering Daily'
input_type: official_transcript
transcript_url: 'https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1905-Marimo.txt'
summary: 'Marimo 创建者 Akshay Agrawal 谈响应式执行模型：静态依赖图取代 hidden state、存储为纯 Python 文件、以及"Claude 很擅长写 Marimo"的意外红利。'
tags: [开发者工具, 编程语言, 开源]
---

# Marimo 的响应式 notebook：从 hidden state 到可复现、可执行、可分享

> 节目：[Software Engineering Daily](/posts/software-engineering-daily/)
>
> 节目发布：2026-03-10 · 逐字稿获取：2026-09-13 · 笔记整理：2026-09-13
>
> 全文共 2960 字 · 阅读约 8 分钟
>
> 标签：[开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) [编程语言](/tags/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80/) [开源](/tags/%E5%BC%80%E6%BA%90/)
>
> 🎧 [收听原节目](https://softwareengineeringdaily.com/podcasts/reinventing-the-python-notebook-with-akshay-agrawal/) · 📄 [查看官方逐字稿](https://softwareengineeringdaily.com/wp-content/uploads/2026/03/SED1905-Marimo.txt)

## 速读

Marimo 创建者 Akshay Agrawal（前 Google Brain、Stanford ML 博士）接受 SED 访谈（主持为 Kevin Ball），讲响应式 Python notebook 的设计。核心是执行模型的取舍：Marimo 选择基于变量定义/引用的静态依赖图（可用纯 Python 忠实实现），放弃基于内存访问的追踪（"不可能 100% 正确"、会陷入 uncanny valley）。

最值得注意的是三条因果链：notebook 存为纯 Python 文件 → "Claude 很擅长写 Marimo"；notebook 可作为脚本执行 → 原型完直接当 cron job 跑；以及有大型上市公司内部部署了数百个 Marimo apps（用户转述）。

## 主题正文

### Jupyter 的三大问题与"带 UI 的 fancy REPL"

Akshay 先承认 Jupyter 在研究与教育中"极其有用"；问题有三。一是 hidden state：Jupyter 默认 IPython kernel 是命令式范式，不知道 cell 之间的关联——他个人经历是删掉某个 cell 后变量仍留在内存里被引用，4 小时后才发现状态不一致。二是软件工程工效：JSON 格式不利于 Git；代码难复用导致他自己曾把同一个 notebook 复制了 40 次。三是分享与交互：协作者必须装好 Python 加 Jupyter 才能改参数——他的博导就做不到。主持人复述并获确认：传统 notebook 本质是"带 UI 的 fancy REPL"；其队友的观点是 REPL 模式只在单人使用时没问题，"甚至是一天后的你自己"就需要可复现性保证。（`00:01:43–00:08:10`）

### Reactive execution：基于变量的静态依赖图

灵感来自 Pluto.jl 与 Observable：运行定义变量 x 的 cell 时自动运行所有读取 x 的 cell。实现机制是无运行时追踪——静态读取每个 cell 的代码、构建依赖图；性能开销"完全可忽略"（Python 内置 AST 模块、C 实现，静态分析只解析一次）。关键的设计取舍（全期最重要的因果断言）：做 Python 响应式 notebook 至少有两条路——基于变量定义/引用（Marimo 的选择，可在 Python 上忠实实现）与基于内存访问（后者无法用纯静态分析可靠实现，"不可能 100% 正确"，会陷入 uncanny valley）。边界声明：Marimo 只跟踪变量定义与引用，mutation 是 escape hatch。有用户形容为 "gentle parenting"。（`00:08:23–00:13:15`）

### 存储为 .py：可复现与可执行

数据流图带来可复现性：用户不可能"跑了这个 cell 忘跑那个 cell"。内置可选的包管理（UV 驱动、PEP 723 标准把包记录在文件顶部注释块）。文件格式：每个 cell 表示为一个函数（用 decorator 标记），命令行 `python my_notebook.py` 即可当脚本执行。他坦承损失：Jupyter 把图表存 Base64 放 GitHub 能立即看到——折中方案是可开启配置自动把 notebook 快照为 .ipynb 存在 `__marimo` 目录。另一损失（打开文件即见上次输出）由自实现 session cache 补救。（`00:13:33–00:17:51`）

复用语法 `from my_notebook import my_function` 直接可用；有后端工程师来信说"用 Marimo notebook 做数据管道，就因为可以这么做"。适用边界（他原话限定）：适合"简单的数据管道"原型——与数据来回对话、可视化检查；原型完可直接 `python myjob.py` 当 cron job 跑。CLI `marimo export html` 可在脚本运行的同时生成 HTML 报告。（`00:18:38–00:23:21`）

### mo.ui 与 Web 应用

mo.ui 机制：UI 元素赋给变量、cell 最后一个表达式输出即显示控件；拖动 slider 会钩入响应式执行系统——"无需回调"。用途分化：有人只用 UI 加速数据探索，有人用它做内部数据 app。匿名案例：某"非常知名的运动队"用 Marimo 做分析应用部署在内部网站；具名案例：Taxwire 全部后端工程师每周使用 Marimo 为税务软件做内部 web app——他明确表示这是没预料到的用例。价值论证：notebook 的价值在于"从随便玩数据 → 发现有用东西 → 暴露给别人"可在同一工具内无缝递进。（`00:23:36–00:28:43`）

### AI/Agent 时代的意外红利

某大型上市公司用户告知：内部部署了数百个 Marimo apps（用户转述）。采纳快的原因是"Claude 很擅长写 Marimo，因为它是纯 Python 文件格式"，且可作脚本运行验证正确性，另有 linter CLI `marimo check`。他的归因（推断性）：Marimo 如今"足够流行、已 in distribution"（进入模型训练分布）。对 AI 变革数据/ML 领域，他明确说"人们还在摸索"，对 text-to-SQL 一类"拭目以待"。（`00:29:26–00:32:03`）

### 语义规则、anywidget 与前沿方向

两条主要语义规则：cell 间不能有环（必须保持 DAG）；不允许跨 cell 重定义同一变量（因系统允许重排 cell）。扩展 API 目前"没有最大的扩展表面"；公开且固定的是文件格式规范。anywidget（既是 spec 也是工具集）被联合创始人早期坚持采用——现在"已成为交互式 notebook 的标准"，`mo.ui.anywidget` 包装后绑定响应式模型；例子：Jupyter Scatter 可高效显示 1000 万个点的散点图。Marimo 团队约 7 人。前沿方向：JupyterHub 兼容进行中、免费托管产品 "Moab" 今年重点投入、headless 驱动 Marimo 配合 agent 的投机项目——"项目的一部分就是搞清楚它是什么"。（`00:36:11–00:45:49`）

## 来源与定位

- 原始节目：[Reinventing the Python Notebook with Akshay Agrawal](https://softwareengineeringdaily.com/podcasts/reinventing-the-python-notebook-with-akshay-agrawal/)
- 定位：官方逐字稿自带 [时:分:秒] 时间戳，以下定位取自归档逐字稿。
  - Jupyter 三大问题与 fancy REPL（00:01:43–00:08:10）
  - 静态依赖图 vs 内存访问追踪的取舍（00:08:23–00:13:15）
  - 存储为 .py 与 session cache（00:13:33–00:17:51）
  - 复用、数据管道与 HTML 报告（00:18:38–00:23:21）
  - mo.ui 与 Web 应用案例（00:23:36–00:28:43）
  - AI 时代的意外红利（00:29:26–00:32:03）
  - 语义规则、anywidget 与前沿方向（00:36:11–00:45:49）

## 整理说明

- 本文基于节目内容与出版方或官方公开逐字稿整理。
- 定位优先采用官方逐字稿中的时间戳；无法可靠获得时间戳的位置使用原文短语。
- "数百个 apps""80%" 等数字均为用户转述（后者受访者自注出处存疑），未独立验证；运动队案例按受访者要求匿名。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
