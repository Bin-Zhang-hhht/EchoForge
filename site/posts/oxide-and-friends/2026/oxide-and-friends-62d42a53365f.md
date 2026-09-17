---
item_id: oxide-and-friends-62d42a53365f
title: 为了一颗电阻：Oxide 停产边缘的五天
date: '2026-09-17'
published_at: '2026-09-16'
transcribed_at: '2026-09-17'
model: 'GLM-5.3 Flash'
source_url: 'https://share.transistor.fm/s/27f44a32'
source_name: 'Oxide and Friends'
input_type: official_transcript
transcript_url: 'https://share.transistor.fm/s/27f44a32/transcription'
summary: 'Oxide 复盘一场几乎停产的缺货危机：时钟缓冲供应商换代撞上 AI 需求洪峰，替代料两度踩坑——8GHz 示波器的探针效应和一个漏掉的字母 K——最终靠 0201 电阻、模板改版与代工厂老手 rework 五天复产。'
tags: [硬件, 供应链]
---

# 为了一颗电阻：Oxide 停产边缘的五天

> 节目：[Oxide and Friends](/podcasts/oxide-and-friends/)
>
> 节目发布：2026-09-16 · 逐字稿获取：2026-09-17 · 笔记整理：2026-09-17
>
> 全文共 4903 字 · 阅读约 13 分钟
>
> 标签：[硬件](/tags/硬件/) [供应链](/tags/供应链/)
>
> 🎧 [收听原节目](https://share.transistor.fm/s/27f44a32) · 📄 [查看官方逐字稿](https://share.transistor.fm/s/27f44a32/transcription)

## 速读

Oxide 复盘一场几乎停产的缺货危机：时钟缓冲供应商换代撞上 AI 需求洪峰，替代料两度踩坑——8GHz 示波器的探针效应和一个漏掉的字母 K——最终靠 0201 电阻、模板改版与代工厂老手 rework 五天复产（`over this like five day period`）。这期适合所有以为「供应链问题只是软件依赖」的工程师：一颗几美元、胡椒粒大小的贴片电阻，就能卡住整条服务器产线；而把它换上去靠的是电气工程师的测量功力、代工厂 rework 技师的手和一套敢在结论未齐时就下单钢网的协作机制。

## 主题正文

### 危机从哪来：产品换代、AI 洪峰与买不到的小零件

运营负责人 Scott Tagwerker 和 CEO Steve Tuck 把起点拨回到一年多以前：给 Oxide 供货电源与时钟两类器件的供应商趁需求低谷推进产品换代，从第九代切到第十代，并向上游晶圆厂发出了切换信号——原厂库存本来只够撑到新产能爬坡（`the AI infrastructure boom like lit them up less than thirty days later`）。结果硬切换完成后不到三十天，AI 基础设施需求爆发，第九代库存被各行业「吸走」，稀缺和市场抢购接踵而至。雪上加霜的是，危机进行中原厂又把 timing 产品线转卖给了新东家，供货节奏和沟通都多了变数（`we've sold the timing business to Cytimes`）。

Oxide 从这家原厂共拿七八颗料：电源侧（power portfolio）四颗、时钟侧三颗。电源侧还能去公开市场「买出一点跑道」，时钟缓冲却怎么都找不到货（`we just weren't finding anything out there for the clock buffer`）。Eric Aasen 补充了行业背景：这类器件被超大规模云厂商和 PC 大厂吸走，分销渠道里根本没有库存；更新一代 3×3 毫米、面向 PCIe Gen 7 低抖动规格的替代品虽然存在，但「买不到的替代品等于没有」（`nothing's in distribution for stuff like this`）。Tuck 的观察更宏观：这些常被忽略的小零件，正在让比 Oxide 大得多的公司削减对客户的供货承诺。

### 一颗 4×4 毫米的芯片有多难换

Robert "RFK" Keith 先科普了这个零件：PCIe 需要 CPU 提供的参考时钟，时钟缓冲把它一分为四，按延迟分级；它没有软件接口、没有可编程性，只有一个使能脚，「你喜欢它就这样」——越简单的器件越没有转圜余地（`the way HCSL, high speed current steering logic`）。替代料筛选的约束一层压一层：首先要封装兼容，因为做转接板极其痛苦，何况这颗料恰好位于风扇之间的死区里，只能放低profile器件；其次板级改版的 lead time 是六个月量级，改设计等于明年这时再说了（`making an interposer board for something like this is painful`，`the lead times on these circuit boards are like six months`）；还要四路输出、每路可独立使能（`is it footprint compatible`）。

Microchip 的一颗料在万分之一的分辨率下几乎完美：封装完全一致，唯一的别扭是旧料上一个「信号丢失指示」引脚（Oxide 根本不用）在新料上是电源引脚。方案是把那儿的一颗 10kΩ 电阻改成 0Ω 直通——一次 BOM 小改（`a loss of signal indicator`，`one ten ks resistor to a zero ohm`）。首波只找到约 3000 颗，随后又有几架的线索，够开工但不够安心。这颗 4×4 毫米、单价几美元的芯片（`four millimeter by four millimeter`，`on the order of like a $3 part`）就这样成了整条产线的命门。

### 两层乌龙：探针效应与一个字母的错料

第一层乌龙藏在测量里。Oxide 的板子按低功耗 HCSL 输出设计——驱动端是一个 0.75V 的电压源，不需要对地下拉端接；而 Microchip 这颗料是上一代 HCSL，14mA 电流源开关必须靠一对约 49.9Ω 的端接电阻才能形成正常摆幅。Eric 上板实测时钟抖动、波形漂亮，因为 8GHz 示波器的输入端接恰好替这颗驱动器补上了那对电阻——教科书级的「探针效应」（`the scope was providing the required termination for this driver chip`，`an eight gigahertz scope`）。等到带 Microchip 料的机器进了产线，症状怪异：无法 net boot、PCIe 能枚举到盘、换上已编程的 M.2 又在不同盘位上相继 panic（`it wouldn't net boot`）。直到 Winona 产线上有人用示波器看到时钟恒为高电平，才想起「HCSL 只会上拉」——缺的就是端接电阻（`the clock just sitting high all the time`）。

第二层乌龙藏在采购描述里。他们需要 49.9Ω 电阻「或接近的值」，巧合的是板上信号过孔与地过孔的间距刚好放得下一颗 0201 封装——Eric 形容那是「四张纸叠四张纸」的尺寸，研坊级的运气（`four sheets of paper by two sheets of paper`）。代工厂库存里没有 49.9Ω，只有 45.3Ω，阻值接近、可以用；rework 技师在显微镜下换了 30 块板。上电——还是不行。全员带着 VNA 和信号源分析仪再赴 Winona，Robert 拿万用表一测：阻值读数 25.6kΩ 量级（`it reads like 25.6 ks`）。追下去发现，发给代工厂的描述抄漏了一个字母 K：电阻不是 45.3Ω，而是 44kΩ，紧挨着的正确型号里 K 明明还在（`one important digit missing in the description`）。等于 900 颗「胡椒粒」白换了。把真正约 45Ω 的电阻换上，板子全部正常；那两块始终点不亮的板子，最后发现是无关的焊锡珠，故障标签都早就挂好了（`first pass yield is above 99%`）。

### 复产与复盘：模板改版、乐观与「Oxide always ships」

让修复真正可量产的是钢网（stencil）改版：把 0201 电阻的焊盘设计进 CAD 发给快转店，两天拿回新钢网，之后这些电阻直接过正常 reflow 工艺，不再需要技师手工贴 900 次（`run this process through normal reflow`，`they got the stencil back in like two days`）。原厂的继任者随后也传来 Q4 供货的消息，但正如 Scott 强调的，这并不能免除替代料验证——没有这条路，产线将面临数周量级的停摆。Bryan 点破硬件生意的残酷之处：产品让人付钱，「但产线一停，营收就是零」（`when the line is down, the revenue is zero`）。

节目没有回避危机中的人为因素。all-hands 上有人引用客户的话说「Oxide always ships」，气氛一度飘向 T 恤周边；第二天晚上，带替代料的板子就点不亮了。Bryan 说「众神盯着那次 all-hands 呢」（`the gods were dialed into that all hands`），Tuck 则自我辩护般复盘了此前十二个月连闯 DDR5、NVMe、IBC 三场缺货、月出货量冲到此前 20 倍的背景，最后收在 Bryan 那句分界线上：「乐观是美德，hubris 是操作系统」。Tuck 补充的价格曲线同样惊人：正常几美元的料先涨到 20–30 美元，一周内 62 美元、再到数百美元，最后的散货要价 700–1000 美元（`it's now $62`）。节目开头 Bryan 还聊到他那篇《The Contagion of Fear》：在 Google AI 把他原创的句子一本正经「考据」成《辛普森一家》台词之后，这期人肉排障恰好成了最佳注脚——AI 能陪你头脑风暴，但让机器真正转起来的，是显微镜下的手、示波器前的眼睛和敢在结论未齐时下单钢网的判断（`humanity in our engineering`）。

## 来源与定位

- 原始节目：[For Want of a Resistor](https://share.transistor.fm/s/27f44a32)
- 定位：官方 transcript 无时间戳，以下为可在全文中搜索的原文短语。
  - 危机起点：供应商第九代切第十代、AI 需求洪峰（`the AI infrastructure boom like lit them up less than thirty days later`）
  - timing 产品线中途转卖（`we've sold the timing business to Cytimes`）
  - 电源侧可买、时钟缓冲无货（`we just weren't finding anything out there for the clock buffer`）
  - 时钟缓冲的作用与 HCSL 输出结构（`the way HCSL, high speed current steering logic`）
  - 替代料约束：封装兼容、转接板之痛、六个月板级周期、分销无货（`is it footprint compatible`；`making an interposer board for something like this is painful`；`the lead times on these circuit boards are like six months`；`nothing's in distribution for stuff like this`）
  - 引脚功能互换与 BOM 小改（`a loss of signal indicator`；`one ten ks resistor to a zero ohm`）
  - 探针效应：8GHz 示波器替驱动器补了端接（`the scope was providing the required termination for this driver chip`；`an eight gigahertz scope`）
  - 产线症状与时钟恒高（`it wouldn't net boot`；`the clock just sitting high all the time`）
  - 0201 尺寸类比与过孔间距的运气（`four sheets of paper by two sheets of paper`）
  - 万用表读数与漏掉的字母 K（`it reads like 25.6 ks`；`one important digit missing in the description`）
  - 修复后的一次性良率与无关失败（`first pass yield is above 99%`）
  - 钢网改版回归正常 reflow（`run this process through normal reflow`；`they got the stencil back in like two days`）
  - all-hands 乐观、五天协作与价格螺旋（`the gods were dialed into that all hands`；`over this like five day period`；`it's now $62`）
  - 产线停摆即营收归零（`when the line is down, the revenue is zero`）

## 整理说明

- 本文基于节目内容与出版方公开的官方转写页整理。
- 出版方转写页的时间标签为非结构化行内标注，归档按无时间戳处理，全部定位使用可搜索原文短语。
- 转写页为机器转写，存在专名噪声：如把博客标题 The Contagion of Fear 转作 "Caucasian of Fear"、把代工缩写 CMs 转作 "Centimeters"、把 HCSL 有时转作 "HSCL"、把 "50 ohms" 转作 "50 homes"。本文对无法确证的公司与型号名一律用角色描述（原厂、新东家、Microchip、代工伙伴 Benchmark Electronics），未采信转写拼写；数字均为对话口径（板数在一百多到八百之间摇摆、25.6kΩ 为板上实测读数、44kΩ 为整卷额定值），本文未独立验证。
- 整理模型：GLM-5.3 Flash
- AI 编辑整理，请以原始节目为准。
