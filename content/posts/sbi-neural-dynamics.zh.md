---
title: "当 90% 可信区间只覆盖 55%"
date: 2026-08-03
slug: sbi-neural-dynamics
translationKey: sbi-neural-dynamics
layout: sbi-essay
heroKicker: "NEURAL DYNAMICS · SBI · FIELD NOTE 02"
heroDeck: "仿真推断可以在给定模型内给出漂亮的后验；但当真实神经系统包含模型没有的动力学时，这个后验还代表机制层面的可信度吗？"
heroFigureLabel: "名义 90% 的可信区间在结构失配条件下实际只覆盖 55%"
nominalLabel: "名义可信度"
observedLabel: "实际科学覆盖率"
recommendedReading: "推荐阅读 24 分钟"
thesis: "模型内校准回答的是推断器有没有学对模拟器；科学覆盖率回答的才是这个区间能不能覆盖真实生成系统中的机制参数。二者不能互换。"
tags: ["SBI", "神经动力学", "贝叶斯推断", "模型失配", "Epileptor"]
categories: ["研究笔记"]
description: "从 90% 可信区间实际只覆盖 55% 出发，讨论 simulation-based inference 在神经动力学中的结构失配、科学覆盖率与可能的结构适配路线。"
showToc: true
tocopen: true
hideMeta: true
disableShare: false
---

在许多神经科学问题中，我们能够写出一个候选动力学模型，也能够在给定参数后模拟 EEG、SEEG、fMRI 或神经元活动，却很难直接计算“这组观测在给定参数下出现的概率”。**仿真推断**（simulation-based inference, SBI）正是为这类问题设计的。

它提供了一条连接机制模型与数据分析的路径：研究者写出模拟器和参数先验，机器学习模型从大量模拟数据中学习如何由观测反推出参数后验。这套思路很有吸引力。真正困难的地方在于，神经数据来自一个高维、非线性、多时间尺度的系统，而用于推断的模拟器通常只保留其中很小一部分结构。

一个在自身模拟数据上表现良好的后验，到了真实系统或更完整的生成模型中，仍可能给出过窄、偏移并且缺少科学覆盖率的参数区间。

## 1. 神经参数反演中的结构失配

给定模拟器 {{< mi >}}M{{< /mi >}}，标准 SBI 从参数先验中采样：

{{< math >}}
\theta \sim p(\theta),
\qquad
x \sim p_M(x\mid\theta),
{{< /math >}}

并训练一个神经后验估计器：

{{< math >}}
q_\psi(\theta\mid x) \approx p_M(\theta\mid x).
{{< /math >}}

