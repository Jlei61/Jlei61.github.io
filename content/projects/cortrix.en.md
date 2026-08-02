---
title: "Why I Built Cortrix"
date: 2026-08-02
slug: cortrix
translationKey: cortrix
tags: ["BCI", "Neuroscience", "SEEG", "EEG", "Source Imaging", "WebGL"]
categories: ["Projects"]
description: "A practical account of building one workspace for anatomy, intracranial recordings, registration, and source-imaging results—and of what the current system can and cannot establish."
aliases: ["/projects/cortix/"]
showToc: true
---

Neuroscience projects rarely fail because one more plot is missing. They fail quietly at the joins: an electrode is displayed in the wrong coordinate frame, a derived surface is reused after its source changed, or a figure can no longer be traced back to the data and transform that produced it.

I built **Cortrix** to make those joins visible.

## The problem I wanted to solve

An intracranial study can involve a cortical reconstruction, CT–MRI registration, SEEG or ECoG contacts, continuous recordings, diffusion-derived pathways, and source estimates. Each modality already has capable specialist software. The difficult part is keeping their identities, coordinate systems, and provenance aligned while moving between them.

Cortrix puts these materials into one subject-centred workspace. The 3-D view is useful, but it is not the main scientific claim. The more important goal is to make every displayed object answer three questions:

1. Which subject and source data does it belong to?
2. In which coordinate frame is it expressed?
3. Which transforms and processing steps produced it?

That is less glamorous than calling the system a “digital twin,” but it is the foundation required before the phrase can mean anything scientifically.

## What is connected today

The current platform brings several workflows into the same interactive scene:

- pial, white-matter, and inflated cortical surfaces;
- CT–MRI registration and electrode localisation;
- SEEG and EEG playback, including bipolar and monopolar views;
- interictal-event review outputs;
- diffusion tractography and region-level anatomy;
- BEM and source-imaging results.

The browser demo uses a packaged example dataset and runs without a backend. It is meant to make the interaction model inspectable, not to serve as evidence of clinical performance.

→ **[Open the Cortrix demo](https://jlei61.github.io/Cortix-DEMO/)**

## The engineering choice that matters most

My priority is not to add every possible analysis to the viewer. It is to keep a strict contract between data, coordinates, provenance, and presentation.

Derived assets therefore need stable fingerprints. A contact set must remain bound to the image and transform chain used to localise it. A saved figure must record enough state to be recreated. Quality-control results should travel with the object they describe instead of living in an unrelated folder or screenshot.

These contracts turn the viewer from a collection of visual layers into a research workspace that can be checked mechanically.

## What Cortrix does not prove yet

Cortrix is currently best described as a **methods and research-infrastructure project**. Contract-level tests and representative cases can show that components are wired together consistently. They do not establish that an event detector is clinically accurate, that a source estimate is superior to existing methods, or that the platform improves patient outcomes.

Those questions require frozen datasets, explicit baselines, independent evaluation, and task-specific metrics. I want the site to keep that boundary visible as the project develops.

## What comes next

The next stage is less about adding modules and more about strengthening evidence: reproducible example cases, clearer quality-control reports, versioned data contracts, and figures that can be regenerated from recorded state.

I will use this blog to document those decisions—including the failures and trade-offs that do not belong in a feature table.

**Source:** [github.com/Jlei61/Cortix-DEMO](https://github.com/Jlei61/Cortix-DEMO)
