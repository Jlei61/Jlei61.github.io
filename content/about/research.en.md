---
title: "Understanding Brain Dynamics and Mechanisms from Partial Observations"
date: 2026-08-03
slug: research
translationKey: research-approach
tags: ["Computational Neuroscience", "Neural Engineering", "Neural Dynamics", "Multimodal Neuroscience"]
categories: ["About"]
description: "My research approach connects mechanistic neuroscience, multimodal neural engineering and uncertainty-aware computational modelling."
estimatedReadingTime: "6 min"
showToc: true
tocopen: false
hideMeta: false
disableShare: true
ShowBreadCrumbs: false
---

The brain is a complex system, yet every neural dataset is only a partial observation of it. Different recording technologies reveal different spatial and temporal scales. Spiking activity provides precise but local measurements of neuronal activity. Stereo-electroencephalography (SEEG) and electrocorticography (ECoG) record population signals from limited regions. Electroencephalography (EEG) and neuroimaging offer broader coverage, but their relationship to the underlying dynamics is more indirect.

My research centres on one question:

> **When observations are incomplete and models are necessarily simplified, how can we recover reliable neural dynamics—and determine whether a model has identified a mechanism rather than merely a statistical representation that fits or decodes the data?**

## Science: finding stable mechanisms across repeated observations

I study how neural population activity gives rise to decisions, state transitions and pathological propagation. My previous work has examined latent representations during human decision-making and the relationship between interictal epileptic activity and seizure dynamics.

These projects have made me less interested in whether a single signal can be classified than in whether stable spatiotemporal structure persists across repeated events. Does that structure generalise across tasks, states or individuals? What perturbation or new observation would be needed to show that it genuinely participates in neural computation?

## Engineering: allowing different modalities to describe the same individual brain

A single modality is rarely sufficient for a complete mechanistic account. Anatomy, white-matter connectivity, electrode positions, source activity and electrophysiological signals each describe a different part of the brain system. I therefore also work on integrating these sources of information reliably.

For this purpose, I develop **Cortrix**, which organises MRI, CT, DWI, fMRI, EEG, SEEG and ECoG within a unified, traceable individualised brain space. Its purpose extends beyond three-dimensional visualisation: I want it to become a working environment that connects multimodal observations, neural dynamical models and predictions about intervention.

Within this framework, virtual resection, tract disconnection, neural stimulation and electrode implantation can be represented as changes to network nodes, connections, inputs or observation models. My long-term goal is for virtual intervention to provide a faster, lower-cost and repeatedly testable layer of model validation before real experiments or clinical procedures.

## Computation: combining existing knowledge with learning from data

Compared with images and language, neuroscience datasets are often smaller, noisier and more incompletely sampled. Ground-truth labels for mechanistic parameters are also much harder to obtain. I therefore do not expect larger end-to-end models alone to resolve the central questions of neuroscience.

I am more interested in a hybrid modelling strategy: treating neural dynamical equations, anatomical structure and experimental knowledge as meaningful inductive biases, while using machine learning to provide enough expressive capacity to discover structure that was not written into the model in advance.

Such models should not be judged only by predictive accuracy. They should also be open to perturbation, comparison and falsification—and should state honestly which mechanisms remain unresolved when observations are insufficient or model assumptions are wrong.
