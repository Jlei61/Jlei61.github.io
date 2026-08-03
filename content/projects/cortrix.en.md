---
title: "How do multimodal neural data become one patient?"
date: 2026-08-02
slug: cortrix
translationKey: cortrix
cover:
  image: "/images/cortrix-patient-conference.png"
  alt: "An epilepsy case conference bringing MRI, PET, CT, EEG, SEEG and the patient's presurgical pathway into one shared discussion"
  caption: "Illustration: multimodal evidence reaches the same epilepsy case conference through different clinical workflows."
tags: ["BCI", "Neuroscience", "Virtual Brain", "SEEG", "Epileptor", "Multimodal Imaging"]
categories: ["Projects"]
description: "Beginning with a composite epilepsy case, this essay describes two paths for Cortrix: turning multimodal neural data into a repeatable clinical pipeline, then using that foundation to build testable patient-specific models."
estimatedReadingTime: "15 min"
aliases: ["/projects/cortix/"]
showToc: true
tocopen: false
hideMeta: false
disableShare: true
ShowBreadCrumbs: false
---

{{< figure src="/images/cortrix-patient-conference.png" alt="An epilepsy case conference bringing MRI, PET, CT, EEG, SEEG and the patient's presurgical pathway into one shared discussion" caption="Illustration: multimodal evidence reaches the same epilepsy case conference through different clinical workflows." >}}

I first understood the difficulty of multimodal neural data in a clinical case conference.

At a national neurosurgical referral centre in China, I joined discussions of patients with epilepsy. Structural MRI, PET, CT, scalp EEG, stereo-electroencephalography (SEEG), neuropsychological assessments and videos of clinical seizures often arrived at the same table. Radiologists looked for cortical malformations, tumours or hippocampal sclerosis. Nuclear-medicine physicians assessed the extent of hypometabolism. Electrophysiologists marked seizure onset and early propagation segment by segment. Neurologists and neurosurgeons then related this evidence to electrode implantation, resection boundaries and the preservation of function.

All of these materials came from the same brain, yet they reached the conference by entirely different routes.

Radiology understood the patient through image slices. Electrophysiology worked through waveforms and channel labels. Surgeons reconstructed another spatial account from gyri, vessels and possible operative corridors. Each discipline had mature tools and a coherent way of reasoning, but the final decision still required those partial views to be assembled back into one patient.

That assembly takes time and depends on a small number of people who understand the entire chain. **Cortrix** begins with this problem: first let one patient's data genuinely meet in a traceable space; only then ask how they might form a computable model on which interventions can be explored.

## Before a patient reaches a treatment decision

Consider a composite “Patient A”. The case combines steps that recur in clinical practice; it does not describe a particular person.

Patient A is in his thirties. Focal epilepsy has persisted for more than a decade, and several anti-seizure medications have failed to provide stable control. He travels to the centre with an MRI disc made several years earlier, a few paper EEG reports and seizure videos recorded by his family on a phone.

The first visit is partly an exercise in reconstruction. Clinicians must rebuild the seizure history, decide whether past events belong to the same seizure type and determine whether outside investigations can support the current presurgical assessment. The old MRI may lack an epilepsy protocol. PET and MRI may never have been registered reliably. A paper EEG report may preserve only the interpretation, not the original waveforms. The patient may therefore need another structural MRI and long-term video EEG, sometimes accompanied by fluorodeoxyglucose PET (FDG-PET), neuropsychological assessment or functional imaging.

