#!/usr/bin/env python3
"""
tests/selftest.py — Self-test harness for the v3.3 Orthogonal Sentience Protocol.

Run:  python3 tests/selftest.py

Fixtures are GENERATED (deterministic), not hand-maintained:
  - tests/cases/*.json   all fixtures, including the negative ones  [git-ignored]
  - examples/*.json      the three canonical records for humans     [committed]

Covers:
  A. All six derivation branches (R0-R5) on well-formed records.
  B. Rejection of malformed records (structure, short-circuit, coherence floor, hygiene).
  C. Regression: the v3.2-era macro-organization record MUST now be rejected
     (proves the R4 realignment took effect).
  D. Regression: approved conditional-disposition phrasing must NOT be flagged
     (proves the CN blacklist no longer fires on the phrasing the protocol mandates).
  E. Schema integrity: the shipped schema must not drift from the validator's constants.
  F. Engine-1 code path: jsonschema integration contract, exercised via an injected stub.
"""

import copy
import importlib
import itertools
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

CASES_DIR = ROOT / "tests" / "cases"
EXAMPLES_DIR = ROOT / "examples"
SCHEMA_PATH = ROOT / "protocol" / "sentience_eval_schema.json"

ALL_INDICATORS = sorted(
    "RPT_1 RPT_2 GWT_1 GWT_2 GWT_3 GWT_4 HOT_1 HOT_2 HOT_3 HOT_4 AST_1 PP_1 AE_1 AE_2".split()
)
AE_INDICATORS = {"AE_1", "AE_2"}

# Fixtures that are also published as human-readable examples.
EXAMPLE_NAMES = {
    "A1_R2_awake_human": "01_awake_human_R2_Satisfied.json",
    "A4_R4_macro_organization": "02_macro_organization_R4_Indeterminate.json",
    "A2_R5_anesthesia": "03_general_anesthesia_R5_Unsatisfied.json",
}


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------
def crit(status, note):
    return {"status": status, "evidence": f"{note}: observed structural features and sustained throughput satisfying this criterion."}


def crit_repair(status, note):
    d = crit(status, note)
    d["excludes_passive_relaxation"] = True
    return d


def crit_ae(status, note):
    d = crit(status, note)
    d["teleology_stripped"] = True
    return d


def t1_block(s, m, r):
    return {
        "boundary": crit(s, "boundary criterion"),
        "metabolic_throughput": crit(m, "metabolic-throughput criterion"),
        "intrinsic_homeostatic_repair": crit_repair(r, "intrinsic-repair criterion"),
        "tier_1_status": (
            "Unsatisfied" if "Unsatisfied" in (s, m, r)
            else "Satisfied" if s == m == r == "Satisfied"
            else "Indeterminate"
        ),
    }


def t2_indicators(vector):
    out = {}
    for k in ALL_INDICATORS:
        st = vector[k] if isinstance(vector, dict) else vector
        out[k] = crit_ae(st, f"{k} criterion") if k in AE_INDICATORS else crit(st, f"{k} criterion")
    return out


def record(target, t1_status, t2_status, verdict, rule, r4=False, vector="Satisfied", bgd=None):
    rec = {
        "protocol_version": "v3.3",
        "target_system": target,
        "boundary_granularity_declaration": bgd or "All judgements in this record are made at the granularity of the target system's own current statistical boundary.",
        "tier_1_admission": t1_block(t1_status, t1_status, t1_status),
        "tier_2_realization": {"tier_2_status": t2_status},
        "rule_r4_magnitude_gap_without_threshold": r4,
        "verdict_derivation_rule": rule,
        "final_verdict": verdict,
    }
    if t2_status != "Not_Evaluated_Short_Circuited":
        rec["tier_2_realization"]["indicators"] = t2_indicators(vector)
    return rec


def mixed_majority_satisfied():
    v = {k: "Satisfied" for k in ALL_INDICATORS}
    v["GWT_4"] = "Unsatisfied"
    v["HOT_3"] = "Indeterminate"
    return v


