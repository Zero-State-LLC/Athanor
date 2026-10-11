# Athanor landing-volume ingest contract (athanor.v1)

Landing: `/Volumes/workspace/athanor_dev/landing/<entity>/*.jsonl` (one JSON object per line).
Entities: `sft_row`, `audit_verdict`, `eval_gate`, `run_telemetry`. Schemas: `contracts/<entity>.v1.schema.json`
(generated from `src/athanor_data/contracts.py`; additionalProperties=false).

Rules
- Never invent rows. Every row carries `source_path` + `source_sha256` of the artifact it was read from.
- `sft_row.source_kind` ∈ observed | synthetic | model_generated; `rights` is required free text (e.g. "internal-only", "PD", "unknown").
- `audit_verdict.judge_winner` is a MODEL label (judge_model + judge_version required). Human agreement is
  separate: `human_reviewed`, `human_winner`, `human_reviewer`. `human_winner` without
  `human_reviewed=true` is quarantined. Never copy the judge verdict into human fields.
- `is_judge_self_agreement` (was `is_agreement_control`) marks the control where the same judge model is run under two
  protocols (with / without reference) to test self-consistency. It is not human agreement; human_* stay false/null for it.
- `sft_row.rights = 'unknown'` (rows seeded from outside text) passes client validation but is quarantined by the
  pipeline with reason `rights_unknown`; it never reaches `curated_sft_row`.
- `record_id` / file-backed ids use `<sha256 of the source file>:<line>` (JSON-array sources: 1-based element position), so ids
  survive a re-copy of the file.
- `eval_gate` rows (P1–P4 etc.) are evaluation outcomes, not training labels; there is no join path into SFT.
- Splits: curated `sft_row` and `audit_verdict` get `split` from sha256(`athanor.split.v1:`+lower(family)) mod 100
  (80/10/10). A family never straddles splits; an audit verdict lands in the same split as its family.
- Idempotent: raw MERGE on sha256(line); curated MERGE on business key (latest `landed_at` wins).
- Invalid rows go to `quarantine_<entity>` with reasons.

## land_record
```
export PATH=~/.local/bin:$PATH DATABRICKS_AUTH_STORAGE=plaintext
python3 scripts/land_record.py <entity> rows.jsonl --landed-by <who> --dry-run   # validate only
python3 scripts/land_record.py <entity> rows.jsonl --landed-by <who>             # upload
databricks bundle run -t dev zs_athanor_data_pipeline                             # raw->validated->curated
```
Any invalid row aborts the whole file (nothing uploaded). It fills contract_version, landed_by, landed_at and
source_sha256 (sha of the jsonl you pass) if absent; it does not fill content.
