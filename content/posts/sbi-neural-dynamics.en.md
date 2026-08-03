---
title: "Simulation-Based Inference in Neural Dynamics"
date: 2026-08-03
slug: sbi-neural-dynamics
translationKey: sbi-neural-dynamics
math: true
estimatedReadingTime: "24 min"
tags: ["SBI", "Neural Dynamics", "Bayesian Inference", "Model Misspecification", "Epileptor"]
categories: ["Research Notes"]
showToc: true
tocopen: false
hideMeta: false
disableShare: true
ShowBreadCrumbs: false
---

In many neuroscience problems, we can write down a candidate dynamical model and simulate EEG, SEEG, fMRI or neuronal activity for a chosen set of parameters. What we cannot readily evaluate is the probability of those observations under the parameters. **Simulation-based inference** (SBI) was designed for precisely this setting.

SBI offers a bridge between mechanistic modelling and data analysis. The researcher specifies a simulator and parameter prior; a machine-learning model then uses many simulations to learn a posterior over parameters from observations. The appeal is obvious. The difficulty is that neural data come from a high-dimensional, nonlinear and multiscale system, while the simulator used for inference usually preserves only a small part of that structure.

A posterior that performs well on its own simulated data can therefore become too narrow, displaced and scientifically miscalibrated when it meets a real system—or merely a more complete generator.

![Neural parameter inference under model misspecification](/images/neural-parameter-inference-model-misspecification.png "Figure 1. Neural parameter inference under model misspecification. The real neural system and fitted simulator can differ in dynamical structure, observation scale and noise, even when both produce similar measurements.")

## 1. Structural misspecification in neural parameter inversion

Given a simulator {{< mi >}}M{{< /mi >}}, standard SBI samples from a parameter prior,

{{< math >}}
\theta \sim p(\theta),
\qquad
x \sim p_M(x\mid\theta),
{{< /math >}}

and trains a neural posterior estimator,

{{< math >}}
q_\psi(\theta\mid x) \approx p_M(\theta\mid x).
{{< /math >}}

