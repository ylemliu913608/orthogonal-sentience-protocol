# Orthogonal Two-Tier Sentience Assessment Protocol (v3.3)

> 📄 **Preprint (DOI)**: `[Pending OSF/PhilSci DOI — will be updated within 24h]`  
> ⚖️ **Discussion**: `[Pending LessWrong Link]`  
> 🇨🇳 **[中文版完整论文与协议说明请点击这里 (Chinese Version)](docs/paper_cn.md)**

## Overview
This repository hosts the formal specification, JSON evaluation schema, and Epistemic Hygiene Linter (`.cursorrules`) for **"Bridging Autopoiesis and Computational Functionalism: A Lightweight Two-Tier Extension to Butlin et al. (2023)"**.

To resolve the decoupling vulnerability (e.g., Blockhead lookup tables, static connectome playbacks) inherent in purely computational checklists, this protocol decouples sentience assessment into two serial, orthogonal gates:
1. **Tier-1 (Homeostatic Admission Layer — Necessary Pre-filter)**: Requires a statistical/physical boundary, non-equilibrium metabolic throughput, and **intrinsic feedback-driven structural repair** within the system's own boundary granularity. Systems failing Tier-1 are short-circuited (`—`).
2. **Tier-2 (Computational Realization Layer — Active Switch)**: Evaluates admitted systems using the 14 computational indicators from Butlin, Long, et al. (2023) (RPT, GWT, HOT, AST, PP, AE).

## Precautionary Tri-Valued Assessment Matrix (v3.3)

`✅ Satisfied` / `🔶 Indeterminate` / `❌ Unsatisfied` — evaluated at the granularity of each system's own boundary. **Any system failing Tier-1 is short-circuited and its Tier-2 field is `— (Not Evaluated)`.**

| Target System (At Own Boundary Granularity) | Tier-1 | Tier-2 | Final Verdict | Core Rationale |
|---|---|---|---|---|
| **Awake Humans / Mammals** | ✅ | ✅ | **✅ Satisfied** | Homeostatic repair and GWT/HOT global loops concurrently active (1st- & 2nd-order experience). |
| **Humans under General Anesthesia** | ✅ | ❌ | **❌ Unsatisfied** | Tier-1 intact, but Tier-2 thalamocortical broadcasting is pharmacologically blocked. |
| **Covert Consciousness / Vegetative Patients** | ✅ | 🔶 | **🔶 Indeterminate** | Severed motor output does not alter the internal auto-coincident locus. |
| **Unicellular Organisms / Isolated Cancer Cells** | ✅ | ✅ | **✅ Satisfied** | Passes Tier-1 with minimal local feedback; $C_{\max}$ exponentially lower, unnamed 1st-order readouts. |
| **Mitochondria (Endosymbiotic Organelles)** | 🔶 | 🔶 | **🔶 Indeterminate** | Embedded structure; boundary and metabolism depend on the host cell. |
| **Free Viral Particles** | ❌ | **—** | **❌ Unsatisfied** | Lacks independent metabolism and intrinsic repair; short-circuited at Tier-1. |
| **Flames / Bénard Convection Cells** | ❌ | **—** | **❌ Unsatisfied** | Passive thermal relaxation, not intrinsic feedback repair; intercepted at Tier-1. |
| **Lookup Table (Blockhead)** | ❌ | **—** | **❌ Unsatisfied** | Computational content causally decoupled from physical self-maintenance. |
| **Contemporary Frontier LLMs** | ❌ | **—** | **❌ Unsatisfied** | Token computation does not participate in a physical self-repair loop for silicon hardware. |
| **Macro-organizations (States / Corporations)** | ✅ | 🔶 | **🔶 Indeterminate** | Passes broad allopoietic admission, but exhibits an orders-of-magnitude gap in latency (hours vs. milliseconds) and bandwidth relative to neural systems. No hard numerical coupling threshold is preset, so the verdict converges to Indeterminate rather than a dogmatic ❌. |
| **Future Self-Maintaining Autonomous AI** | 🔶 | 🔶 | **🔶 Indeterminate** | Open conditional state: satisfied iff future hardware closes the intrinsic self-repair loop and meets Tier-2. |