NPE、NLE、NRE，以及基于 flow matching 或 diffusion 的方法，都可以放在这个框架下理解。它们分别学习后验、似然、似然比，或用更灵活的生成模型表示后验分布。SBI 已被用于从膜电位、群体活动和行为数据中估计生物物理模型参数，也被视为连接机制建模与统计学习的重要工具。[相关综述与方法背景](https://www.pnas.org/doi/10.1073/pnas.1912789117)。

然而，真实反演问题通常包含两套不同的生成过程：

{{< math >}}
\phi \xrightarrow{G} z(t) \xrightarrow{O_G} y,
{{< /math >}}

{{< math >}}
\theta \xrightarrow{M} \widetilde z(t) \xrightarrow{O_M} x.
{{< /math >}}

这里，{{< mi >}}G{{< /mi >}} 表示真实系统或更完整的生成器，{{< mi >}}\phi{{< /mi >}} 是其中的机制参数，{{< mi >}}z(t){{< /mi >}} 是不可直接观测的潜在动力学，{{< mi >}}O_G{{< /mi >}} 表示真实测量过程。用于反演的模型 {{< mi >}}M{{< /mi >}} 往往更低维、更快，也更容易训练；它拥有自己的参数 {{< mi >}}\theta{{< /mi >}}、状态 {{< mi >}}\widetilde z(t){{< /mi >}} 和观测算子 {{< mi >}}O_M{{< /mi >}}。

标准 SBI 最终给出的是

{{< math >}}
p_M(\theta\mid y),
{{< /math >}}

而科学问题通常关心

{{< math >}}
p_G\!\left(g(\phi)\mid y\right),
{{< /math >}}

其中 {{< mi >}}g(\phi){{< /mi >}} 可以是兴奋性、慢恢复时间尺度、有效连接强度、分岔控制参数，或其他希望在不同模型之间保持共同含义的机制量。只有当模型结构、参数语义和观测过程足够一致时，这两个后验才能被直接联系起来。

### 为什么神经数据尤其容易出现这一问题

神经系统中的参数退化非常常见。差异很大的离子通道密度、突触权重和连接组合，可以产生相似的放电模式或网络节律。经典神经回路研究已经展示，多组相距很远的参数能够生成近乎相同的功能输出。[深度密度估计在神经模型参数识别中的工作](https://elifesciences.org/articles/56261)也清楚呈现了这种多解性。

有限观测进一步扩大了这种多对一关系。即使现代记录技术可以同时记录大量神经元，它们仍只覆盖真实神经回路的一小部分。近期研究表明，只观察部分神经元时，一个经过数据约束的替代网络可以很好地复现已观测单元的动力学，却形成虚假的吸引子结构，并对底层机制给出错误解释。[Qian 等人的 NeurIPS 2024 研究](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7caf9d251b546bc78078b35b4a6f3b7e-Abstract-Conference.html)正是这一风险的直接例子。

EEG、SEEG、MEG 和 fMRI 还包含各自的观测变换。头皮 EEG 经过体积传导形成空间混合信号；SEEG 只覆盖稀疏且由临床选择的局部区域；fMRI 通过缓慢、区域依赖的神经血管耦合观察神经活动。模拟器与数据之间的差异因此可能同时来自动力学结构、空间尺度、时间尺度和传感器模型。

> 当拟合模型缺失真实系统中的一部分动力学时，剩余参数会怎样吸收这些缺失机制的影响？模型报告的不确定性，是否仍然覆盖我们真正关心的机制量？

## 2. 现有 SBI 方法究竟适配了什么

可以把完整推断过程拆成几个数学对象：

{{< math >}}
\theta \xrightarrow{M} x
\xrightarrow{p_\delta(y\mid x)} y,
\qquad
q_\psi(\theta\mid y).
{{< /math >}}

这里既包含动力学模拟器 {{< mi >}}M{{< /mi >}}，也包含模拟观测到真实观测之间的误差通道 {{< mi >}}p_\delta{{< /mi >}}，还包含最终的后验估计器 {{< mi >}}q_\psi{{< /mi >}}。现有方法的差别，很大程度上来自它们选择修改哪一部分。

| 适配层级 | 被修改的对象 | 典型形式 | 代表方法 | 额外信息 |
|---|---|---|---|---|
| 模型内后验估计 | {{< mi >}}q_\psi{{< /mi >}} | {{< mi >}}q_\psi(\theta\mid x)\approx p_M(\theta\mid x){{< /mi >}} | NPE、NLE、NRE、FMPE | 模拟器生成的参数—观测样本 |
| 观测误差适配 | {{< mi >}}p_\delta(y\mid x){{< /mi >}} | {{< mi >}}\int p_\delta(y\mid x)p_M(x\mid\theta)\,dx{{< /mi >}} | RNPE、robust SNL、RVNP | discrepancy 假设或未配对真实数据 |
| 推断目标适配 | summary 或 cost | {{< mi >}}\pi_C\propto e^{-\lambda C}p(\theta){{< /mi >}} | robust statistics、GBI-ACE | 稳健统计量或科学代价 |
| 目标域校正 | 域映射 {{< mi >}}\mathcal T{{< /mi >}} | {{< mi >}}q_{\rm target}=\mathcal T(q_M){{< /mi >}} | RoPE、FRISBI、FMCPE | 少量带参数标签的真实或高保真数据 |
| 模型结构适配 | 模型身份 {{< mi >}}m{{< /mi >}} | {{< mi >}}p(m,\theta_m\mid y){{< /mi >}} | multi-fidelity SBI、模型集合 | 候选模拟器或高保真预算 |

### 2.1 在给定模拟器中学习和校验后验

NPE、NLE 和 NRE 关注同一个核心目标：在给定模型 {{< mi >}}M{{< /mi >}} 的条件下，尽可能准确地恢复其后验。FMPE 使用连续 normalizing flow 和 flow matching 表示条件后验，提高复杂数据和高维参数下的扩展能力。[FMPE 原文](https://arxiv.org/abs/2305.17161)对这一点有完整描述。

SBC 和 TARP 属于这一层的校验工具。SBC 从同一个模型联合分布中反复采样

{{< math >}}
\theta^{(i)}\sim p(\theta),
\qquad
x^{(i)}\sim p_M(x\mid\theta^{(i)}),
{{< /math >}}

再检查生成参数在后验样本中的 rank 是否符合理论分布。TARP 则利用随机参考点估计生成式后验的 coverage。它们检验的是

{{< math >}}
q_\psi(\theta\mid x) \approx p_M(\theta\mid x).
{{< /math >}}

训练数据、测试数据和校准真值均来自同一个模拟器。模型结构改变后，需要另行定义跨模型的科学覆盖检验。换句话说，[SBC](https://arxiv.org/abs/1804.06788) 能证明推断算法是否忠实于模型，却不能独自证明模型是否忠实于真实系统。

### 2.2 把模拟—真实差异写进观测模型

RNPE 在模拟观测和真实观测之间引入显式 discrepancy model。一个简化形式是

{{< math >}}
x\sim p_M(x\mid\theta),
\qquad
y=x+\delta+\epsilon,
{{< /math >}}

此时

{{< math >}}
p(y\mid\theta)
=\int p_\delta(y\mid x)p_M(x\mid\theta)\,dx.
{{< /math >}}

Robust SNL 使用额外调整参数识别模型无法复现的 summary；RVNP 则通过变分推断和数据驱动误差模型学习 simulation-to-reality gap。这类方法能够处理污染、异常值、额外测量噪声以及部分 summary incompatibility。[RNPE 的研究](https://proceedings.neurips.cc/paper_files/paper/2022/hash/db0eac6747e3631eb91095cd76065611-Abstract-Conference.html)展示了这一思路。

这种适配主要发生在观测空间。真实系统中的缺失机制若已经被模型参数吸收，模拟数据与真实数据之间可能只剩下很小的可见残差。此时，discrepancy model 很难仅根据观测差异判断变化来自真实参数，还是来自模型中被省略的状态变量。

### 2.3 改变模型需要解释的数据特征

另一类方法重新选择推断所依据的信息。Robust-statistics SBI 会学习或选择对模型失配较稳定的 summary {{< mi >}}s_\omega(y){{< /mi >}}，并惩罚那些显著放大模拟—真实差异的统计量。[相关 NeurIPS 2023 工作](https://proceedings.neurips.cc/paper_files/paper/2023/hash/16c5b4102a6b6eb061e502ce6736ad8a-Abstract-Conference.html)沿着这一路线展开。

Generalized Bayesian inference 则把原始似然替换为科学代价：

{{< math >}}
\pi_C(\theta\mid y)
\propto
\exp\!\left[-\lambda C\!\left(M(\theta),y\right)\right]p(\theta).
{{< /math >}}

GBI-ACE 使用神经网络摊销估计这一代价，从而降低反复运行模拟器的成本。[GBI-ACE](https://proceedings.neurips.cc/paper_files/paper/2023/hash/fdd565f63f49776bef620e0ce368a492-Abstract-Conference.html)允许研究者把关注点放在传播方向、频谱、发作持续时间或决策损失等目标上。

相应的后验由所选 summary 或 cost 定义：

{{< math >}}
\theta_C^\dagger
=
\arg\min_\theta
\mathbb E\!\left[C\!\left(M(\theta),y\right)\right].
{{< /math >}}

因此，summary-level robustness、预测稳定性与机制参数恢复需要分别验证。被 summary 忽略的失配信息中，也可能恰好包含区分机制参数所需的信息。

### 2.4 用真实域或高保真标签校正后验

RoPE、FRISBI 和 FMCPE 向训练过程加入了新的科学信息：少量真实或高保真参数—观测对。RoPE 使用校准集

{{< math >}}
\mathcal D_{\rm cal}
=\left\{(\theta_j,y_j)\right\}_{j=1}^{N_{\rm cal}},
{{< /math >}}

并通过最优传输学习模拟域与真实域之间的映射。FRISBI 将这一过程扩展为可摊销的 inductive domain transfer，同时利用配对校准数据和未配对真实样本。[FRISBI 论文](https://proceedings.mlr.press/v267/wehenkel25a.html)详细讨论了这一设置。

FMCPE 先在大量模拟数据上训练普通 posterior estimator，再使用 flow matching 将其输出运输到由少量目标域校准样本支持的后验。这里需要区分 FMPE 与 FMCPE：FMPE 改进固定模拟器中的后验表示，FMCPE 使用目标域样本修正已有后验。[FMCPE 预印本](https://arxiv.org/html/2509.23385v5)给出了这一校准框架。

这条路线在能够获得真实参数标签或可信高保真模拟器的场景中很有力量。机器人、受控工程实验和部分物理系统可以直接测量质量、摩擦或材料参数。神经机制参数通常缺少这样的成对真值：我们能收集更多 EEG 或 SEEG，却很难同时获得患者真实的慢恢复常数、神经元兴奋性或微观突触连接强度。

### 2.5 从低保真模型迁移到高保真模型

Multi-fidelity SBI 假设存在一对具有相关结构的模拟器：

{{< math >}}
x_L\sim p_L(x_L\mid\theta_L),
\qquad
x_H\sim p_H(x_H\mid\theta_H).
{{< /math >}}

MF-NPE 先使用大量低成本模拟预训练后验估计器，再用有限高保真模拟进行迁移和修正。[相关工作](https://arxiv.org/html/2502.08416v2)已经在多区室神经元和较大规模脉冲网络上展示模拟效率优势，部分任务所需的高保真模拟量可减少多个数量级。

这种方法估计的是 {{< mi >}}p_H(\theta_H\mid y){{< /mi >}}。它依赖高低保真模型之间存在可迁移表示、可比较观测和一定程度的参数对应关系。高保真模拟器本身仍然需要接受真实数据、跨模态观测与干预响应的检验。

把这些方法放在一起，可以看到一条逐渐增加信息的路径：

{{< math >}}
\text{后验估计}
\rightarrow \text{观测误差适配}
\rightarrow \text{推断目标适配}
\rightarrow \text{目标域校正}
\rightarrow \text{模型结构适配}.
{{< /math >}}

我们的受控实验关注最后一个缺口：当没有真实参数校准集、拟合模型缺失部分动力学，而观测又不足以直接暴露这种结构差异时，模型内部的后验校准能否继续代表机制层面的可靠性。此前对 neural SBI misspecification 的系统研究已经发现，结构或分布失配可能显著破坏后验可靠性，现有缓解策略也没有在所有测试条件中统一消除失败。[相关系统研究](https://arxiv.org/abs/2209.01845)提供了更广泛的证据。

## 3. 当 90% 区间只覆盖了 55%–59%

一个名义 90% 的后验可信区间包含一项可以通过重复实验检验的承诺：如果不断从同一生成过程采样数据并重新推断，真实参数应当大约在 90% 的实验中落入区间，只有约 10% 的实验会漏掉真值。

在我们的受控实验中，RNPE 在 2D fitted simulator 内部取得了接近名义水平的覆盖率：

{{< math >}}
\mathrm{CB}_{\rm int}=0.938.
{{< /math >}}

同一个后验估计器用于解释由 6D Epileptor 生成的数据时，对共享参数 {{< mi >}}x_0{{< /mi >}} 的科学覆盖率下降为

{{< math >}}
\mathrm{CB}_{\mathrm{sci},C3}=0.55,
\qquad
\mathrm{CB}_{\mathrm{sci},C4}=0.59.
{{< /math >}}

将 coverage 改写成“真值落在区间外的概率”，过度自信会更直观：

| 场景 | 区间标注 | 实际覆盖率 | 真值落在区间外 | 相对名义漏覆盖率 |
|---|---:|---:|---:|---:|
| 2D → 2D，RNPE 模型内校准 | 90% | 93.8% | 6.2% | {{< mi >}}0.62\times{{< /mi >}} |
| 6D → 2D，C3 | 90% | 55% | 45% | {{< mi >}}4.5\times{{< /mi >}} |
| 6D → 2D，C4 | 90% | 59% | 41% | {{< mi >}}4.1\times{{< /mi >}} |

这里使用的相对漏覆盖率是

{{< math >}}
R_{\rm miss}
=
\frac{1-\widehat{\mathrm{Coverage}}}{1-0.90}.
{{< /math >}}

一个 90% 区间原本只允许约 10% 的真值落在区间外。在 C3 和 C4 中，实际漏覆盖率达到 45% 和 41%，相当于名义水平的 4.5 倍和 4.1 倍。

**55% 的 coverage 不表示“低维模型保留了 55% 的机制信息”。**它表示在 100 次重复推断中，大约有 45 次生成参数会被排除在一个标注为“90% 可信”的区间之外。即使区间中心与真值仍有相关性，区间宽度所表达的确定程度已经失去原来的解释。

在更基础的 NPE 基准中，这一结构效应更加明显。结构匹配的 2D→2D 条件下，名义 90% 区间的实际覆盖率约为 0.75–0.86；进入 6D→2D 条件后，覆盖率下降到约 0–0.30。RNPE 将科学覆盖提高到 0.55–0.59，说明观测差异建模缓解了一部分失败，但仍留下超过 30 个百分点的 coverage gap：

{{< math >}}
\Delta_{\rm coverage}
=
\widehat{\mathrm{Coverage}}-0.90
=-0.35,\,-0.31.
{{< /math >}}

### 缺失动力学如何进入参数

这一结果可以用一个简单的慢—快系统理解。假设生成系统包含快变量 {{< mi >}}u{{< /mi >}} 和慢变量 {{< mi >}}v{{< /mi >}}：

{{< math >}}
\begin{aligned}
\dot u &= f(u,v;x_0),\\
\tau_v\dot v &= g(u,v),
\end{aligned}
\qquad
y=O[u]+\epsilon.
{{< /math >}}

拟合模型删除了慢变量：

{{< math >}}
\dot u=\widetilde f(u;\widetilde x_0).
{{< /math >}}

慢变量 {{< mi >}}v{{< /mi >}} 对观测的影响依然存在。2D 模型中没有相应状态，因此会通过调整 {{< mi >}}\widetilde x_0{{< /mi >}} 和其他剩余参数来重现这些变化。最终后验容易集中在一个模型投影参数附近：

{{< math >}}
\widetilde x_0^\dagger
=
\arg\min_{\widetilde x_0}
D\!\left(P_G^y, P_{M,\widetilde x_0}^y\right).
{{< /math >}}

直觉上可以写成

{{< math >}}
\widetilde x_0^\dagger
\approx x_0+\Delta_{\rm omitted},
{{< /math >}}

其中 {{< mi >}}\Delta_{\rm omitted}{{< /mi >}} 表示缺失动力学被吸收到参数中的补偿量。

错误指定贝叶斯理论中，后验可以随着数据增加而收缩到模型族内最接近真实分布的 pseudo-true parameter。这个投影点在拟合意义上可以非常稳定，同时与生成系统中的机制参数保持系统偏离。[错误指定条件下的 Bernstein–von Mises 理论](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-6/issue-none/The-Bernstein-Von-Mises-theorem-under-misspecification/10.1214/12-EJS675.short)为这种行为提供了理论背景。

2D 模型能够复现一部分 6D 观测，使结构失配不容易从重建结果中直接暴露。观测相似性、模型内部校准和机制参数覆盖是三项不同要求：

{{< math >}}
\text{observation fit},
\qquad
\mathrm{CB}_{\rm int},
\qquad
\mathrm{CB}_{\rm sci}.
{{< /math >}}

当前结果表明，前两项可以在一定程度上成立，而第三项依然显著欠覆盖：

> 缺失动力学 → 剩余参数补偿 → 狭窄的模型投影后验 → 约四倍于名义水平的漏覆盖。

因此，一个后验区间所标注的“90%”，只在其对应的模型结构和联合分布中成立。结构发生变化后，这个数字必须围绕生成器定义的科学目标重新检验。

## 4. 面向结构适配的四条路线

模型结构进入误差来源以后，推断过程需要容纳更多可能的数据生成机制。近年的工作开始从模型族、多保真模拟、跨尺度观测与主动干预几个方向推进。这些路线仍面临计算和可识别性限制，却为神经 SBI 提供了比单一后验校正更宽的空间。

### 4.1 让模型结构也进入后验

最直接的扩展，是将固定模拟器 {{< mi >}}M{{< /mi >}} 改写为模型族：

{{< math >}}
m\sim p(m),
\qquad
\theta_m\sim p(\theta_m\mid m),
\qquad
y\sim p(y\mid\theta_m,m).
{{< /math >}}

推断对象同时包含模型身份和模型内部参数：

{{< math >}}
p(m,\theta_m\mid y)
\propto
p(y\mid\theta_m,m)p(\theta_m\mid m)p(m).
{{< /math >}}

如果不同模型中的参数可以映射到共同科学目标 {{< mi >}}\phi=g_m(\theta_m){{< /mi >}}，就可以边缘化模型结构：

{{< math >}}
p(\phi\mid y)
=
\sum_m\int
\delta\!\left[\phi-g_m(\theta_m)\right]
p(\theta_m,m\mid y)\,d\theta_m.
{{< /math >}}

在神经动力学中，可以把 2D、5D 和 6D Epileptor 组织成嵌套模型族，也可以同时考虑 neural mass、neural field、spiking network 与多区室神经元模型。每个模型保留不同层级的状态变量、空间分辨率和生物物理细节，共同目标则通过 {{< mi >}}g_m{{< /mi >}} 映射到兴奋性、时间尺度或动力学边界等跨模型量。

Multi-fidelity SBI 已沿这一方向迈出一步。天气和气候领域也长期使用具有不同参数化、分辨率与结构误差的模型集合，并通过多模型数据同化调整各模型对预测的贡献。[多模型 ensemble Kalman filter](https://arxiv.org/abs/2202.02272)提供了一个可借鉴的例子。

模型族还可以从人工定义走向开放式生成。近期工作把可执行机制模型视为粒子，由大语言模型提出和修改候选程序，再按近似边际似然赋权。同期的 program-synthesis SBI 也让语言模型生成候选模拟器，再用 neural ratio estimation 比较模型证据和估计参数后验。[一种概率化 LLM 模型发现框架](https://arxiv.org/html/2602.18266v2)展示了这一方向。NPE-PFN 则尝试用预训练条件密度估计器减少每个候选模拟器重新选网络与调参的成本。[NPE-PFN 预印本](https://arxiv.org/html/2504.17660v2)提供了相应工具。

关键难点仍在模型空间本身。候选集合需要覆盖真正影响科学目标的结构差异；不同模型中的参数需要建立可信的共享语义；边际似然还会受到模型先验、参数先验和程序复杂度的显著影响。对近期神经问题而言，由专家定义、只包含少数关键机制分歧的模型族，可能比完全开放的方程搜索更实际。

### 4.2 让不同尺度的观测彼此校验

不同神经模态可以写成同一潜在系统在不同尺度上的投影：

{{< math >}}
z_{\rm micro}\xrightarrow{C_1}z_{\rm meso}\xrightarrow{C_2}z_{\rm macro},
{{< /math >}}

{{< math >}}
y_k=O_k\!\left[z_{\ell(k)};\eta_k\right]+\epsilon_k.
{{< /math >}}

{{< mi >}}C_1{{< /mi >}} 和 {{< mi >}}C_2{{< /mi >}} 描述微观活动到宏观状态的 coarse-graining，{{< mi >}}O_k{{< /mi >}} 是每种模态独立的观测算子。SEEG、头皮 EEG 和 fMRI 分别观察局部电活动、空间混合电场以及经过神经血管耦合的慢尺度 BOLD 动力学。

已有 multimodal DCM 工作使用共享神经状态方程和模态特异观测模型连接 EEG/MEG 与 fMRI，也有更近期的框架尝试整合部分观测的多尺度神经信号。[神经血管耦合 DCM 的比较研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC7322559/)体现了显式观测模型的重要性。患者特异的 virtual brain twin 则把结构连接、SEEG、头皮 EEG 与刺激诱发活动纳入同一患者模型，用多种来源共同约束致痫网络。[癫痫刺激的 virtual brain twin](https://www.nature.com/articles/s43588-025-00841-6)是近期代表。

对于第 {{< mi >}}k{{< /mi >}} 种观测，可以定义与数据相容的机制集合：

{{< math >}}
\mathcal E_k(y_k)
=
\left\{(\phi,m):
d_k\!\left(O_k[G_m(\phi)],y_k\right)<\varepsilon_k
\right\}.
{{< /math >}}

联合观测保留这些集合的交集：

{{< math >}}
\mathcal E_{\rm joint}=\bigcap_{k=1}^{K}\mathcal E_k(y_k).
{{< /math >}}

不同模态若提供互补约束，这个交集会逐步缩小。一个从 EEG 推断出的参数集合，如果还能预测未参与拟合的 SEEG、fMRI 或刺激响应，其机制解释会获得更强支持。

这类验证尤其适合 held-out modality prediction：

{{< math >}}
p(y_k\mid y_{-k})
=
\sum_m\int
p(y_k\mid\phi,m)p(\phi,m\mid y_{-k})\,d\phi.
{{< /math >}}

模型先利用部分模态推断，再预测另一种未参与拟合的观测。这样的设计能够区分“多模态联合重建得很好”与“同一机制能够跨观测体系泛化”。

跨尺度映射本身也可能成为新的失配来源。把多种特征直接拼接到一个编码器中，容易让 coarse-graining、体积传导和神经血管耦合的误差共同进入潜变量。地震 full-waveform inversion 的 coarse-to-fine 策略提供了一种组织思路：先用低频波形缩小高概率参数区域，再逐步加入更复杂的高频数据并更新 surrogate。[相关顺序式 surrogate 工作](https://academic.oup.com/gji/article/243/2/ggaf349/8248518)可作为方法参考。

### 4.3 用干预打开被动观测看不到的差异

自发活动中，两个机制可能产生近似相同的观测：

{{< math >}}
p(y\mid\phi_1,m_1)\approx p(y\mid\phi_2,m_2).
{{< /math >}}

施加已知干预 {{< mi >}}a{{< /mi >}} 后，它们的响应可能明显分离：

{{< math >}}
p(y^{(a)}\mid\phi_1,m_1,a)
\neq
p(y^{(a)}\mid\phi_2,m_2,a).
{{< /math >}}

干预的价值来自对系统动力学的定向激发。两个模型都可以解释静息功率谱，却可能对刺激后的传播方向、共振频率、恢复时间或发作阈值给出不同预测。

Bayesian experimental design 可以选择最有助于区分参数和模型的实验条件：

{{< math >}}
a^\star
=
\arg\max_a I\!\left((\phi,m);Y\mid a\right).
{{< /math >}}

对于似然不可计算的模拟器，已有方法通过神经互信息估计联合优化实验设计与后验推断。[隐式模型的贝叶斯实验设计](https://proceedings.mlr.press/v119/kleinegesse20a.html)给出了相应框架。

在神经科学中，干预可以来自 SEEG 电刺激、TMS、DBS、药理操控、任务状态以及睡眠—清醒转换。由自发活动反演出的参数集合，需要进一步预测刺激位置变化后传播路径如何重组、输入频率变化后是否出现共振、药物作用后阈值与恢复速度如何改变。

干预本身仍需要 forward model。电场作用于哪些细胞和纤维、药物同时改变哪些通道和突触参数、刺激前后是否能够共享同一模型结构，都需要额外建模。更适合结构适配的目标，是在安全可行的刺激集合中寻找模型分歧最大的条件：

{{< math >}}
a^\star
=
\arg\max_a
D\!\left[p(Y\mid a,m_1),\ldots,p(Y\mid a,m_K)\right].
{{< /math >}}

此时，干预既用于缩小参数后验，也用于排除无法解释新响应的动力学结构。

### 4.4 在证据有限时保留可行区域

模型族、多模态观测和干预数据加入以后，部分机制仍可能无法唯一确定。气候和海洋模型中的 history matching 提供了一种适合这种情况的表达方式：根据观测、模拟器误差和结构误差逐步排除明显不合理的参数区域，保留当前证据尚未排除的部分。

对于模型 {{< mi >}}m{{< /mi >}} 和参数 {{< mi >}}\theta_m{{< /mi >}}，可以定义 implausibility score：

{{< math >}}
I_m(\theta_m)
=
\frac{
\left|s[M_m(\theta_m)]-s(y)\right|
}{
\sqrt{\sigma_{\rm obs}^2+\sigma_{\rm emulator}^2+\sigma_{\rm discrepancy}^2}
}.
{{< /math >}}

随后保留

{{< math >}}
\Theta_{\rm NROY}
=
\left\{(m,\theta_m):I_m(\theta_m)<c\right\},
{{< /math >}}

其中 NROY 表示 *not ruled out yet*。History matching 已用于 NEMO 海洋模型和气候模型调参，通过大型参数 ensemble 与 emulator 逐轮缩小和观测相容的区域，减少只针对有限指标寻找单一最优参数造成的过拟合。[NEMO 的案例](https://gmd.copernicus.org/articles/10/1789/2017/)展示了这一过程。

映射到神经机制问题后，可以进一步报告

{{< math >}}
\Phi_{\rm NROY}(y)
=
\bigcup_{(m,\theta_m)\in\Theta_{\rm NROY}}g_m(\theta_m).
{{< /math >}}

它表示在当前模型族、观测误差和结构误差范围内，仍与数据相容的科学目标区域。随着新模态或干预数据加入，这个区域可以继续收缩。多个合理模型长期给出相近的 {{< mi >}}\phi{{< /mi >}} 时，可以形成稳定的跨模型结论；模型之间持续存在分歧时，这种 model dependence 会直接保留在结果中。

History matching 没有标准后验那样直接的概率解释，阈值、summary 与 discrepancy scale 都需要科学依据。它提供的是一种更合适的报告粒度：哪些机制已经被数据排除，哪些仍然可行，以及当前模型族在哪些问题上还缺少辨识力。

## 结语：可靠的推断应该知道何时停下

神经科学一直在探索如何把数据与机制结合起来。黑盒模型擅长从大规模数据中学习复杂映射，机制模型则把离子通道、突触、连接结构和状态转移写进可检验的动力学方程。SBI 位于这两条路线之间：专家知识进入模拟器、参数先验和实验设计，神经密度估计器则利用大量模拟数据完成传统似然方法难以处理的参数反演。

距离高噪声、稀疏采样、多时间尺度和多空间尺度的真实神经数据，仍然存在几个关键台阶。模型内部后验、观测误差和模型结构需要分别校准；跨模型参数需要共同的科学定义；多模态数据需要显式的跨尺度生成过程；干预数据需要可靠的作用模型。部分观测导致的机制错配已经说明，单纯提高数据拟合能力不能自动解决这些问题。

接下来的发展可能不会来自某一个更大的 posterior network，而会来自一套更完整的推断过程：用模型族表达动力学假设，用高低保真模拟分配计算预算，用跨模态预测和干预响应检验机制，在证据不足时保留可行区域。

真正值得期待的状态很简单：证据一致时，后验能够合理收缩；模型结构仍然含糊时，不确定性会被保留下来；当前数据尚不足以识别某个机制时，推断结果也能诚实地停在这里。

### 延伸阅读

1. Cranmer, Brehmer & Louppe. [The frontier of simulation-based inference](https://www.pnas.org/doi/10.1073/pnas.1912789117). *PNAS*, 2020.
2. Gonçalves et al. [Training deep neural density estimators to identify mechanistic models of neural dynamics](https://elifesciences.org/articles/56261). *eLife*, 2020.
3. Qian et al. [Partial observation can induce mechanistic mismatches in data-constrained models of neural dynamics](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7caf9d251b546bc78078b35b4a6f3b7e-Abstract-Conference.html). *NeurIPS*, 2024.
4. Dax et al. [Flow Matching for Scalable Simulation-Based Inference](https://arxiv.org/abs/2305.17161). *NeurIPS*, 2023.
5. Talts et al. [Validating Bayesian Inference Algorithms with Simulation-Based Calibration](https://arxiv.org/abs/1804.06788), 2018.
6. Ward et al. [Robust Neural Posterior Estimation and Statistical Model Criticism](https://proceedings.neurips.cc/paper_files/paper/2022/hash/db0eac6747e3631eb91095cd76065611-Abstract-Conference.html). *NeurIPS*, 2022.
7. Huang et al. [Learning Robust Statistics for Simulation-based Inference under Model Misspecification](https://proceedings.neurips.cc/paper_files/paper/2023/hash/16c5b4102a6b6eb061e502ce6736ad8a-Abstract-Conference.html). *NeurIPS*, 2023.
8. Gao et al. [Generalized Bayesian Inference for Scientific Simulators via Amortized Cost Estimation](https://proceedings.neurips.cc/paper_files/paper/2023/hash/fdd565f63f49776bef620e0ce368a492-Abstract-Conference.html). *NeurIPS*, 2023.
9. Wehenkel et al. [Addressing Misspecification in Simulation-based Inference through Data-driven Calibration](https://proceedings.mlr.press/v267/wehenkel25a.html). *ICML*, 2025.
10. [Flow Matching Calibration for Simulation-Based Inference under Misspecification](https://arxiv.org/html/2509.23385v5), 2025.
11. [Multifidelity Simulation-based Inference for Computationally Expensive Simulators](https://arxiv.org/html/2502.08416v2), 2025.
12. Cannon et al. [Investigating the Impact of Model Misspecification in Neural Simulation-based Inference](https://arxiv.org/abs/2209.01845), 2022.
13. Kleijn & van der Vaart. [The Bernstein–von Mises theorem under misspecification](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-6/issue-none/The-Bernstein-Von-Mises-theorem-under-misspecification/10.1214/12-EJS675.short). *Electronic Journal of Statistics*, 2012.
14. Bach & Ghil. [A multi-model ensemble Kalman filter for data assimilation and forecasting](https://arxiv.org/abs/2202.02272), 2022.
15. [A Probabilistic Framework for LLM-Based Model Discovery](https://arxiv.org/html/2602.18266v2), 2026.
16. [Effortless, Simulation-Efficient Bayesian Inference using Tabular Foundation Models](https://arxiv.org/html/2504.17660v2), 2025.
17. Jafarian et al. [Comparing dynamic causal models of neurovascular coupling with fMRI and EEG/MEG](https://pmc.ncbi.nlm.nih.gov/articles/PMC7322559/), 2020.
18. Schirner et al. [Virtual brain twins for stimulation in epilepsy](https://www.nature.com/articles/s43588-025-00841-6). *Nature Computational Science*, 2025.
19. [Bayesian full waveform inversion with sequential surrogate updates](https://academic.oup.com/gji/article/243/2/ggaf349/8248518). *Geophysical Journal International*, 2025.
20. Kleinegesse & Gutmann. [Bayesian Experimental Design for Implicit Models by Mutual Information Neural Estimation](https://proceedings.mlr.press/v119/kleinegesse20a.html). *ICML*, 2020.
21. Williamson et al. [History matching for the NEMO ocean model](https://gmd.copernicus.org/articles/10/1789/2017/). *Geoscientific Model Development*, 2017.