NPE, NLE, NRE and methods based on flow matching or diffusion all fit within this broad framework. They learn a posterior, likelihood or likelihood ratio, or use a flexible generative process to represent the posterior. SBI has already been used to infer biophysical parameters from membrane potentials, population activity and behaviour, and has become an important way to connect mechanistic models with statistical learning. The [PNAS overview of the field](https://www.pnas.org/doi/10.1073/pnas.1912789117) gives a useful introduction.

Real inverse problems, however, usually contain two different generative processes:

{{< math >}}
\phi \xrightarrow{G} z(t) \xrightarrow{O_G} y,
{{< /math >}}

{{< math >}}
\theta \xrightarrow{M} \widetilde z(t) \xrightarrow{O_M} x.
{{< /math >}}

Here, {{< mi >}}G{{< /mi >}} denotes the real system or a more complete generator, {{< mi >}}\phi{{< /mi >}} its mechanistic parameters, {{< mi >}}z(t){{< /mi >}} its latent dynamics and {{< mi >}}O_G{{< /mi >}} the real measurement process. The model used for inversion, {{< mi >}}M{{< /mi >}}, is often lower-dimensional, faster and easier to train. It has its own parameters {{< mi >}}\theta{{< /mi >}}, states {{< mi >}}\widetilde z(t){{< /mi >}} and observation operator {{< mi >}}O_M{{< /mi >}}.

Standard SBI ultimately returns

{{< math >}}
p_M(\theta\mid y),
{{< /math >}}

whereas the scientific question usually concerns

{{< math >}}
p_G\!\left(g(\phi)\mid y\right).
{{< /math >}}

The target {{< mi >}}g(\phi){{< /mi >}} might be excitability, a slow recovery timescale, effective coupling, a bifurcation-control parameter or another mechanistic quantity intended to retain meaning across models. The two posteriors can be connected directly only when model structure, parameter semantics and observation processes are sufficiently aligned.

### Why neural data are especially vulnerable

Parameter degeneracy is common in neural systems. Very different ion-channel densities, synaptic weights and connectivity patterns can produce similar firing patterns or network rhythms. Classic circuit studies have shown that distant regions of parameter space can generate almost indistinguishable functional outputs. Work on [neural density estimation for mechanistic models](https://elifesciences.org/articles/56261) makes this multiplicity particularly visible.

Partial observation expands the many-to-one mapping. Even modern recording systems sample only a small fraction of the neurons in a real circuit. Recent work shows that a data-constrained surrogate network can reproduce the observed units remarkably well while developing spurious attractors and supporting a false account of the underlying mechanism. [Qian and colleagues' NeurIPS 2024 study](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7caf9d251b546bc78078b35b4a6f3b7e-Abstract-Conference.html) provides a direct example.

EEG, SEEG, MEG and fMRI also impose different observation transformations. Scalp EEG is spatially mixed by volume conduction; SEEG samples sparse, clinically selected locations; fMRI observes neural activity through slow and region-dependent neurovascular coupling. A simulation-to-data gap can therefore arise simultaneously from dynamical structure, spatial scale, temporal scale and sensor physics.

> When a fitted model omits part of the real dynamics, how do its remaining parameters absorb the missing mechanism? Does the reported uncertainty still cover the quantity we actually care about?

## 2. What existing SBI methods adapt

The inference pipeline can be separated into several mathematical objects:

{{< math >}}
\theta \xrightarrow{M} x
\xrightarrow{p_\delta(y\mid x)} y,
\qquad
q_\psi(\theta\mid y).
{{< /math >}}

This representation includes the dynamical simulator {{< mi >}}M{{< /mi >}}, a discrepancy channel {{< mi >}}p_\delta{{< /mi >}} between simulated and real observations, and the posterior estimator {{< mi >}}q_\psi{{< /mi >}}. Much of the difference between existing methods follows from which object they modify.

| Adaptation level | Modified object | Typical form | Examples | Additional information |
|---|---|---|---|---|
| Within-model posterior | {{< mi >}}q_\psi{{< /mi >}} | {{< mi >}}q_\psi(\theta\mid x)\approx p_M(\theta\mid x){{< /mi >}} | NPE, NLE, NRE, FMPE | Parameter–observation simulations |
| Observation discrepancy | {{< mi >}}p_\delta(y\mid x){{< /mi >}} | {{< mi >}}\int p_\delta(y\mid x)p_M(x\mid\theta)\,dx{{< /mi >}} | RNPE, robust SNL, RVNP | A discrepancy model or unpaired real data |
| Inference target | Summary or cost | {{< mi >}}\pi_C\propto e^{-\lambda C}p(\theta){{< /mi >}} | Robust statistics, GBI-ACE | Robust summaries or scientific costs |
| Target-domain calibration | Map {{< mi >}}\mathcal T{{< /mi >}} | {{< mi >}}q_{\rm target}=\mathcal T(q_M){{< /mi >}} | RoPE, FRISBI, FMCPE | A few labelled real or high-fidelity pairs |
| Model structure | Model identity {{< mi >}}m{{< /mi >}} | {{< mi >}}p(m,\theta_m\mid y){{< /mi >}} | Multi-fidelity SBI, model ensembles | Candidate simulators or high-fidelity budget |

### 2.1 Learning and validating a posterior for a fixed simulator

NPE, NLE and NRE pursue the same core objective: accurately recover the posterior implied by a given model {{< mi >}}M{{< /mi >}}. FMPE represents the conditional posterior with a continuous normalizing flow learned by flow matching, improving scalability to complex data and high-dimensional parameters. The [FMPE paper](https://arxiv.org/abs/2305.17161) describes this estimator in detail.

Simulation-based calibration (SBC) and TARP operate at this level. SBC repeatedly draws

{{< math >}}
\theta^{(i)}\sim p(\theta),
\qquad
x^{(i)}\sim p_M(x\mid\theta^{(i)}),
{{< /math >}}

then tests whether the generative parameter has the expected rank among posterior samples. TARP uses random reference points to assess the coverage of generative posteriors. Both examine whether

{{< math >}}
q_\psi(\theta\mid x) \approx p_M(\theta\mid x).
{{< /math >}}

The training data, test data and calibration truth all come from the same simulator. Once model structure changes, a separate cross-model target and coverage test are required. [SBC](https://arxiv.org/abs/1804.06788) can tell us whether an algorithm is faithful to its model; on its own, it cannot tell us whether the model is faithful to the real system.

### 2.2 Writing the simulation-to-reality gap into the observation model

RNPE introduces an explicit discrepancy model between simulated and real observations. A simplified formulation is

{{< math >}}
x\sim p_M(x\mid\theta),
\qquad
y=x+\delta+\epsilon,
{{< /math >}}

so that

{{< math >}}
p(y\mid\theta)
=\int p_\delta(y\mid x)p_M(x\mid\theta)\,dx.
{{< /math >}}

Robust SNL uses adjustment parameters to identify summaries that the model cannot reproduce; RVNP uses variational inference and a data-driven error model to learn a simulation-to-reality gap. These approaches can handle contamination, outliers, extra measurement noise and partial summary incompatibility. [RNPE](https://proceedings.neurips.cc/paper_files/paper/2022/hash/db0eac6747e3631eb91095cd76065611-Abstract-Conference.html) is a representative example.

The adaptation remains concentrated in observation space. If omitted dynamics have already been absorbed by fitted parameters, little visible residual may remain between simulated and real observations. A discrepancy model then cannot easily determine whether an observed change came from a true parameter or from a missing state variable.

### 2.3 Changing which features the model must explain

Another family of methods changes the information on which inference is based. Robust-statistics SBI learns or selects summaries {{< mi >}}s_\omega(y){{< /mi >}} that remain stable under misspecification and penalizes statistics that amplify the simulation-to-reality gap. A [NeurIPS 2023 study](https://proceedings.neurips.cc/paper_files/paper/2023/hash/16c5b4102a6b6eb061e502ce6736ad8a-Abstract-Conference.html) develops this approach.

Generalized Bayesian inference replaces the original likelihood with a scientific cost:

{{< math >}}
\pi_C(\theta\mid y)
\propto
\exp\!\left[-\lambda C\!\left(M(\theta),y\right)\right]p(\theta).
{{< /math >}}

GBI-ACE uses a neural network to amortize cost estimation, reducing the need to rerun the simulator for each observation. [GBI-ACE](https://proceedings.neurips.cc/paper_files/paper/2023/hash/fdd565f63f49776bef620e0ce368a492-Abstract-Conference.html) lets researchers focus inference on quantities such as propagation direction, spectra, seizure duration or decision loss.

The corresponding posterior is defined by the selected summary or cost:

{{< math >}}
\theta_C^\dagger
=
\arg\min_\theta
\mathbb E\!\left[C\!\left(M(\theta),y\right)\right].
{{< /math >}}

Summary-level robustness, predictive stability and recovery of mechanistic parameters must therefore be tested separately. The information discarded as misspecified may also contain exactly what is needed to distinguish mechanisms.

### 2.4 Calibrating with target-domain or high-fidelity labels

RoPE, FRISBI and FMCPE add a new kind of scientific information: a small number of real or high-fidelity parameter–observation pairs. RoPE uses a calibration set

{{< math >}}
\mathcal D_{\rm cal}
=\left\{(\theta_j,y_j)\right\}_{j=1}^{N_{\rm cal}}
{{< /math >}}

and optimal transport to learn a mapping from the simulation domain to the target domain. FRISBI extends this idea to amortized inductive domain transfer, combining paired calibration data with unpaired real samples. The [FRISBI paper](https://proceedings.mlr.press/v267/wehenkel25a.html) explains this setting.

FMCPE first trains an ordinary posterior estimator on many simulations, then uses flow matching to transport its output towards a posterior supported by a small target-domain calibration set. FMPE and FMCPE should not be confused: FMPE improves posterior representation for a fixed simulator, whereas FMCPE uses target-domain samples to correct an existing posterior. The [FMCPE preprint](https://arxiv.org/html/2509.23385v5) presents the latter framework.

This route is powerful when real parameter labels or a trusted high-fidelity simulator are available. In robotics, controlled engineering and some physical systems, mass, friction or material properties can be measured directly. Neural mechanism parameters rarely come with such paired truth. We can collect more EEG or SEEG, but usually cannot measure a patient's true slow recovery constant, neuronal excitability or microscopic synaptic coupling at the same time.

### 2.5 Transferring from low- to high-fidelity models

Multi-fidelity SBI assumes a related pair of simulators:

{{< math >}}
x_L\sim p_L(x_L\mid\theta_L),
\qquad
x_H\sim p_H(x_H\mid\theta_H).
{{< /math >}}

MF-NPE pretrains a posterior estimator on many inexpensive low-fidelity simulations, then transfers and corrects it using a limited high-fidelity budget. Recent [multi-fidelity SBI work](https://arxiv.org/html/2502.08416v2) reports substantial efficiency gains for multicompartment neurons and larger spiking networks, with orders-of-magnitude reductions in high-fidelity simulations on some tasks.

The method estimates {{< mi >}}p_H(\theta_H\mid y){{< /mi >}}. It assumes that high- and low-fidelity models admit transferable representations, comparable observations and some parameter correspondence. The high-fidelity simulator must still be tested against real data, cross-modal observations and intervention responses.

Together, these methods form a path of increasing information:

{{< math >}}
\text{posterior estimation}
\rightarrow \text{observation adaptation}
\rightarrow \text{target adaptation}
\rightarrow \text{domain calibration}
\rightarrow \text{structural adaptation}.
{{< /math >}}

Our controlled experiment addresses the final gap. If no real parameter calibration set exists, the fitted model omits part of the dynamics, and observations do not directly expose that structural difference, can within-model calibration still represent mechanistic reliability? Systematic work on [misspecification in neural SBI](https://arxiv.org/abs/2209.01845) has already shown that structural or distributional shifts can severely damage posterior reliability, with no single mitigation succeeding across all test conditions.

## 3. When 90% covers only 55–59%

A nominal 90% posterior credible interval makes a testable repeated-sampling promise. If data are repeatedly drawn from the same generative process and inference is repeated, the true parameter should fall inside the interval in roughly 90% of experiments. Only about 10% should miss.

In our controlled experiment, RNPE achieved near-nominal coverage within the fitted 2D simulator:

{{< math >}}
\mathrm{CB}_{\rm int}=0.938.
{{< /math >}}

When the same posterior estimator interpreted observations generated by a 6D Epileptor, scientific coverage for the shared parameter {{< mi >}}x_0{{< /mi >}} fell to

{{< math >}}
\mathrm{CB}_{\mathrm{sci},C3}=0.55,
\qquad
\mathrm{CB}_{\mathrm{sci},C4}=0.59.
{{< /math >}}

The overconfidence becomes clearer when coverage is restated as the probability that truth lies outside the interval:

| Setting | Interval label | Empirical coverage | Truth outside | Relative miss rate |
|---|---:|---:|---:|---:|
| 2D → 2D, within-model RNPE | 90% | 93.8% | 6.2% | {{< mi >}}0.62\times{{< /mi >}} |
| 6D → 2D, C3 | 90% | 55% | 45% | {{< mi >}}4.5\times{{< /mi >}} |
| 6D → 2D, C4 | 90% | 59% | 41% | {{< mi >}}4.1\times{{< /mi >}} |

The relative miss rate is

{{< math >}}
R_{\rm miss}
=
\frac{1-\widehat{\mathrm{Coverage}}}{1-0.90}.
{{< /math >}}

A 90% interval is supposed to exclude truth in only about 10% of repetitions. In C3 and C4, the miss rates reached 45% and 41%—4.5 and 4.1 times the nominal rate.

**A coverage of 55% does not mean that the reduced model retained 55% of the mechanistic information.** It means that in 100 repeated inferences, roughly 45 generating parameters would be excluded by an interval labelled “90% credible”. The posterior centre may still correlate with truth, but the certainty expressed by its width has lost its original interpretation.

The structural effect is stronger in the basic NPE benchmark. Under matched 2D→2D structure, empirical coverage of nominal 90% intervals was approximately 0.75–0.86; under 6D→2D mismatch it fell to approximately 0–0.30. RNPE improved scientific coverage to 0.55–0.59, showing that observation-discrepancy modelling mitigated part of the failure. It still left a gap of more than 30 percentage points:

{{< math >}}
\Delta_{\rm coverage}
=
\widehat{\mathrm{Coverage}}-0.90
=-0.35,\,-0.31.
{{< /math >}}

### How omitted dynamics enter the parameters

A simple slow–fast system illustrates the mechanism. Suppose the generating system contains a fast variable {{< mi >}}u{{< /mi >}} and a slow variable {{< mi >}}v{{< /mi >}}:

{{< math >}}
\begin{aligned}
\dot u &= f(u,v;x_0),\\
\tau_v\dot v &= g(u,v),
\end{aligned}
\qquad
y=O[u]+\epsilon.
{{< /math >}}

The fitted model removes the slow variable:

{{< math >}}
\dot u=\widetilde f(u;\widetilde x_0).
{{< /math >}}

The influence of {{< mi >}}v{{< /mi >}} remains in the observations. Because the 2D model has no corresponding state, it reproduces those changes by adjusting {{< mi >}}\widetilde x_0{{< /mi >}} and other surviving parameters. Its posterior can then concentrate around a model-projection parameter,

{{< math >}}
\widetilde x_0^\dagger
=
\arg\min_{\widetilde x_0}
D\!\left(P_G^y, P_{M,\widetilde x_0}^y\right),
{{< /math >}}

which can be understood schematically as

{{< math >}}
\widetilde x_0^\dagger
\approx x_0+\Delta_{\rm omitted}.
{{< /math >}}

The term {{< mi >}}\Delta_{\rm omitted}{{< /mi >}} is the compensation absorbed by the parameter for dynamics the model does not contain.

Under Bayesian misspecification, a posterior can contract with increasing data around the pseudo-true parameter closest to the real distribution within the chosen model family. That projection can be extremely stable as a fit while remaining systematically displaced from the generating mechanism. The [Bernstein–von Mises theory under misspecification](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-6/issue-none/The-Bernstein-Von-Mises-theorem-under-misspecification/10.1214/12-EJS675.short) provides the formal background.

The 2D model can reproduce part of the 6D observation, making structural mismatch difficult to see from reconstruction alone. Observation similarity, within-model calibration and mechanistic coverage are three distinct requirements:

{{< math >}}
\text{observation fit},
\qquad
\mathrm{CB}_{\rm int},
\qquad
\mathrm{CB}_{\rm sci}.
{{< /math >}}

Our result shows that the first two can hold to a useful degree while the third remains badly undercovered:

> Omitted dynamics → compensation by remaining parameters → a narrow model-projection posterior → a miss rate about four times the nominal level.

The “90%” printed on a posterior interval is therefore conditional on its model structure and joint distribution. Once structure changes, that number must be retested against a generator-defined scientific target.

## 4. Four routes towards structural adaptation

Once model structure becomes part of the error, inference must accommodate multiple possible data-generating mechanisms. Recent work is beginning to move through model families, multi-fidelity simulation, cross-scale observation and active intervention. These routes still face computational and identifiability limits, but they provide a broader response than correcting a single posterior.

### 4.1 Put model structure into the posterior

The most direct extension replaces a fixed simulator {{< mi >}}M{{< /mi >}} with a family:

{{< math >}}
m\sim p(m),
\qquad
\theta_m\sim p(\theta_m\mid m),
\qquad
y\sim p(y\mid\theta_m,m).
{{< /math >}}

Inference then covers both model identity and within-model parameters:

{{< math >}}
p(m,\theta_m\mid y)
\propto
p(y\mid\theta_m,m)p(\theta_m\mid m)p(m).
{{< /math >}}

If parameters in different models map to a shared scientific target {{< mi >}}\phi=g_m(\theta_m){{< /mi >}}, model structure can be marginalized:

{{< math >}}
p(\phi\mid y)
=
\sum_m\int
\delta\!\left[\phi-g_m(\theta_m)\right]
p(\theta_m,m\mid y)\,d\theta_m.
{{< /math >}}

In neural dynamics, 2D, 5D and 6D Epileptor variants could form a nested family. Neural mass, neural field, spiking-network and multicompartment models could also be compared. Each retains a different level of state, spatial resolution and biophysical detail; {{< mi >}}g_m{{< /mi >}} would map their parameters onto common targets such as excitability, timescale or distance to a dynamical boundary.

Multi-fidelity SBI has taken one step in this direction. Weather and climate science have also long used ensembles with different parameterizations, resolutions and structural errors, dynamically reweighting their predictive contributions. A [multi-model ensemble Kalman filter](https://arxiv.org/abs/2202.02272) offers one relevant example.

Model families may eventually move beyond expert enumeration. Recent work treats executable mechanistic models as particles, uses language models to propose or edit candidate programs, and weights them by approximate marginal likelihood. Program-synthesis SBI similarly generates candidate simulators and uses neural ratio estimation to compare evidence and infer parameters. [A probabilistic framework for LLM-based model discovery](https://arxiv.org/html/2602.18266v2) illustrates this direction. NPE-PFN, meanwhile, uses a pretrained conditional density estimator to reduce the architecture selection and tuning required for each candidate simulator. See the [NPE-PFN preprint](https://arxiv.org/html/2504.17660v2).

The hard problem remains the model space itself. Candidate families must cover structural differences that matter for the scientific target; parameters need defensible shared semantics; and marginal likelihood is sensitive to model priors, parameter priors and program complexity. For near-term neuroscience, an expert-defined family containing a small number of consequential mechanistic alternatives may be more useful than unrestricted equation search.

### 4.2 Make observations at different scales check one another

Neural modalities can be written as projections of the same latent system at different scales:

{{< math >}}
z_{\rm micro}\xrightarrow{C_1}z_{\rm meso}\xrightarrow{C_2}z_{\rm macro},
{{< /math >}}

{{< math >}}
y_k=O_k\!\left[z_{\ell(k)};\eta_k\right]+\epsilon_k.
{{< /math >}}

The maps {{< mi >}}C_1{{< /mi >}} and {{< mi >}}C_2{{< /mi >}} describe coarse-graining from microscopic activity to macroscopic state, while {{< mi >}}O_k{{< /mi >}} is a modality-specific observation operator. SEEG, scalp EEG and fMRI observe local electrical activity, spatially mixed fields and slow BOLD dynamics coupled through neurovascular processes.

Multimodal DCM has used shared neural state equations with modality-specific observation models to connect EEG/MEG and fMRI. Other frameworks are beginning to combine partially observed, multiscale neural signals. A [comparison of DCMs for neurovascular coupling](https://pmc.ncbi.nlm.nih.gov/articles/PMC7322559/) shows why the observation layer must remain explicit. Patient-specific virtual brain twins now combine structural connectivity, SEEG, scalp EEG and stimulation-evoked activity to constrain epileptogenic networks. [Virtual brain twins for epilepsy stimulation](https://www.nature.com/articles/s43588-025-00841-6) are a recent example.

For modality {{< mi >}}k{{< /mi >}}, define the set of mechanisms compatible with its data:

{{< math >}}
\mathcal E_k(y_k)
=
\left\{(\phi,m):
d_k\!\left(O_k[G_m(\phi)],y_k\right)<\varepsilon_k
\right\}.
{{< /math >}}

Joint observation retains the intersection

{{< math >}}
\mathcal E_{\rm joint}=\bigcap_{k=1}^{K}\mathcal E_k(y_k).
{{< /math >}}

If modalities provide complementary constraints, the intersection shrinks. A parameter set inferred from EEG gains stronger mechanistic support if it also predicts SEEG, fMRI or stimulation responses that were not used for fitting.

This logic is well suited to held-out modality prediction:

{{< math >}}
p(y_k\mid y_{-k})
=
\sum_m\int
p(y_k\mid\phi,m)p(\phi,m\mid y_{-k})\,d\phi.
{{< /math >}}

Inference uses a subset of modalities, then predicts another observation that played no role in fitting. This separates “the model jointly reconstructed all modalities” from the stronger statement that one mechanism generalizes across observation systems.

Cross-scale mappings can themselves introduce mismatch. Concatenating features into one encoder risks hiding coarse-graining, volume-conduction and neurovascular errors in a shared latent vector. Coarse-to-fine full-waveform inversion in geophysics offers a more disciplined organization: low-frequency data first narrow the high-probability region, then higher-frequency data and local surrogate updates add detail. [Sequential surrogate work in full-waveform inversion](https://academic.oup.com/gji/article/243/2/ggaf349/8248518) provides one analogy.

### 4.3 Use interventions to expose differences hidden in passive data

Two mechanisms may generate almost identical spontaneous observations:

{{< math >}}
p(y\mid\phi_1,m_1)\approx p(y\mid\phi_2,m_2).
{{< /math >}}

After a known intervention {{< mi >}}a{{< /mi >}}, their responses may separate:

{{< math >}}
p(y^{(a)}\mid\phi_1,m_1,a)
\neq
p(y^{(a)}\mid\phi_2,m_2,a).
{{< /math >}}

Interventions directionally excite the dynamics. Two models may both explain a resting power spectrum yet predict different propagation directions, resonance frequencies, recovery times or seizure thresholds after stimulation.

Bayesian experimental design can select conditions that best distinguish parameters and models:

{{< math >}}
a^\star
=
\arg\max_a I\!\left((\phi,m);Y\mid a\right).
{{< /math >}}

For implicit simulators, neural mutual-information estimators can jointly optimize experimental design and posterior inference. [Bayesian experimental design for implicit models](https://proceedings.mlr.press/v119/kleinegesse20a.html) gives one such framework.

In neuroscience, interventions may include SEEG stimulation, TMS, DBS, pharmacology, task state and sleep–wake transitions. Parameters inferred from spontaneous activity should then predict how propagation reorganizes after the stimulation site changes, whether resonance appears as input frequency varies, or how thresholds and recovery change under a drug.

The intervention still needs a forward model. Which cells and fibres experience an electric field, which channels and synapses a drug changes simultaneously, and whether pre- and post-intervention states share one model structure all require explicit assumptions. For structural adaptation, a more useful objective may be to search the safe, feasible intervention set for maximal disagreement between models:

{{< math >}}
a^\star
=
\arg\max_a
D\!\left[p(Y\mid a,m_1),\ldots,p(Y\mid a,m_K)\right].
{{< /math >}}

Intervention then serves two purposes: narrowing parameter uncertainty and rejecting dynamical structures that cannot explain the new response.

### 4.4 Preserve a viable region when evidence remains limited

Even after model families, multimodal observations and interventions are added, some mechanisms may remain non-identifiable. History matching in climate and ocean modelling offers a useful language for this situation. Instead of forcing a single best parameter, it iteratively rules out implausible regions while preserving those that current evidence has not excluded.

For model {{< mi >}}m{{< /mi >}} and parameters {{< mi >}}\theta_m{{< /mi >}}, define an implausibility score

{{< math >}}
I_m(\theta_m)
=
\frac{
\left|s[M_m(\theta_m)]-s(y)\right|
}{
\sqrt{\sigma_{\rm obs}^2+\sigma_{\rm emulator}^2+\sigma_{\rm discrepancy}^2}
},
{{< /math >}}

then retain

{{< math >}}
\Theta_{\rm NROY}
=
\left\{(m,\theta_m):I_m(\theta_m)<c\right\},
{{< /math >}}

where NROY means *not ruled out yet*. History matching has been used to tune NEMO and climate models, using large parameter ensembles and emulators to shrink the observation-compatible region over successive waves. A [NEMO case study](https://gmd.copernicus.org/articles/10/1789/2017/) demonstrates the process.

For a neural mechanism, one could report

{{< math >}}
\Phi_{\rm NROY}(y)
=
\bigcup_{(m,\theta_m)\in\Theta_{\rm NROY}}g_m(\theta_m).
{{< /math >}}

This is the region of scientific targets compatible with the current model family, observation error and structural discrepancy. It can shrink as new modalities or interventions arrive. If several defensible models consistently yield similar {{< mi >}}\phi{{< /mi >}}, a stable cross-model conclusion may emerge. If they continue to disagree, model dependence remains visible in the result.

History matching does not have the direct probability interpretation of a standard posterior; its thresholds, summaries and discrepancy scales require scientific justification. What it offers is a more appropriate reporting resolution: which mechanisms have been excluded, which remain viable, and where the current model family still lacks identifiability.

## Conclusion: reliable inference should know when to stop

Neuroscience has long tried to connect data with mechanism. Black-box models learn complex mappings from large datasets; mechanistic models place ion channels, synapses, connectivity and state transitions into testable dynamical equations. SBI sits between them. Expert knowledge enters through the simulator, prior and experimental design, while neural density estimators perform parameter inversion where conventional likelihood methods struggle.

Several steps still separate this promise from noisy, sparsely sampled and multiscale neural data. Within-model posteriors, observation discrepancy and model structure must be calibrated separately. Parameters need shared scientific definitions across models. Multimodal data need an explicit cross-scale generative process. Interventions need a credible action model. Mechanistic mismatch under partial observation already shows that better data fit does not automatically resolve these problems.

The next advance may not come from one larger posterior network. It may come from a more complete inference process: model families that express dynamical alternatives, multi-fidelity simulators that allocate computation, cross-modal predictions and intervention responses that test mechanisms, and viable regions that remain wide when the evidence is weak.

The goal is simple to state. When evidence agrees, the posterior should contract appropriately. When model structure remains ambiguous, uncertainty should remain visible. And when current data cannot identify a mechanism, the inference should be able to stop there honestly.

### Further reading

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
