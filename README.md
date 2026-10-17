# Orthogonal Two-Tier Sentience Assessment Protocol (v3.3)

> 📄 **Preprint (DOI)**: [10.5281/zenodo.23327409](https://doi.org/10.5281/zenodo.23327409)  
> 🐦 **Author thread**: [X](https://x.com/ylemliu/status/2111532000163373511)  
> 💬 **Discussion**: [GitHub Issues](https://github.com/ylemliu913608/orthogonal-sentience-protocol/issues)  
> 🇬🇧 **[Full English paper (Markdown)](docs/paper_en.md)**  
> 🇨🇳 **[中文版完整论文与协议说明请点击这里 (Chinese Version)](docs/paper_cn.md)**  

## Overview
This repository hosts the formal specification, JSON evaluation schema, and Epistemic Hygiene Linter (`.cursorrules`) for **"Bridging Autopoiesis and Computational Functionalism: A Lightweight Two-Tier Extension to Butlin et al. (2023)"**.

To resolve the decoupling vulnerability (e.g., Blockhead lookup tables, static connectome playbacks) inherent in purely computational checklists, this protocol decouples sentience assessment into two serial, orthogonal gates:
1. **Tier-1 (Homeostatic Admission Layer — Necessary Pre-filter)**: Requires a statistical/physical boundary, non-equilibrium metabolic throughput, and **intrinsic feedback-driven structural repair** within the system's own boundary granularity. Systems failing Tier-1 are short-circuited (`—`).
2. **Tier-2 (Computational Realization Layer — Active Switch)**: Evaluates admitted systems using the 14 computational indicators from Butlin, Long, et al. (2023) (RPT, GWT, HOT, AST, PP, AE).

## Precautionary Tri-Valued Assessment Matrix (v3.3)
See §4 of [Paper_EN.md](docs/paper_en.md) for the full matrix.

## Repository Structure
- `docs/paper_en.md` — Full English commentary paper (v3.3).
- `docs/paper_cn.md` — Full Chinese commentary paper (v3.3 中文定稿).
- `protocol/sentience_eval_schema.json` — Strict Draft-07 JSON Schema enforcing Tier-1 short-circuiting (R0), Kleene tri-valued conjunction, and the R0–R5 derivation state machine.
- `tools/score.py` — Companion CLI validator enforcing what static JSON Schema cannot: regex-based Epistemic Hygiene Linter (scanning `evidence` strings for prohibited teleological/absolute terms) and Tier-2 coherence floors.
- `audit_rules/.cursorrules` — Epistemic Linguistic Hygiene Linter rules for Cursor / Claude / LLM research agents (English & Chinese).
- `examples/*.json` — Three canonical records, one per verdict.
- `tests/selftest.py` — Self-test harness; generates fixtures and asserts validator behaviour.

## Quick Start: Running an Audit
`tools/score.py` runs out-of-the-box with **zero external dependencies** on Python 3.7+ (and automatically pairs with `jsonschema` Draft-07 validation if installed):
```bash
python tools/score.py protocol/sentience_eval_schema.json examples/01_awake_human_R2_Satisfied.json
```