After MRI acquisition, the data still require cortical reconstruction, anatomical parcellation, lesion annotation and manual quality control. [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) reconstructs cortical surfaces and anatomical regions from structural MRI. [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/) provides tools for structural, functional and diffusion MRI processing and registration. [MNE-Python](https://mne.tools/stable/) covers EEG/MEG preprocessing, lead-field construction and source analysis. Each package solves important parts of the chain; each also assumes that its user understands image orientation, coordinate spaces, tissue segmentation, signal processing and numerical methods.

Long-term video EEG accumulates data over days. Once monitoring ends, electrophysiologists identify seizures, compare their consistency, mark onset and early spread, and relate channel names to anatomy. PET requires reconstruction, correction, registration and specialist interpretation. Post-implantation CT must return to the preoperative MRI so that every SEEG contact can be located. Diffusion-weighted imaging (DWI) may enter a tractography pipeline to provide structural context for propagation and surgical planning.

Only when these results first meet does the patient enter a genuinely informed multidisciplinary discussion.

If non-invasive evidence converges on a well-demarcated lesion away from eloquent cortex, resection or ablation may be considered. More often, MRI, PET, scalp EEG and the clinical semiology do not point to exactly the same place. The team must then formulate an SEEG sampling hypothesis, segment vessels, design implantation trajectories, register post-implantation CT to MRI, localise the contacts and wait for enough spontaneous seizures to support a second discussion.

The waiting in this pathway has several causes. Beds, scanners, monitoring time and operating schedules are visible constraints. Image conversion, manual repair, EEG review, cross-modal registration and expert verification form a less visible human pipeline. That pipeline directly limits how many patients a centre can discuss in depth each week.

## Neural data are becoming longer, denser and more fragmented

Advances in neural recording will amplify this problem.

Clinical practice already works with MRI, CT, PET, DWI, EEG and SEEG. New brain–computer interfaces and neural recording devices are increasing both the duration and channel density of continuous data. In small-animal research, [Neuropixels 2.0](https://pubmed.ncbi.nlm.nih.gov/33859006/) provides more than 5,000 recording sites and has supported tracking of neuronal activity for more than two months during free behaviour.

Long-term human implants and use in the home are creating another form of continuous neural record. The Neural Electronic Opportunity (NEO) system developed by a Tsinghua team uses epidural electrodes with wireless power and communication. A [2025 medRxiv preprint](https://www.medrxiv.org/content/10.1101/2025.10.06.25337264v1) reported stable neural recordings for more than 18 months in one participant. This remains early evidence from a single case and has not been peer reviewed; it should not be generalised into a claim of long-term clinical performance.

These advances extend the timespan over which brain activity can be observed, but they also change the scale of the data problem. A patient or experimental subject is no longer represented by a handful of static examinations. The record may become a continuously updated combination of anatomy, implant location, neural signals, behaviour and device state.

In practice, these data often remain where they were produced: on a laboratory server, a departmental workstation, a device vendor's software or inside a small team familiar with one workflow. Collaboration across departments and institutions may still depend on manual exports, copied drives and repeated conversations about which version is current. Cohorts are difficult to scale, processing conventions are difficult to reuse, and new algorithms struggle to reach datasets large and heterogeneous enough for meaningful validation.

Smaller hospitals face a different version of the problem. The scanner or recording device may be available, while the full processing expertise is not. Cortical reconstruction, CT–MRI registration, DWI tractography, SEEG preprocessing and EEG source analysis require different backgrounds. A clinical team cannot infer from a collection of software manuals which question each modality can answer, how a result should be checked or what to trust when modalities disagree.

Specialist centres have more experience but also far more patients. A small group of experts repeatedly performs similar conversions and spatial checks. As volume rises, expert time becomes the limiting resource.

## The immediate value: a repeatable multimodal clinical pipeline

Multimodal neural data integration is first a clinical engineering problem.

Structural MRI, CT, PET, DWI, EEG, SEEG, lesions, vessels and implanted devices need to enter an explicit patient coordinate system. Every object should retain its source, processing parameters, spatial transformations, manual edits and quality-control state. When an upstream input changes, the system should be able to identify which derived results are no longer valid.

The [Brain Imaging Data Structure (BIDS)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978148/) provides a common organisation, naming system and metadata foundation for reproducible neuroimaging. A clinical pipeline must continue beyond file organisation and manage dependencies between raw data and derived results, so that a three-dimensional object can be traced back to the corresponding image slice, waveform segment and processing record.

Within a shared patient space, MRI contributes cortical and subcortical anatomy; CT shows haemorrhage, calcification and implanted hardware; PET provides metabolic distribution; DWI estimates white-matter connectivity; and EEG and SEEG describe electrical activity at different scales. A three-dimensional scene brings these results onto the same clinical work surface, allowing radiology, electrophysiology, neurology and neurosurgery to discuss the same spatial relationships.

{{< video src="/videos/cortrix-demo-low.mp4" label="Cortrix browser demo showing an interactive three-dimensional brain scene" caption="Figure 1. Cortrix places reconstructed anatomy, implanted hardware and neural data in one interactive 3-D scene. This recording demonstrates the interface and joint visualisation, not clinical performance." fallback="Open the Cortrix demo video" >}}

Three-dimensional integration does not replace the original images or waveforms. Clinicians still need to inspect MRI contrast, native PET slices, EEG time series and local SEEG activity. The shared scene supplies navigation between modalities: which gyrus contains an abnormal contact, how far it lies from a lesion boundary, whether it overlaps a hypometabolic region, and which vessels or tracts surround it.

For a smaller hospital, such a pipeline could provide a reusable application pattern. The clinical team could see where each modality enters the decision, which result requires manual confirmation and which failure should trigger a return to raw data. Standardised outputs would also be easier to send to a specialist centre for remote review.

For a high-volume centre, the potential value lies in shorter preparation and more consistent quality. Repeated conversion, surface reconstruction, registration, contact localisation and basic visualisation can be initiated through one workflow, leaving experts more time to investigate abnormalities, resolve conflicts and make clinical judgements. Automation performs preparatory work; the final decision remains with the team that understands the patient's history and the limits of treatment.

The same infrastructure could support stroke, intracerebral haemorrhage, Parkinson's disease and brain tumours. Acute stroke compresses multimodal imaging into minutes: non-contrast CT, CT angiography, perfusion imaging and clinical symptoms must meet quickly. Deep-brain stimulation (DBS) planning for Parkinson's disease relates a target, structural imaging, electrode position and stimulation field. Surgery for haemorrhage or tumour must consider lesions, vessels, functional regions and operative paths together. The timescale differs, but every application depends on a clear, traceable patient space.

The near-term case for a multimodal pipeline and joint visualisation is therefore concrete and testable. Whether it actually reduces preparation time, prevents errors or extends specialist capacity must be measured prospectively in real workflows; it cannot be inferred from an interface demonstration alone.

## From a shared patient space to a computable model

Once anatomy, connectivity, electrodes and neural activity occupy the same space, the clinical questions naturally extend further.

A clinician may ask which brain regions contributed to a scalp-EEG event; what a virtual electrode would record if moved; whether a seizure could still spread after a pathway was disconnected; or what network state might follow stimulation at a particular site.

These questions require observation and dynamical models on top of the patient space.

EEG source localisation works backwards from sensor measurements to activity inside the brain. Its basic observation relationship can be written as

{{< math >}}
\mathbf{y}(t)=\mathbf{L}\mathbf{j}(t)+\boldsymbol{\varepsilon}(t),
{{< /math >}}

where {{< mi >}}\mathbf{y}(t){{< /mi >}} is the EEG or SEEG observation, {{< mi >}}\mathbf{j}(t){{< /mi >}} represents candidate intracranial current sources and {{< mi >}}\mathbf{L}{{< /mi >}} is the lead field determined by head geometry, tissue conductivity, electrode position and source orientation.

Clinical recordings contain far fewer sensors than candidate sources, so several patterns of intracranial activity may generate similar scalp potentials. Source-localisation methods select a solution by imposing assumptions about smoothness, energy, orientation, sparsity or anatomical extent. Superficial, focal and high-signal-to-noise activity is usually better conditioned; deep, distributed or noisy activity carries greater spatial uncertainty.

{{< figure src="/images/cortrix-seeg-electrodes.gif" alt="Rotating cortical rendering with implanted SEEG shafts and individual electrode contacts" caption="Figure 2. Implanted SEEG shafts and contacts displayed in the reconstructed brain space. This clip documents the spatial interface; it does not establish electrode-localisation accuracy." >}}

A second route begins with dynamics inside the brain and generates signals that could be observed. A simplified whole-brain model can be expressed as

{{< math >}}
\dot{\mathbf{x}}(t)=F\!\left(\mathbf{x}(t),\mathbf{C},\boldsymbol{\theta},\mathbf{u}(t)\right),
{{< /math >}}

where {{< mi >}}\mathbf{x}(t){{< /mi >}} denotes hidden states at brain regions or cortical locations, {{< mi >}}\mathbf{C}{{< /mi >}} is structural connectivity, {{< mi >}}\boldsymbol{\theta}{{< /mi >}} contains parameters such as local excitability, time constants and coupling strength, and {{< mi >}}\mathbf{u}(t){{< /mi >}} represents external input. An observation function and lead field then map the model state to EEG or SEEG.

[The Virtual Brain](https://pubmed.ncbi.nlm.nih.gov/23781198/) brought individual structural connectivity, local neural dynamics and macroscopic brain signals into one simulation framework. The [Epileptor](https://pubmed.ncbi.nlm.nih.gov/24919973/) describes seizure onset, within-seizure activity and termination across multiple timescales, providing an important basis for [patient-specific modelling of seizure spread](https://pubmed.ncbi.nlm.nih.gov/27477535/).

Such generative models turn structural and dynamical hypotheses into waveforms, spectra and propagation patterns that can be compared with observations. Their output depends jointly on the equations, structural connections, delays, observation model and parameter ranges. A patient model must therefore be tested on seizures that were not used for fitting, on another measurement modality or against a real perturbation. Fitting an existing recording is not the same as predicting a new clinical event.

## The longer-term path: a virtual intervention before a real one

A shared patient space addresses how clinical data appear together. Patient-specific dynamics add a computable experimental environment.

Neurological treatment has a vast intervention space. Surgery must define the extent of resection, ablation or disconnection. DBS requires choices of target, contact, amplitude, frequency, pulse width and duty cycle. Responsive neurostimulation (RNS) adds detection features, trigger thresholds and response parameters. Pharmacological treatment introduces targets, dose, timing, combinations and patient stratification.

A real patient can tolerate very few trials. Surgery carries an irreversible cost. Neuromodulation may require repeated programming visits. Drug combinations can take months or longer to evaluate for both efficacy and adverse effects.

The purpose of virtual intervention is to construct a patient-specific candidate space before those real trials.

For structural interventions, a model could compare resection, ablation or fibre-disconnection boundaries and relate them to lesions, vessels, functional regions and the structural network. The spatial model determines where the change occurs; the dynamical model asks how activity might reorganise afterwards.

For electrical stimulation, device settings must first produce a spatial electric field, recruit neurons and axons, and alter network state before they can influence EEG, SEEG or clinical behaviour. Patient MRI, CT and electrode locations constrain the field. Fibre orientation and neuronal properties affect recruitment. The dynamical model describes how a local perturbation might alter whole-brain propagation and state transitions.

Recent work on [high-resolution virtual brain twins for stimulation](https://www.nature.com/articles/s43588-025-00841-6) has begun to connect patient MRI, DWI, EEG, SEEG, dynamical parameters and stimulation simulation while comparing invasive SEEG stimulation with non-invasive temporal-interference stimulation. These studies remain part of method development and patient-level demonstration; they are not mature treatment-decision systems.

In a more distant research programme, drugs could also enter the framework as perturbations of patient dynamics. Changes in ion channels, receptors, synaptic gain and excitation–inhibition balance might be represented as parameter changes, whose consequences for seizure threshold, propagation, oscillations and measurable signals could then be examined. Pharmacokinetics, pharmacodynamics and the spatial distribution of receptors would determine whether such a mapping could become quantitatively testable. Cortrix has not validated this pharmacological modelling chain; here it is a future research question, not a current capability.

At present, the most useful output of this route is a ranked set of candidate interventions and a real experiment designed to distinguish competing mechanistic hypotheses. A model might propose stimulation sites worth comparing, frequencies expected to produce different network responses, or an evoked response that would be especially informative. Only when real stimulation, drug response or postoperative change returns to the model can its patient parameters and mechanistic account be updated.

Virtual and real intervention should therefore form a loop:

{{< math >}}
\text{patient data}
\longrightarrow
\text{patient model}
\longrightarrow
\text{candidate intervention}
\longrightarrow
\text{real test}
\longrightarrow
\text{model update}.
{{< /math >}}

## Two paths of value, on two timescales

The multimodal pipeline and virtual intervention address two different levels of neurological medicine.

The first path belongs to today's clinical workflow. Patients have already generated many investigations, but their data remain divided among devices, departments, software packages and teams. Automated processing, data-lineage management and joint three-dimensional presentation can reduce repeated work, make interdisciplinary communication more consistent and allow the experience of specialist centres to travel in a more stable form.

The relevant measures are relatively clear: time required to prepare one case, registration and annotation errors, number of manual steps before conference, reproducibility of spatial relationships across clinicians, and whether a smaller hospital can generate results suitable for specialist review. This is infrastructure that can be built and deployed now, although its value still needs validation in real clinical workflows.

The second path belongs to future intervention research. A patient-specific model places structure, connectivity, neural activity and intervention mechanisms in one computational environment to narrow the candidate space for drugs, surgery and neuromodulation. Its tests are harder: can the model predict unseen data, explain differences between patients, propose stimulation or drug experiments that distinguish hypotheses, and help a trial discard low-value options earlier?

This direction could eventually affect more than programming a device for one patient. Moving a drug or neuromodulation technology from mechanism discovery through animal studies, early human research and formal clinical trials consumes considerable time and resources. Only if patient models reliably identify likely responders, high-priority parameter regions and informative endpoints in independent data should later studies be organised around the smaller candidate set they propose.

The multimodal pipeline first makes patient data usable. Virtual intervention builds on that foundation and turns integrated data into testable treatment hypotheses.

The first path asks whether a clinical team can see what is happening now with less repeated work. The second asks whether drugs, surgery and neuromodulation can enter real clinical testing with a smaller and more informative search space. They are at different stages of development, but together they define Cortrix's longer route from data infrastructure to intervention science.

→ **[Open the live Cortrix demo](https://jlei61.github.io/Cortix-DEMO/)**

### Further reading

1. Gorgolewski et al. [The Brain Imaging Data Structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978148/). *Scientific Data*, 2016.
2. Steinmetz et al. [Neuropixels 2.0: A miniaturized high-density probe for stable, long-term brain recordings](https://pubmed.ncbi.nlm.nih.gov/33859006/). *Science*, 2021.
3. Yao et al. [Fine grained two-dimensional cursor control with epidural minimally invasive brain-computer interface](https://www.medrxiv.org/content/10.1101/2025.10.06.25337264v1). *medRxiv* preprint, 2025.
4. Sanz Leon et al. [The Virtual Brain](https://pubmed.ncbi.nlm.nih.gov/23781198/). *Frontiers in Neuroinformatics*, 2013.
5. Jirsa et al. [On the nature of seizure dynamics](https://pubmed.ncbi.nlm.nih.gov/24919973/). *Brain*, 2014.
6. Jirsa et al. [The Virtual Epileptic Patient](https://pubmed.ncbi.nlm.nih.gov/27477535/). *NeuroImage*, 2017.
7. Wang et al. [Virtual brain twins for stimulation in epilepsy](https://www.nature.com/articles/s43588-025-00841-6). *Nature Computational Science*, 2025.