def build_cases():
    cases = {}

    # ---- A. six derivation branches ----
    cases["A1_R2_awake_human"] = (
        record("Awake human / mammal", "Satisfied", "Satisfied", "Satisfied",
               "R2-all-admitted-strong-realization"), True)
    cases["A2_R5_anesthesia"] = (
        record("Human under general anesthesia", "Satisfied", "Unsatisfied", "Unsatisfied",
               "R5-admitted-realization-blocked", vector="Unsatisfied"), True)
    cases["A3_R3_covert_consciousness"] = (
        record("Covert consciousness / vegetative patient", "Satisfied", "Indeterminate", "Indeterminate",
               "R3-admitted-weak-realization", vector=mixed_majority_satisfied()), True)
    cases["A4_R4_macro_organization"] = (
        record("Macro-organization (state / corporation)", "Satisfied", "Indeterminate", "Indeterminate",
               "R4-no-threshold-no-veto", r4=True, vector=mixed_majority_satisfied()), True)
    cases["A5_R1_mitochondria"] = (
        record("Mitochondria (endosymbiotic organelle)", "Indeterminate", "Indeterminate", "Indeterminate",
               "R1-admission-failure-soft", vector="Indeterminate"), True)
    cases["A6_R0_frontier_llm"] = (
        record("Contemporary frontier LLM", "Unsatisfied", "Not_Evaluated_Short_Circuited", "Unsatisfied",
               "R0-short-circuit"), True)

    # ---- B. malformed records ----
    cases["B01_shortcircuit_not_applied"] = (
        record("Contemporary frontier LLM", "Unsatisfied", "Unsatisfied", "Unsatisfied",
               "R0-short-circuit", vector="Unsatisfied"), False)

    cases["B02_floor_satisfied_all_unsat"] = (
        record("Awake human / mammal", "Satisfied", "Satisfied", "Satisfied",
               "R2-all-admitted-strong-realization", vector="Unsatisfied"), False)
    cases["B03_floor_unsat_all_sat"] = (
        record("Awake human / mammal", "Satisfied", "Unsatisfied", "Unsatisfied",
               "R5-admitted-realization-blocked", vector="Satisfied"), False)
    cases["B04_floor_indet_unanimous"] = (
        record("Awake human / mammal", "Satisfied", "Indeterminate", "Indeterminate",
               "R3-admitted-weak-realization", vector="Satisfied"), False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["intrinsic_homeostatic_repair"].pop("excludes_passive_relaxation")
    cases["B05_missing_passive_flag"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_2_realization"]["indicators"]["AE_1"]["teleology_stripped"] = False
    cases["B06_ae_teleology_not_stripped"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["intrinsic_homeostatic_repair"]["evidence"] = \
        "The cell actively repairs itself in order to survive."
    cases["B07_eh_teleological_en"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["boundary"]["evidence"] = "该系统必然呈现出统计边界，这是绝对确定的。"
    cases["B08_eh_absolute_cn"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["boundary"]["evidence"] = "The system necessarily exhibits a statistical boundary."
    cases["B09_eh_absolute_en"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["tier_1_status"] = "Indeterminate"
    cases["B10_kleene_violation"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["protocol_version"] = "v3.2"
    cases["B11_wrong_version"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_2_realization"]["indicators"].pop("HOT_4")
    cases["B12_missing_indicator"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_2_realization"]["indicators"]["RPT_1"]["status"] = "Probably"
    cases["B13_bad_tri_value"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["tier_1_admission"]["boundary"]["evidence"] = "too short"
    cases["B14_short_evidence"] = (bad, False)

    bad = record("Test system", "Indeterminate", "Indeterminate", "Indeterminate", "R1-admission-failure-soft")
    bad["rule_r4_magnitude_gap_without_threshold"] = True
    cases["B15_r4_with_indeterminate_tier1"] = (bad, False)

    bad = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    bad["extra_field"] = "unexpected"
    cases["B16_unexpected_root_key"] = (bad, False)

    # ---- C. regression: the v3.2-era macro record must now be rejected ----
    cases["C1_regression_v32_macro_record"] = (
        record("Macro-organization (state / corporation)", "Satisfied", "Unsatisfied", "Indeterminate",
               "R4-no-threshold-no-veto", r4=True, vector=mixed_majority_satisfied()), False)

    # ---- D. regression: approved conditional-disposition phrasing must pass ----
    ok = record("Test system", "Satisfied", "Satisfied", "Satisfied", "R2-all-admitted-strong-realization")
    ok["tier_1_admission"]["intrinsic_homeostatic_repair"]["evidence"] = \
        "在一定条件下，该系统结构以高概率呈现出损伤后重建现象。"
    ok["tier_1_admission"]["boundary"]["evidence"] = \
        "在给定条件下观测到边界维持现象，且并不一定需要外部梯度驱动。"
    ok["tier_1_admission"]["metabolic_throughput"]["evidence"] = \
        "跨边界通量的绝对值维持在可观测区间内，与温度呈一定程度的相关。"
    cases["D1_approved_phrasing_not_flagged"] = (ok, True)

    return cases


# ---------------------------------------------------------------------------
# State-space enumeration
# ---------------------------------------------------------------------------
def enumerate_legal_triples():
    t1s = ["Satisfied", "Indeterminate", "Unsatisfied"]
    t2s = ["Satisfied", "Indeterminate", "Unsatisfied", "Not_Evaluated_Short_Circuited"]
    rules = sorted(score.DERIVATION_RULES)
    verdicts = ["Satisfied", "Indeterminate", "Unsatisfied"]
    legal = []
    total = 0
    for t1, t2, r4, rule, verdict in itertools.product(t1s, t2s, [False, True], rules, verdicts):
        total += 1
        rec = record("probe", t1, t2, verdict, rule, r4=r4,
                     vector="Indeterminate" if t2 != "Not_Evaluated_Short_Circuited" else "Satisfied")
        if score.validate_native_structure_and_rules(rec):
            continue
        legal.append((t1, r4, t2, rule, verdict))
    return legal, total


# ---------------------------------------------------------------------------
# Schema integrity
# ---------------------------------------------------------------------------
def schema_integrity(schema):
    results = []
    results.append(("schema is well-formed JSON object", isinstance(schema, dict)))
    results.append(("declares Draft-07", schema.get("$schema", "").endswith("draft-07/schema#")))

    props = schema.get("properties", {})
    defs = schema.get("definitions", {})

    def deref(node):
        """Follow a local #/definitions/... $ref one or more levels."""
        seen = 0
        while isinstance(node, dict) and "$ref" in node and seen < 8:
            ref = node["$ref"]
            if not ref.startswith("#/definitions/"):
                return {}
            node = defs.get(ref[len("#/definitions/"):], {})
            seen += 1
        return node if isinstance(node, dict) else {}

    results.append(("protocol_version pinned to v3.3",
                    props.get("protocol_version", {}).get("const") == "v3.3"))

    schema_rules = set(defs.get("derivation_rule", {}).get("enum", []))
    results.append(("schema rule enum == score.DERIVATION_RULES",
                    schema_rules == set(score.DERIVATION_RULES)))
    if schema_rules != set(score.DERIVATION_RULES):
        results.append((f"  only-in-schema={sorted(schema_rules - set(score.DERIVATION_RULES))} "
                        f"only-in-validator={sorted(set(score.DERIVATION_RULES) - schema_rules)}", False))

    t2_schema = deref(props.get("tier_2_realization", {})).get("properties", {}).get("indicators", {})
    schema_keys = set(t2_schema.get("properties", {}).keys())
    results.append((f"schema indicator set == score.INDICATOR_KEYS ({len(schema_keys)} keys)",
                    schema_keys == set(score.INDICATOR_KEYS)))
    if schema_keys != set(score.INDICATOR_KEYS):
        results.append((f"  only-in-schema={sorted(schema_keys - set(score.INDICATOR_KEYS))} "
                        f"only-in-validator={sorted(set(score.INDICATOR_KEYS) - schema_keys)}", False))
    results.append(("schema requires all 14 indicators",
                    set(t2_schema.get("required", [])) == set(score.INDICATOR_KEYS)))

    ae_refs = {k for k, v in t2_schema.get("properties", {}).items()
               if v.get("$ref", "").endswith("criterion_and_teleology")}
    results.append(("schema marks exactly AE_1/AE_2 as criterion_and_teleology",
                    ae_refs == set(score.AE_INDICATORS)))

    repair_ref = (deref(props.get("tier_1_admission", {}))
                  .get("properties", {})
                  .get("intrinsic_homeostatic_repair", {})
                  .get("$ref", ""))
    results.append(("schema marks intrinsic_homeostatic_repair as criterion_and_passive",
                    repair_ref.endswith("criterion_and_passive")))

    oneof = None
    for entry in schema.get("allOf", []):
        if "oneOf" in entry:
            oneof = entry["oneOf"]
    results.append(("schema expresses the state machine via oneOf (6 disjoint branches)",
                    isinstance(oneof, list) and len(oneof) == 6))

    names = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "properties" and isinstance(v, dict):
                    names.update(v.keys())
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(schema)
    banned = {"pass_threshold", "threshold", "weight", "weights", "min_core",
              "max_unsatisfied", "score", "aggregate", "aggregation"}
    hits = sorted(n for n in names if n.lower() in banned)
    results.append((f"no aggregation/weighting property names (found={hits})", not hits))

    return results


# ---------------------------------------------------------------------------
# Engine-1 code path (stubbed jsonschema)
# ---------------------------------------------------------------------------
class _StubError:
    def __init__(self, path, message):
        self.absolute_path = list(path)
        self.message = message


class _StubDraft7Validator:
    def __init__(self, schema):
        self.schema = schema

    def iter_errors(self, doc):
        found = []

        def walk(node, path):
            if isinstance(node, dict):
                if node.get("evidence") == "TRIGGER":
                    found.append(_StubError(path + ["evidence"], "stub: evidence == 'TRIGGER'"))
                for k, v in node.items():
                    walk(v, path + [k])
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, path + [i])

        walk(doc, [])
        return found


def engine1_code_path(schema, sample):
    results = []
    stub = types.ModuleType("jsonschema")
    stub.Draft7Validator = _StubDraft7Validator
    sys.modules["jsonschema"] = stub
    sys.modules.pop("score", None)
    fresh = importlib.import_module("score")
    results.append(("HAS_JSONSCHEMA flips True with a jsonschema module present",
                    fresh.HAS_JSONSCHEMA is True))

    errs = fresh.collect_errors(sample, schema)
    results.append((f"clean record yields no Schema Error (total errors={len(errs)})",
                    not any("Schema Error" in e for e in errs)))

    bad = copy.deepcopy(sample)
    bad["tier_1_admission"]["boundary"]["evidence"] = "TRIGGER"
    errs_bad = fresh.collect_errors(bad, schema)
    schema_errs = [e for e in errs_bad if e.startswith("[Schema Error @")]
    results.append((f"stub violation surfaces as [Schema Error @ ...] (n={len(schema_errs)})",
                    len(schema_errs) == 1))
    results.append(("error path rendered as dotted absolute_path",
                    bool(schema_errs) and "tier_1_admission.boundary.evidence" in schema_errs[0]))
    results.append(("no schema supplied => Engine 1 stays silent",
                    not any("Schema Error" in e for e in fresh.collect_errors(bad, None))))

    # restore the real module state for the remaining checks
    sys.modules.pop("jsonschema", None)
    sys.modules.pop("score", None)
    importlib.import_module("score")
    return results


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main():
    global score
    score = importlib.import_module("score")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"protocol version        : {score.PROTOCOL_VERSION}")
    print(f"jsonschema available    : {score.HAS_JSONSCHEMA}")

    legal, total = enumerate_legal_triples()
    print(f"legal state space       : {len(legal)} accepted triples out of {total} enumerated")
    by_rule = {}
    for t1, r4, t2, rule, verdict in legal:
        by_rule.setdefault(rule, []).append((t1, r4, t2, verdict))
    for rule in sorted(by_rule):
        cells = sorted(set(by_rule[rule]))
        print(f"    {rule:<38} {len(cells)} cell(s): " +
              "; ".join(f"{c[0]}/{c[1]}/{c[2]}->{c[3]}" for c in cells))

    print("\n--- fixtures (generated) ---")
    cases = build_cases()
    failures = []
    for name in sorted(cases):
        rec, expect_accept = cases[name]
        (CASES_DIR / f"{name}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if name in EXAMPLE_NAMES:
            (EXAMPLES_DIR / EXAMPLE_NAMES[name]).write_text(
                json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        errs = score.collect_errors(copy.deepcopy(rec), schema)
        got_accept = not errs
        ok = (got_accept == expect_accept)
        if not ok:
            failures.append(name)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<38} "
              f"want={'accept' if expect_accept else 'reject':<6} "
              f"got={'accept' if got_accept else 'reject':<6} ({len(errs)} error(s))")
        if not ok:
            for e in errs[:4]:
                print(f"         {e}")

    print(f"\n--- examples written: {len(EXAMPLE_NAMES)} file(s) in examples/ ---")
    for src, dst in sorted(EXAMPLE_NAMES.items(), key=lambda kv: kv[1]):
        print(f"  {dst}   <- {src}")

    print("\n--- schema integrity ---")
    r_schema = schema_integrity(schema)
    for label, ok in r_schema:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        if not ok:
            failures.append(label)

    print("\n--- assertions ---")
    checks = [
        ("A4 (R4 macro) accepted under v3.3",
         not score.collect_errors(copy.deepcopy(cases["A4_R4_macro_organization"][0]), schema)),
        ("C1 (v3.2-era macro record) rejected under v3.3",
         bool(score.collect_errors(copy.deepcopy(cases["C1_regression_v32_macro_record"][0]), schema))),
        ("D1 approved phrasing not flagged",
         not score.collect_errors(copy.deepcopy(cases["D1_approved_phrasing_not_flagged"][0]), schema)),
        ("D1 produces zero hygiene violations",
         len(score.check_epistemic_hygiene(cases["D1_approved_phrasing_not_flagged"][0])) == 0),
        ("B08 fires on 必然 / 绝对",
         len(score.check_epistemic_hygiene(cases["B08_eh_absolute_cn"][0])) >= 2),
        ("B09 fires exactly once on 'necessarily'",
         len(score.check_epistemic_hygiene(cases["B09_eh_absolute_en"][0])) == 1),
        ("no scoring API remains (SCORE_MAP / INDICATOR_WEIGHTS)",
         not hasattr(score, "SCORE_MAP") and not hasattr(score, "INDICATOR_WEIGHTS")),
        ("no aggregation-threshold API remains",
         not hasattr(score, "check_tier2_aggregation")),
        ("R3 and R4 share the (Satisfied, Indeterminate) cell",
         any(t == "Satisfied" and t2 == "Indeterminate" and r is False and ru == "R3-admitted-weak-realization"
             for t, r, t2, ru, _ in legal)
         and any(t == "Satisfied" and t2 == "Indeterminate" and r is True and ru == "R4-no-threshold-no-veto"
                 for t, r, t2, ru, _ in legal)),
        ("legal state space is exactly 8 triples", len(legal) == 8),
    ]
    for label, res in checks:
        print(f"  [{'PASS' if res else 'FAIL'}] {label}")
        if not res:
            failures.append(label)

    print("\n--- Engine-1 code path (stubbed jsonschema) ---")
    r_engine = engine1_code_path(schema, cases["A1_R2_awake_human"][0])
    for label, ok in r_engine:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        if not ok:
            failures.append(label)

    print()
    if failures:
        print(f"❌ SELFTEST FAILED — {len(failures)} problem(s): {failures}")
        sys.exit(1)

    print(f"⚠️  Real Draft-07 semantics were NOT exercised (jsonschema not installed here).")
    print(f"    Run `pip install jsonschema && python3 tests/selftest.py` to cover Engine 1 fully.")
    print(f"\n✅ SELFTEST PASSED — {len(cases)} fixtures, {len(r_schema)} schema checks, "
          f"{len(checks)} assertions, {len(r_engine)} engine checks — 0 failures")
    sys.exit(0)


if __name__ == "__main__":
    main()
