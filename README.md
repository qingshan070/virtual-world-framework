# VWI: Virtual World Framework

[English](README.md) | [简体中文](README_zh-CN.md)

> There is no free will; there are only the consequences of stress, strain, and emergence.

VWI is a **research-oriented virtual world framework** for exploring how deterministic simulation, personality modeling, and large language models can be combined into a unified sandbox system.

This repository is currently in an **early alpha / proof-of-concept** stage. It contains:

- core theoretical documents and whitepapers
- an early Python demo of the dual-engine design
- implementation notes for future iterations

> **Naming note**
>  
> This repository is hosted under the name `virtual-world-framework`.  
> `VWI` remains the current internal project codename used in existing documents and demo code.

---

## What VWI is trying to do

VWI attempts to model characters not as collections of static personality tags, but as **materials under stress**.

In this framework:

- external events act as multi-dimensional impacts
- characters transform those impacts through internal desire structures
- psychological changes accumulate as elastic or plastic strain
- decisions emerge from deterministic state transitions rather than a fixed notion of “free will”
- character actions write back to the world and generate new causal chains

The goal is not to imitate humans with vague role labels, but to build a more structured simulation loop between **inner cognition** and **outer world state**.

---

## Core idea

The project is built around a dual-engine structure:

### 1. Sentient World
The internal cognitive layer of characters.

This part focuses on:
- subjective stress calculation
- memory and trauma accumulation
- elastic vs. plastic psychological deformation
- phase transformation under extreme pressure
- bounded decision output

### 2. Vessel World
The external world layer.

This part focuses on:
- event generation and propagation
- environmental change
- karma / consequence write-back
- world-state evolution across ticks

Together, these two layers form a closed loop:
**world impacts character -> character changes -> character acts -> world changes again**

---

## Theoretical direction

VWI uses a **personality material mechanics** perspective.

Some of the key ideas include:

- **Stress**: external impact across somatic, material, social, and ideological dimensions
- **Elastic strain**: temporary emotional fluctuation
- **Plastic strain**: irreversible personality deformation
- **Fracture**: complete breakdown after accumulated overload
- **Phase transformation / alloying**: under extreme conditions, the model may alter the character’s internal material structure

This is a research model, not a claim of psychological realism.  
The current implementation is meant to test whether such a framework can produce coherent simulation behavior.

---

## Current status

This repository is **not** a production-ready engine.

At the moment, it should be understood as:

- a research alpha
- a conceptual framework
- an early technical prototype
- a public snapshot of an evolving system

Some parts are intentionally simplified.  
For example, the current demo uses placeholder-style random population generation and a simplified social topology to prove that the engine pipeline can run end to end.

---

## Repository structure

```text
docs/   theoretical documents, whitepapers, and design notes
demo/   early proof-of-concept code
Running the demo

The Python demo currently uses package-style relative imports.

Please run it from the project root as a module, instead of directly executing __main__.py.

Example:

python -m vwi_demo --ticks 20 --mode GOD

Available options may include:

--ticks number of simulation ticks
--mode interaction mode (GOD, ARCHON, AVATAR)
--seed random seed for reproducibility
--use-llm enable LLM-assisted processing when configured
--interactive interactive event input

If enabled, logs are written to:

outputs/run_log.jsonl
Notes on the demo

Please read the current demo as an engine experiment, not as a complete social simulation product.

The present version is mainly used to validate:

the dual-engine loop
stress -> deformation -> decision mapping
world write-back logic
basic LLM-assisted phase transformation flow

It does not yet represent a fully realistic society model, large-scale concurrency architecture, or production deployment system.

Suggested reading order

If you want to understand the project from theory to prototype, a good reading order is:

top-level architecture design
sentient-world / personality engine documents
material transformation / personality mechanics documents
vessel-world / external world engine documents
demo code
Why this repository is public

This repository is being published in its current form for three reasons:

to make the core ideas inspectable
to establish a public research starting point
to iterate in the open, instead of waiting for a “perfect” first release
License

This project uses a custom Virtual World Framework License.

It is available for personal study, education, research, and non-commercial evaluation only.

Commercial use, SaaS/hosted deployment, and integration into closed-source products require separate written permission from the copyright holder.

Please see LICENSE
 for details.
