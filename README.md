# VWI (Virtual World Infrastructure): Dual-Engine of Sentient & Vessel Worlds

[English Version](README.md) | [中文版](README_zh-CN.md)

> **"There is no free will; there are only the consequences of stress, strain, and emergence."**

VWI (Virtual World Infrastructure) is a **research-oriented virtual world infrastructure**. By bidirectionally binding a "Physics Engine" with "Large Language Models (LLMs)", it constructs an autonomous sandbox system that strictly follows determinism, possesses microscopic psychological evolution capabilities, and macroscopic social emergent properties.

This project is currently in the **Research Alpha** phase. It primarily open-sources its foundational **core theoretical architecture and whitepapers**, accompanied by some proof-of-concept code (`vwi_demo`).

---

## Core Ontology: No Self, Only Karma

The philosophical core of this system is deeply inspired by Buddhist ontology, translating it into a rigorous software engineering paradigm:

In this world, **NPCs (Characters) do not possess so-called "free will."**
Every decision a character makes, every line they speak, is a **deterministic strain calculation result** produced when their "personality material" faces "physical impacts" from the external world.
- **Anatta (No-Self)**: There is no permanent "soul" with free will making decisions. A character is merely a collection of "material properties" (Stiffness $E$, Toughness $T$, Plastic Strain $\varepsilon_p$) that are constantly hammered, twisted, and annealed by external events.
- **Karma (Cause and Effect)**: Characters' actions generate "Karma," which writes back to and alters the external world (the Vessel World). This triggers new events that continue to impact the psychological materials of other characters, forming an indestructible chain of causality.

Through an incredibly complex computational closed-loop, the system allows these deterministic equations to exhibit the **illusion of free will**—behaviors that look like "choices" and "humanity."

---

## Theoretical Foundation: Material Physics Mapping Psychology

The system abandons traditional "personality tags" and "linear HP deduction" models, pioneering the **Personality Material Mechanics Model**:

1. **Stress ($\sigma$)**: The impact caused by external events across four dimensions (Somatic, Material, Social, Ideological) is amplified through the character's "Desire Matrix," forming psychological pressure.
2. **Elastic Strain ($\varepsilon_e$)**: Temporary emotional fluctuations that subside after the pressure disappears.
3. **Plastic Strain ($\varepsilon_p$)**: Irreversible personality distortion. When pressure exceeds a character's "Yield Point," they suffer permanent psychological trauma and personality drift.
4. **Fracture**: When plastic strain surpasses the extreme limit, the character breaks down completely.

### Soul Alchemy: Phase Transformation and Alloying
Under extreme psychological strain, the Large Language Model (LLM) intervenes as an "Alchemist," injecting alloy elements into the character to alter their underlying material structure (Phase Transformation):
- **Carbon (C)**: Hardens and makes brittle; leads to arrogance or "Blackening" (Martensite).
- **Nickel (Ni)**: Softens the heart, increases toughness; leads to tolerance or "Sanctification" (Austenite).
- **Sulfur (S)**: Introduces toxicity, drastically lowering the breakdown threshold.

---

## Engineering Closed-Loop: The 7-Step FSM Pipeline

Every cognitive cycle of a character must strictly pass through the following 7-step pipeline, designed based on the Buddhist concept of the Five Aggregates (Skandhas):

1. **Contact (触)**: Perception and multi-dimensional subjective stress calculation (Objective Impact $\times$ Desire Amplification).
2. **Conditioning (缘)**: Context buffering and the stress concentration effect ($K_t$) of historical trauma anchors.
3. **Sensation (受)**: Calculation of elastic strain and accumulation of plastic distortion.
4. **Cognition (想)**: Motivation generation, and triggering LLM's alloying judgment under extreme pressure.
5. **Conflict (行)**: Calculation of internal friction ($F_{int}$) between internal drives and moral/risk constraints.
6. **Decision (识)**: Five-state decision output (The system forces convergence into five absolute enums: `EXPLODE`, `ACT`, `HESITATE`, `SUPPRESS`, `BREAKDOWN`).
7. **Karma (业)**: Multi-dimensional karma write-back, affecting the external world and recording time-decay logs.

---

## Architecture Guarantees: Tick Isolation and Single Source of Truth

To ensure causal determinism under multi-character concurrency, VWI adopts strict, industry-grade architectural standards:
- **Tick Isolation (Double Buffering)**: In any Tick $N$, characters can only read from a frozen, read-only snapshot $State_N$.
- **CQRS and Transaction Pool**: Decisions made by characters during the "Karma" phase are pushed into a global transaction pool. The `Karma Resolver` handles conflict merging to generate $State_{N+1}$.
- **LLM Structural Clamping**: Through strict JSON Schemas and global enum truth tables, the system completely seals off the risks of LLM numerical divergence or semantic drift.

---

## Open Source Content

This repository currently contains the following core components:

1. **Theoretical Whitepapers** (`*.md` in Chinese): Detailed architectural designs, mathematical formulas, and engineering flowcharts for both the Sentient World (psychological engine) and Vessel World (physical sandbox). This is the absolute foundation of the project.
2. **Proof of Concept Prototype** (`/vwi_demo`): Contains a miniature Python-based dual-engine prototype. Used to verify the feasibility of "Material Mechanics Mapping Psychology" and "LLM Bidirectional Binding." (*Note: This code is currently a single-threaded prototype for theoretical validation, provided for research reference.*)

### How to Read the Documentation (Currently in Chinese)

We recommend reading the theoretical designs in the following order:
1. `虚拟世界基础设施V2.0架构设计.md` (VWI V2.0 Architecture Design) — Macro top-level design and engineering closed-loop specifications.
2. `有情世间引擎文档1.0.md` (Sentient World Engine Doc) — Core psychological engine (7-step pipeline and material model).
3. `人格模拟系统10.0设计方案（上）.md` (Personality Simulation System V10.0) — The underlying logic of material phase transformations.
4. `器世间引擎文档1.0.md` (Vessel World Engine Doc) — Natural evolution and event diffusion of the external physical environment.

## Future Outlook
VWI aims to explore the boundaries of complex autonomous systems in the AI era. We have proven that by placing "mathematical shackles" on LLMs, narratives can become rigorous and computable. Future evolutionary directions include: Social fluid dynamics, complete database-backed Event Sourcing, and integration with massive parallel computing.