**Derivation state machine (R0–R5).** Every record resolves to exactly one of six rules over the 8 legal `(tier_1_status, r4_flag, tier_2_status)` triples: `R0-short-circuit` → `Unsatisfied` · `R1-admission-failure-soft` → `Indeterminate` · `R2-all-admitted-strong-realization` → `Satisfied` · `R3-admitted-weak-realization` → `Indeterminate` · `R4-no-threshold-no-veto` → `Indeterminate` · `R5-admitted-realization-blocked` → `Unsatisfied`. Since v3.3, **R4 shares the `(Satisfied, Indeterminate)` cell with R3 and exists only as a reason annotation on that cell** — it is not an independent verdict path.

## Repository Structure
- `docs/paper_en.md` — Full English commentary paper (v3.3).
- `docs/paper_cn.md` — Full Chinese commentary paper (v3.3 中文定稿).
- `protocol/sentience_eval_schema.json` — Strict Draft-07 JSON schema enforcing Tier-1 short-circuiting (R0), Kleene tri-valued conjunction, the R0–R5 derivation state machine, and R4 non-veto rules.
- `tools/score.py` — Companion CLI validator enforcing what static JSON Schema cannot: regex-based Epistemic Hygiene Linter (scanning `evidence` strings for prohibited teleological/absolute terms) and Tier-2 coherence floors.
- `audit_rules/.cursorrules` — Epistemic Linguistic Hygiene Linter rules for Cursor / Claude / LLM research agents (English & Chinese).
- `examples/*.json` — Three canonical records, one per verdict (Satisfied / Indeterminate / Unsatisfied).
- `tests/selftest.py` — Self-test harness; generates fixtures and asserts validator behaviour.

**Tier-2 is a checklist, not a metric.** This repository prescribes no weighting, no pass threshold and no minimum-count rule for the 14 indicators. What the validator checks is a *coherence floor*: a declared Tier-2 status may not contradict a unanimous indicator vector. Assigning that status remains a human judgement.

## Quick Start: Running an Audit
`tools/score.py` runs out-of-the-box with **zero external dependencies** on Python 3.7+ (and automatically pairs with `jsonschema` Draft-07 validation if installed):
```bash
# zero-dependency mode
python tools/score.py examples/02_macro_organization_R4_Indeterminate.json

# with jsonschema installed, to also run Draft-07 validation
python tools/score.py protocol/sentience_eval_schema.json examples/01_awake_human_R2_Satisfied.json
```

Exit codes: `0` accepted · `1` rejected or file error · `2` bad CLI usage.

## Running the Tests
```bash
python tests/selftest.py
```
This generates all fixtures into `tests/cases/` (git-ignored) and rewrites the three records in `examples/`, then runs 24 fixtures, 10 schema-integrity checks, 10 assertions and 5 jsonschema-integration checks. Two of them are regression guards: the v3.2-era macro-organization record must now be **rejected**, and a record using the approved conditional-disposition phrasing (`在一定条件下…`) must **pass**.

> ⚠️ Real Draft-07 semantics are only exercised when `jsonschema` is installed; otherwise the harness verifies the integration contract via an injected stub.

## Changes in v3.3 (breaking)
Records written against the `v3.2` schema will be **rejected** by the v3.3 validator.
1. `protocol_version` const is now `"v3.3"` (the `v` prefix follows the convention already used by the v3.2 schema).
2. **R4 realigned** — `rule_r4_magnitude_gap_without_threshold = true` now requires `tier_2_status = "Indeterminate"`, **not** `"Unsatisfied"`, and additionally requires `tier_1_status = "Satisfied"`.
3. **Rule enum normalised** — the mixed `X1-` / `X4-` / `X5-` naming is replaced by consistent `R1-` / `R4-` / `R5-` names, matching `tools/score.py`.
4. `indicators` is now **required** whenever Tier-1 does not fail, and the full 14-key set is required within it.
5. The **R0 side-condition** and the **full R0–R5 state machine** are now expressed in the schema.
6. **Tier-2 weighting and thresholds removed** from `tools/score.py` (see the note under Repository Structure).

## Known Limitations
- §3.2 of the paper (the receptor-saturation intensity model) is not representable in the schema and is not validated.
- The scope limitation on the dual falsification criteria ("applies only to systems capable of reporting") has no corresponding field in the schema.
- The Epistemic Hygiene blacklists are pattern-based. Negative lookarounds cover the known false positives (`一定条件`, `一定程度`, `不一定`, `绝对值`, `not necessarily`), but a determined author can evade any regex.
