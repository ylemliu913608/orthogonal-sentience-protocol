#!/usr/bin/env python3
"""
tools/score.py — Standalone & Schema-Backed Validator for the v3.3 Orthogonal Sentience Protocol.

Enforces:
  1. Windows GBK/UTF-8 console safety out of the box.
  2. Zero-dependency fallback: uses `jsonschema` if installed, plus a built-in native
     structural & state-machine validator running on any bare Python 3.7+ environment.
  3. Kleene tri-valued conjunction for Tier-1 and the 6-branch derivation state machine
     over the 8 legal (tier_1_status, rule_r4_flag, tier_2_status) triples:

       R0-short-circuit                    t1=Unsatisfied                          -> Unsatisfied
       R1-admission-failure-soft           t1=Indeterminate                        -> Indeterminate
       R2-all-admitted-strong-realization  t1=Satisfied, t2=Satisfied              -> Satisfied
       R3-admitted-weak-realization        t1=Satisfied, t2=Indeterminate          -> Indeterminate
       R4-no-threshold-no-veto             t1=Satisfied, t2=Indeterminate, r4=true -> Indeterminate
       R5-admitted-realization-blocked     t1=Satisfied, t2=Unsatisfied            -> Unsatisfied

     NOTE ON R4: since 3.3, R4 shares the (Satisfied, Indeterminate) cell with R3 and
     exists ONLY as a REASON ANNOTATION on that cell (recording that the Tier-2 judgement
     is indeterminate because a magnitude gap was observed without a preset numerical
     threshold). It is not an independent verdict path. Under 3.2 this branch wrongly
     required tier_2_status == "Unsatisfied"; that requirement is removed.

  4. Tier-2 is NOT scored. The protocol specifies no aggregation rule, therefore this tool
     performs COHERENCE CHECKING ONLY: it verifies that a declared Tier-2 status does not
     contradict a unanimous indicator vector. There is no weighted score, no pass
     threshold, no indicator weighting, and no minimum-count rule -- any such numbers would
     be normative content the protocol does not contain.

  5. Recursive Epistemic Linguistic Hygiene Linter over ALL strings (EN + CN blacklists).

Usage:
    python3 score.py <case.json> [<schema.json>]
    python3 score.py --help

Exit codes: 0 = accepted, 1 = rejected or file error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Fix Windows GBK console crash on Unicode symbols
# ---------------------------------------------------------------------------
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# 2. Optional jsonschema import with graceful fallback
# ---------------------------------------------------------------------------
try:
    import jsonschema as _jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    _jsonschema = None
    HAS_JSONSCHEMA = False

# NOTE: the "v" prefix follows the convention already established by the repository's
# published schema (`protocol_version.const = "v3.2"`), so the bump is v3.2 -> v3.3
# rather than a change of convention.
PROTOCOL_VERSION = "v3.3"

TRI_VALUES = frozenset({"Satisfied", "Indeterminate", "Unsatisfied"})
T2_STATUS_VALUES = TRI_VALUES | {"Not_Evaluated_Short_Circuited"}

DERIVATION_RULES = frozenset({
    "R0-short-circuit",
    "R1-admission-failure-soft",
    "R2-all-admitted-strong-realization",
    "R3-admitted-weak-realization",
    "R4-no-threshold-no-veto",
    "R5-admitted-realization-blocked",
})

INDICATOR_KEYS = frozenset({
    "RPT_1", "RPT_2",
    "GWT_1", "GWT_2", "GWT_3", "GWT_4",
    "HOT_1", "HOT_2", "HOT_3", "HOT_4",
    "AST_1", "PP_1",
    "AE_1", "AE_2",
})
AE_INDICATORS = frozenset({"AE_1", "AE_2"})

# ---------------------------------------------------------------------------
# EH-1 (Teleological) & EH-2 (Cross-layer Absolute) blacklist patterns.
#
# NOTE ON NEGATIVE LOOKAROUNDS: the guards below exist to avoid flagging the very
# conditional-disposition formulations that EH-1 *requires*.
#   "在一定条件下..."   is the approved style -> must NOT fire on "一定"
#   "不一定"            is a hedge, not an absolute -> must NOT fire
#   "绝对值"            is a mathematical term -> must NOT fire
#   "not necessarily"   is a hedge, not an absolute -> must NOT fire
# ---------------------------------------------------------------------------
PROHIBITED_PATTERNS = (
    # --- teleological (EH-1) ---
    r"\bin order to\b",
    r"\bactively wants?\b",
    r"\bstrives? to\b",
    r"\bfor the purpose of\b",
    r"\bdesigned to\b",
    r"为了",
    r"主动想要",
    r"努力维持",
    # --- cross-layer absolutes (EH-2) ---
    r"(?<!not )\bnecessarily\b",
    r"\babsolutely\b",
    r"\binevitably\b",
    r"必然",
    r"绝对(?!值)",
    r"(?<!不)一定(?!条件|程度)",
)


# ---------------------------------------------------------------------------
# Criterion-level validation
# ---------------------------------------------------------------------------
def validate_criterion_obj(obj, path, require_passive_exclusion=False, require_teleology_stripped=False):
    """Validate one criterion object: exact key set, tri-valued status, evidence length."""
    errors = []
    if not isinstance(obj, dict):
        return [f"[Structure] {path} must be an object."]

    allowed_keys = {"status", "evidence"}
    if require_passive_exclusion:
        allowed_keys.add("excludes_passive_relaxation")
    if require_teleology_stripped:
        allowed_keys.add("teleology_stripped")

    extra_keys = set(obj.keys()) - allowed_keys
    if extra_keys:
        errors.append(f"[Structure] Unexpected properties at {path}: {sorted(extra_keys)}")
    for missing in sorted(allowed_keys - set(obj.keys())):
        errors.append(f"[Structure] Missing required property at {path}: {missing}")

    if "status" in obj and obj["status"] not in TRI_VALUES:
        errors.append(
            f"[Structure] {path}.status must be one of {sorted(TRI_VALUES)}, got {obj['status']!r}."
        )

    if "evidence" in obj:
        ev = obj["evidence"]
        if not isinstance(ev, str) or len(ev.strip()) < 10:
            errors.append(f"[Evidence] {path}.evidence must be a non-empty string of at least 10 characters.")

    # Flag checks fire only when the key is present (a missing key already reported above),
    # so a single defect is never reported twice.
    if require_passive_exclusion and "excludes_passive_relaxation" in obj:
        if obj["excludes_passive_relaxation"] is not True:
            errors.append(f"[Rule] {path}.excludes_passive_relaxation must be explicitly set to true.")

    if require_teleology_stripped and "teleology_stripped" in obj:
        if obj["teleology_stripped"] is not True:
            errors.append(f"[EH-1 Rule] {path}.teleology_stripped must be explicitly set to true.")

    return errors


# ---------------------------------------------------------------------------
# Native structural + state-machine validator (zero dependency)
# ---------------------------------------------------------------------------
def validate_native_structure_and_rules(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["[Structure] Root document must be a JSON object."]

    required_top = {
        "protocol_version",
        "target_system",
        "boundary_granularity_declaration",
        "tier_1_admission",
        "tier_2_realization",
        "rule_r4_magnitude_gap_without_threshold",
        "verdict_derivation_rule",
        "final_verdict",
    }
    extra_top = set(doc.keys()) - required_top
    if extra_top:
        errors.append(f"[Structure] Unexpected root properties: {sorted(extra_top)}")
    missing_top = required_top - set(doc.keys())
    if missing_top:
        errors.append(f"[Structure] Missing required root properties: {sorted(missing_top)}")
        return errors

    if doc.get("protocol_version") != PROTOCOL_VERSION:
        errors.append(
            f"[Version] protocol_version must be {PROTOCOL_VERSION!r}, got {doc.get('protocol_version')!r}."
        )

    if not isinstance(doc.get("target_system"), str) or len(doc["target_system"].strip()) < 2:
        errors.append("[Structure] target_system must be a string of length >= 2.")

    bgd = doc.get("boundary_granularity_declaration")
    if not isinstance(bgd, str) or len(bgd.strip()) < 15:
        errors.append("[Granularity] boundary_granularity_declaration must be a string of length >= 15.")

    r4_flag = doc.get("rule_r4_magnitude_gap_without_threshold")
    if not isinstance(r4_flag, bool):
        errors.append("[Structure] rule_r4_magnitude_gap_without_threshold must be a boolean.")

    rule = doc.get("verdict_derivation_rule")
    if rule not in DERIVATION_RULES:
        errors.append(
            f"[Rule] verdict_derivation_rule must be one of {sorted(DERIVATION_RULES)}, got {rule!r}."
        )

    final_verdict = doc.get("final_verdict")
    if final_verdict not in TRI_VALUES:
        errors.append(f"[Structure] final_verdict must be one of {sorted(TRI_VALUES)}, got {final_verdict!r}.")

    # ---------------- Tier-1 ----------------
    t1 = doc.get("tier_1_admission")
    if not isinstance(t1, dict):
        return errors + ["[Structure] tier_1_admission must be an object."]

    req_t1 = {"boundary", "metabolic_throughput", "intrinsic_homeostatic_repair", "tier_1_status"}
    extra_t1 = set(t1.keys()) - req_t1
    if extra_t1:
        errors.append(f"[Structure] Unexpected properties in tier_1_admission: {sorted(extra_t1)}")
    missing_t1 = req_t1 - set(t1.keys())
    if missing_t1:
        errors.append(f"[Structure] Missing required properties in tier_1_admission: {sorted(missing_t1)}")
        return errors

    errors.extend(validate_criterion_obj(t1["boundary"], "tier_1_admission.boundary"))
    errors.extend(validate_criterion_obj(t1["metabolic_throughput"], "tier_1_admission.metabolic_throughput"))
    errors.extend(validate_criterion_obj(
        t1["intrinsic_homeostatic_repair"],
        "tier_1_admission.intrinsic_homeostatic_repair",
        require_passive_exclusion=True,
    ))

    t1_status = t1.get("tier_1_status")
    if t1_status not in TRI_VALUES:
        errors.append(f"[Structure] tier_1_status must be one of {sorted(TRI_VALUES)}, got {t1_status!r}.")

    # Kleene strong conjunction: Unsatisfied dominates; all-Satisfied => Satisfied; else Indeterminate.
    c_statuses = [
        t1[k].get("status") if isinstance(t1.get(k), dict) else None
        for k in ("boundary", "metabolic_throughput", "intrinsic_homeostatic_repair")
    ]
    if all(s in TRI_VALUES for s in c_statuses):
        if "Unsatisfied" in c_statuses:
            expected_t1 = "Unsatisfied"
        elif all(s == "Satisfied" for s in c_statuses):
            expected_t1 = "Satisfied"
        else:
            expected_t1 = "Indeterminate"
        if t1_status != expected_t1:
            errors.append(
                f"[Tier-1 Kleene Conjunction Error] Criterion statuses are {c_statuses}, which requires "
                f"tier_1_status='{expected_t1}', but got '{t1_status}'."
            )

    # ---------------- Tier-2 ----------------
    t2 = doc.get("tier_2_realization")
    if not isinstance(t2, dict):
        return errors + ["[Structure] tier_2_realization must be an object."]

    allowed_t2 = {"tier_2_status", "indicators"}
    extra_t2 = set(t2.keys()) - allowed_t2
    if extra_t2:
        errors.append(f"[Structure] Unexpected properties in tier_2_realization: {sorted(extra_t2)}")

    t2_status = t2.get("tier_2_status")
    if t2_status not in T2_STATUS_VALUES:
        errors.append(f"[Structure] tier_2_status invalid: {t2_status!r}.")

    # ---------------- Cross-tier state machine ----------------
    if t1_status not in TRI_VALUES or t2_status not in T2_STATUS_VALUES or not isinstance(r4_flag, bool):
        return errors  # upstream structural errors already reported; do not cascade

    if t1_status == "Unsatisfied":
        # ---- R0: short-circuit ----
        if t2_status != "Not_Evaluated_Short_Circuited":
            errors.append(
                "[R0 Short-Circuit Violation] When tier_1_status is 'Unsatisfied', tier_2_status "
                f"MUST be 'Not_Evaluated_Short_Circuited', got '{t2_status}'."
            )
        if "indicators" in t2:
            errors.append("[R0 Short-Circuit Violation] 'indicators' must be omitted when Tier-1 is short-circuited.")
        if r4_flag is not False:
            errors.append(
                "[R0 Short-Circuit Violation] rule_r4_magnitude_gap_without_threshold must be false when short-circuited."
            )
        if rule != "R0-short-circuit":
            errors.append(f"[R0 Rule Violation] verdict_derivation_rule must be 'R0-short-circuit', got '{rule}'.")
        if final_verdict != "Unsatisfied":
            errors.append(f"[R0 Verdict Violation] final_verdict must be 'Unsatisfied' on Tier-1 failure, got '{final_verdict}'.")
    else:
        # ---- Tier-1 admitted (Satisfied or Indeterminate): Tier-2 must be evaluated ----
        if t2_status == "Not_Evaluated_Short_Circuited":
            errors.append("[Tier-2 Violation] Cannot short-circuit Tier-2 when tier_1_status is not 'Unsatisfied'.")

        indicators = t2.get("indicators")
        if not isinstance(indicators, dict):
            errors.append("[Tier-2 Violation] 'indicators' object containing all 14 Butlin-Long indicators is required.")
        else:
            extra_ind = set(indicators.keys()) - INDICATOR_KEYS
            missing_ind = INDICATOR_KEYS - set(indicators.keys())
            if extra_ind:
                errors.append(f"[Tier-2 Structure] Unknown indicator keys: {sorted(extra_ind)}")
            if missing_ind:
                errors.append(f"[Tier-2 Structure] Missing required 14 indicators: {sorted(missing_ind)}")
            for k in sorted(INDICATOR_KEYS & set(indicators.keys())):
                errors.extend(validate_criterion_obj(
                    indicators[k],
                    f"tier_2_realization.indicators.{k}",
                    require_teleology_stripped=(k in AE_INDICATORS),
                ))

        if r4_flag is True:
            # ---- R4: no-threshold-no-veto (reason annotation on the R3 cell) ----
            if t1_status != "Satisfied":
                errors.append(
                    "[R4 Violation] rule_r4_magnitude_gap_without_threshold=true requires "
                    f"tier_1_status='Satisfied', got '{t1_status}'."
                )
            if t2_status != "Indeterminate":
                errors.append(
                    "[R4 Violation] rule_r4_magnitude_gap_without_threshold=true is only valid when "
                    f"tier_2_status is 'Indeterminate', got '{t2_status}'."
                )
            if rule != "R4-no-threshold-no-veto":
                errors.append(f"[R4 Rule Violation] verdict_derivation_rule must be 'R4-no-threshold-no-veto', got '{rule}'.")
            if final_verdict != "Indeterminate":
                errors.append(
                    "[R4 Verdict Violation] Without a preset numerical threshold, a magnitude gap MUST converge to "
                    f"final_verdict='Indeterminate', got '{final_verdict}'."
                )
        elif t1_status == "Indeterminate":
            # ---- R1 ----
            if rule != "R1-admission-failure-soft":
                errors.append(
                    "[R1 Rule Violation] When tier_1_status is 'Indeterminate' and R4=false, "
                    f"verdict_derivation_rule must be 'R1-admission-failure-soft', got '{rule}'."
                )
            if final_verdict != "Indeterminate":
                errors.append(
                    f"[R1 Verdict Violation] Tier-1 'Indeterminate' MUST propagate to final_verdict='Indeterminate', got '{final_verdict}'."
                )
        elif t1_status == "Satisfied":
            if t2_status == "Satisfied":
                # ---- R2 ----
                if rule != "R2-all-admitted-strong-realization":
                    errors.append(f"[R2 Rule Violation] Expected 'R2-all-admitted-strong-realization', got '{rule}'.")
                if final_verdict != "Satisfied":
                    errors.append(f"[R2 Verdict Violation] Expected final_verdict='Satisfied', got '{final_verdict}'.")
            elif t2_status == "Indeterminate":
                # ---- R3 ----
                if rule != "R3-admitted-weak-realization":
                    errors.append(f"[R3 Rule Violation] Expected 'R3-admitted-weak-realization', got '{rule}'.")
                if final_verdict != "Indeterminate":
                    errors.append(f"[R3 Verdict Violation] Expected final_verdict='Indeterminate', got '{final_verdict}'.")
            elif t2_status == "Unsatisfied":
                # ---- R5 ----
                if rule != "R5-admitted-realization-blocked":
                    errors.append(f"[R5 Rule Violation] Expected 'R5-admitted-realization-blocked', got '{rule}'.")
                if final_verdict != "Unsatisfied":
                    errors.append(f"[R5 Verdict Violation] Expected final_verdict='Unsatisfied', got '{final_verdict}'.")

    return errors


# ---------------------------------------------------------------------------
# Tier-2 coherence floors (NO scoring, NO thresholds, NO weights)
# ---------------------------------------------------------------------------
def check_tier2_coherence(doc):
    """
    The protocol defines no Tier-2 aggregation rule, so this function issues no score and
    applies no numeric threshold. It checks only logical coherence: a declared Tier-2 status
    must not contradict a unanimous indicator vector.
    """
    errors = []
    t2 = doc.get("tier_2_realization")
    if not isinstance(t2, dict):
        return errors
    t2_status = t2.get("tier_2_status")
    if t2_status == "Not_Evaluated_Short_Circuited" or t2_status not in TRI_VALUES:
        return errors

    indicators = t2.get("indicators")
    if not isinstance(indicators, dict) or set(indicators.keys()) != INDICATOR_KEYS:
        return errors

    statuses = []
    for k in sorted(INDICATOR_KEYS):
        v = indicators.get(k)
        if not isinstance(v, dict) or v.get("status") not in TRI_VALUES:
            return errors
        statuses.append(v["status"])

    n_total = len(statuses)
    n_sat = statuses.count("Satisfied")
    n_uns = statuses.count("Unsatisfied")

    if t2_status == "Satisfied" and n_sat == 0:
        errors.append(
            "[Tier-2 Coherence Floor] tier_2_status='Satisfied' contradicts a unanimous 'Unsatisfied' "
            f"indicator vector (0/{n_total} satisfied)."
        )
    elif t2_status == "Unsatisfied" and n_uns == 0:
        errors.append(
            "[Tier-2 Coherence Floor] tier_2_status='Unsatisfied' contradicts a unanimous 'Satisfied' "
            f"indicator vector ({n_total}/{n_total} satisfied)."
        )
    elif t2_status == "Indeterminate" and (n_sat == n_total or n_uns == n_total):
        unanimous = "Satisfied" if n_sat == n_total else "Unsatisfied"
        errors.append(
            f"[Tier-2 Coherence Floor] tier_2_status='Indeterminate' contradicts a unanimous '{unanimous}' "
            f"indicator vector ({n_total}/{n_total})."
        )
    return errors


# ---------------------------------------------------------------------------
# Epistemic Linguistic Hygiene linter (recurses over dicts, lists AND bare strings)
# ---------------------------------------------------------------------------
def check_epistemic_hygiene(obj, path="root"):
    errors = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(check_epistemic_hygiene(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            errors.extend(check_epistemic_hygiene(item, f"{path}[{idx}]"))
    elif isinstance(obj, str):
        for pat in PROHIBITED_PATTERNS:
            if re.search(pat, obj, re.IGNORECASE):
                errors.append(f"[EH-Violation] Prohibited term matching '{pat}' at {path}: {obj!r}")
    return errors


# ---------------------------------------------------------------------------
# Shared error collection (used by both the CLI and the self-test harness)
# ---------------------------------------------------------------------------
def collect_errors(doc, schema=None):
    errors = []

    # Engine 1: Draft-07 jsonschema (only when installed AND a schema is supplied).
    # iter_errors() is used so that ALL schema violations are reported, matching the
    # diagnostic granularity of the native engine.
    if HAS_JSONSCHEMA and isinstance(schema, dict):
        validator = _jsonschema.Draft7Validator(schema)
        for e in sorted(validator.iter_errors(doc), key=lambda x: list(x.absolute_path)):
            path_str = ".".join(str(p) for p in e.absolute_path) or "root"
            errors.append(f"[Schema Error @ {path_str}] {e.message}")

    # Engine 2: native structural + R0-R5 state machine
    errors.extend(validate_native_structure_and_rules(doc))

    # Engine 3: Tier-2 coherence floors + Epistemic Hygiene linter
    errors.extend(check_tier2_coherence(doc))
    errors.extend(check_epistemic_hygiene(doc))

    # De-duplicate, preserving order
    seen = set()
    return [x for x in errors if not (x in seen or seen.add(x))]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate a sentience evaluation JSON record against Protocol 3.3 structure, "
            "the R0-R5 derivation state machine, Tier-2 coherence floors, and Epistemic Hygiene. "
            "Tier-2 is not scored: no weighting, no threshold."
        )
    )
    parser.add_argument("schema", nargs="?", help="Path to sentience_eval_schema.json (optional; used only when jsonschema is installed)")
    parser.add_argument("case", help="Path to the evaluation case JSON file")
    parser.add_argument("--quiet", action="store_true", help="Suppress the success banner (violations are still printed)")
    args = parser.parse_args()

    schema = None
    if args.schema:
        try:
            schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"❌ [SCHEMA ERROR]: Failed to load schema {args.schema!r}: {e}")
            sys.exit(1)

    try:
        doc = json.loads(Path(args.case).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ [FILE ERROR]: Failed to load case {args.case!r}: {e}")
        sys.exit(1)

    all_errors = collect_errors(doc, schema)

    if all_errors:
        print(f"❌ [REJECTED] {args.case} ({len(all_errors)} violation(s) found):")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)

    if not args.quiet:
        engines = "jsonschema+native" if (HAS_JSONSCHEMA and schema is not None) else "native-zero-dep"
        t1s = doc.get("tier_1_admission", {}).get("tier_1_status")
        t2s = doc.get("tier_2_realization", {}).get("tier_2_status")
        print(
            f"✅ [ACCEPTED | {engines}] Target: {doc.get('target_system')} | "
            f"Tier-1: {t1s} | Tier-2: {t2s} | "
            f"Final Verdict: {doc.get('final_verdict')} ({doc.get('verdict_derivation_rule')})"
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
