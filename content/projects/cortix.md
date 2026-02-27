---
title: "Cortix — Multimodal Neural Digital Twin"
date: 2026-02-27
tags: ["BCI", "Neuroscience", "SEEG", "EEG", "Source Imaging", "WebGL"]
categories: ["Projects"]
description: "An open interactive platform that unifies cortical surfaces, intracranial electrophysiology, CT coregistration, and source imaging in a real-time 3-D viewer."
showToc: true
---

## Overview

**Cortix** is a multimodal neural digital twin platform built for clinical neuroscience research. It brings together anatomical and electrophysiological data into a single real-time 3-D web interface — no installation required.

## Key Features

| Module | Description |
|--------|-------------|
| **3-D Brain Viewer** | Pial / white / inflated surfaces with per-region coloring |
| **CT Coregistration** | Raw CT overlaid on MRI with electrode detection |
| **SEEG / EEG Playback** | Streamed chunked playback with bipolar/monopolar modes |
| **IED Detection** | Two-stage interictal spike detection with band envelopes |
| **Source Imaging** | dSPM source localization rendered as a Gaussian heat-map |
| **DWI Tractography** | White-matter fiber bundles overlaid on the brain |

## Live Demo

The demo runs entirely in the browser with pre-packaged S002 sample data — no backend required.

→ **[Launch Cortix Demo](https://jlei61.github.io/Cortix-DEMO/)**

## Tech Stack

- **Frontend**: Vanilla JS + Three.js + WebGL
- **Build**: Vite (multi-page, static export)
- **Backend** *(full mode)*: Python / Flask + MNE-Python / Dipy
- **Deployment**: GitHub Pages

## Source Code

→ [github.com/Jlei61/Cortix-DEMO](https://github.com/Jlei61/Cortix-DEMO)
