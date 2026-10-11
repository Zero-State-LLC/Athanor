"""Athanor data contracts v1. Single source of truth; JSON schemas are generated from this."""
CONTRACT_VERSION = "athanor.v1"
SOURCE_KINDS = ["observed", "synthetic", "model_generated"]

# field: (spark_type, required)
CONTRACTS = {
    "sft_row": {
        "key": "record_id", "group": "family",
        "fields": {
            "record_id": ("string", True), "contract_version": ("string", True),
            "run_id": ("string", True), "family": ("string", True), "domain": ("string", False),
            "prompt": ("string", True), "target": ("string", True),
            "source_kind": ("string", True), "source_path": ("string", True),
            "source_sha256": ("string", True), "source_line": ("bigint", False),
            "generator": ("string", False), "rights": ("string", True),
            "landed_by": ("string", True), "landed_at": ("string", True),
        },
        "enums": {"source_kind": SOURCE_KINDS},
    },
    "audit_verdict": {
        # Judge verdicts are MODEL labels. Human agreement lives in its own columns and is never inferred.
        "key": "verdict_id", "group": "family",
        "fields": {
            "verdict_id": ("string", True), "contract_version": ("string", True),
            "record_id": ("string", True), "family": ("string", True), "audit_round": ("string", True),
            "candidate_model": ("string", True), "baseline_model": ("string", True),
            "judge_model": ("string", True), "judge_version": ("string", True),
            "judge_prompt_sha256": ("string", False),
            "judge_winner": ("string", True), "judge_rationale": ("string", False),
            "human_reviewed": ("boolean", True), "human_winner": ("string", False),
            "human_reviewer": ("string", False), "is_agreement_control": ("boolean", True),
            "source_path": ("string", True), "source_sha256": ("string", True),
            "landed_by": ("string", True), "landed_at": ("string", True),
        },
        "enums": {"judge_winner": ["TARGET", "BASE", "TIE"], "human_winner": ["TARGET", "BASE", "TIE", None]},
    },
    "eval_gate": {
        # Gate results are evaluation outcomes. They are NOT training labels and never join into SFT.
        "key": "eval_id", "group": None,
        "fields": {
            "eval_id": ("string", True), "contract_version": ("string", True),
            "run_id": ("string", True), "checkpoint": ("string", True), "eval_suite": ("string", True),
            "gate_id": ("string", False), "gate_spec_ref": ("string", False),
            "metric": ("string", True), "value": ("double", False), "threshold": ("double", False),
            "passed": ("boolean", False), "n_samples": ("bigint", False),
            "source_path": ("string", True), "source_sha256": ("string", True),
            "landed_by": ("string", True), "landed_at": ("string", True),
        },
        "enums": {"gate_id": ["P1", "P2", "P3", "P4", None]},
    },
    "run_telemetry": {
        "key": "telemetry_id", "group": None,
        "fields": {
            "telemetry_id": ("string", True), "contract_version": ("string", True),
            "run_id": ("string", True), "host": ("string", True), "base_model": ("string", True),
            "config_sha256": ("string", True), "step": ("bigint", True), "epoch": ("double", False),
            "loss": ("double", False), "eval_loss": ("double", False), "learning_rate": ("double", False),
            "source_path": ("string", True), "source_sha256": ("string", True),
            "landed_by": ("string", True), "landed_at": ("string", True),
        },
        "enums": {},
    },
}


def validate(entity: str, rec: dict) -> list[str]:
    c = CONTRACTS[entity]
    errs = [f"unknown_field:{k}" for k in rec if k not in c["fields"]]
    for f, (_, req) in c["fields"].items():
        if req and rec.get(f) in (None, ""):
            errs.append(f"missing:{f}")
    for f, allowed in c["enums"].items():
        if f in rec and rec[f] not in allowed:
            errs.append(f"enum:{f}")
    if rec.get("contract_version") not in (None, CONTRACT_VERSION):
        errs.append("contract_version")
    if entity == "audit_verdict" and rec.get("human_reviewed") is False and rec.get("human_winner") is not None:
        errs.append("human_winner_without_review")
    return errs
