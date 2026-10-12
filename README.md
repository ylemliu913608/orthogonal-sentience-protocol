# Orthogonal Two-Tier Sentience Assessment Protocol (v3.2)

> 📄 **Preprint (DOI)**: `[Pending OSF/PhilSci DOI — will be updated within 24h]`  
> ⚖️ **Discussion**: `[Pending LessWrong Link]`  
> 🇨🇳 **[中文版完整论文与协议说明请点击这里 (Chinese Version)](docs/paper_cn.md)**

## Overview
This repository hosts the formal specification, JSON evaluation schema, and Epistemic Hygiene Linter (`.cursorrules`) for **"Bridging Autopoiesis and Computational Functionalism: A Lightweight Two-Tier Extension to Butlin et al. (2023)"**.

To resolve the decoupling vulnerability (e.g., Blockhead lookup tables, static connectome playbacks) inherent in purely computational checklists, this protocol decouples sentience assessment into two serial, orthogonal gates:
1. **Tier-1 (Homeostatic Admission Layer — Necessary Pre-filter)**: Requires a statistical/physical boundary, non-equilibrium metabolic throughput, and **intrinsic feedback-driven structural repair** within the system's own boundary granularity. Systems failing Tier-1 are short-circuited (`—`).
2. **Tier-2 (Computational Realization Layer — Active Switch)**: Evaluates admitted systems using the 14 computational indicators from Butlin, Long, et al. (2023) (RPT, GWT, HOT, AST, PP, AE).

## Precautionary Tri-Valued Assessment Matrix (v3.2)
*(Insert your Section 4 English Matrix Table from Paper_EN.md here)*

## Repository Structure
- `docs/paper_en.md` — Full English commentary paper (v3.2).
- `docs/paper_cn.md` — Full Chinese commentary paper (v3.2 中文定稿).
- `protocol/sentience_eval_schema.json` — Strict Draft-07 JSON Schema enforcing Tier-1 short-circuiting (R0), Kleene tri-valued conjunction, R3 indeterminate propagation, and R4 non-veto rules.
- `tools/score.py` — Companion CLI validator enforcing what static JSON Schema cannot: regex-based Epistemic Hygiene Linter (scanning `evidence` strings for prohibited teleological/absolute terms) and Tier-2 14-indicator aggregation consistency.
- `audit_rules/.cursorrules` — Epistemic Linguistic Hygiene Linter rules for Cursor / Claude / LLM research agents (English & Chinese).

## Quick Start: Running an Audit
`tools/score.py` runs out-of-the-box with **zero external dependencies** on Python 3.7+ (and automatically pairs with `jsonschema` Draft-07 validation if installed):
```bash
python tools/score.py protocol/sentience_eval_schema.json cases/your_system_eval.json
