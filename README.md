# VWI: Virtual World Framework

[English Version](README.md) | [中文版](README_zh-CN.md)

"There is no free will; there are only the consequences of stress, strain, and emergence."

This repository hosts `virtual-world-framework`. The internal project codename `VWI` is used throughout the documentation and demo code.

VWI is a research-oriented virtual world framework. It explores how to combine deterministic simulation, personality modeling, and large language models (LLMs) into a unified sandbox system. Rather than treating characters as static sets of personality tags, VWI treats them as materials under stress. External events act as multidimensional impacts, which characters process through their internal desire structures. Psychological changes accumulate as elastic or plastic strain, and decisions emerge from deterministic state transitions rather than a fixed concept of free will. Character actions then write back to the world, generating new causal chains.

## Dual-Engine Architecture

The framework operates on a dual-engine loop:

1. **Sentient World**
   - The internal cognitive layer of characters.
   - Handles subjective stress calculation.
   - Manages memory and trauma accumulation.
   - Computes elastic vs. plastic psychological deformation.
   - Triggers phase transformation under extreme pressure.
   - Produces bounded decision outputs.

2. **Vessel World**
   - The external environmental layer.
   - Manages event generation and propagation.
   - Tracks environmental change.
   - Processes karma and consequence write-back.
   - Drives world-state evolution across ticks.

## Theoretical Direction: Personality Material Mechanics

VWI adopts the perspective of "personality material mechanics." Key concepts include:

- **Stress**: The multidimensional psychological pressure exerted on a character by external events, amplified by their specific desires.
- **Elastic strain**: Temporary psychological or emotional fluctuations that recover over time.
- **Plastic strain**: Permanent, irreversible psychological deformation or trauma.
- **Fracture**: Complete psychological breakdown when plastic strain exceeds a critical threshold.
- **Phase transformation / alloying**: Fundamental shifts in personality structure (e.g., becoming hardened or sensitized) triggered under extreme stress, occasionally facilitated by LLM intervention.

This is a research model, not a claim to absolute psychological realism. The current implementation is primarily designed to test whether this framework can produce coherent simulation behavior.

## Current Status

This repository is **not** a production-ready engine. It is a research alpha, a conceptual framework, an early technical prototype, and a public snapshot of an evolving system. 

Many components are intentionally simplified. For example, the current demo uses placeholder-style random population generation and a simplified social topology. These exist primarily to prove that the engine pipeline can run end-to-end.

## Repository Structure

- `docs/` - theoretical documents, whitepapers, and design notes
- `demo/` - early proof-of-concept code (`vwi_demo`)

## Running the Demo

The Python demo uses package-style relative imports. Therefore, it must be run as a module from the project root, rather than executing `__main__.py` directly.

To run the simulation, use the following command:

```bash
python -m vwi_demo --ticks 20 --mode GOD
```

### Available Parameters:
- `--ticks`: Number of simulation ticks to run.
- `--mode`: Interaction mode (`GOD`, `ARCHON`, or `AVATAR`).
- `--seed`: Integer seed for random generation.
- `--use-llm`: Flag to enable LLM integration. LLM-assisted behavior requires API configuration; otherwise, the demo gracefully falls back to a pure mathematical/non-LLM path.
- `--interactive`: Flag to enable step-by-step interactive mode.
- `--model`: Specify the LLM model to use (default: `gpt-3.5-turbo`).
- `--avatar`: The character ID to play as when in `AVATAR` mode.
- `--population`: The number of initial nodes to randomly generate (default: 4).

Logs for the simulation run will be written to: `outputs/run_log.jsonl`

## Demo Disclaimer

The current demo should be understood strictly as an engine experiment, not as a complete social simulation product. This early version is built to validate:
- The dual-engine loop.
- The stress -> deformation -> decision mapping.
- The world write-back logic.
- The basic LLM-assisted phase transformation flow.

It does **not** represent:
- A fully realistic society model.
- A large-scale concurrency architecture.
- A production deployment system.

## Suggested Reading Order

To understand the framework, we recommend reading the materials in this order:

1. Top-level architecture design
2. Sentient-world / personality engine documents
3. Material transformation / personality mechanics documents
4. Vessel-world / external world engine documents
5. Demo code

## Why This Repository is Public

We have made this repository public for three main reasons:
1. To make the core ideas inspectable.
2. To establish a public research starting point.
3. To iterate in the open instead of waiting for a "perfect" first release.

## License

This project is licensed under a custom Virtual World Framework License. The license permits personal study, education, research, and non-commercial evaluation. 

Commercial use, SaaS / hosted deployment, or integration into closed-source products requires separate written permission from the copyright holder.

Please see [LICENSE](LICENSE) for details.
