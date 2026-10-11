# zs_athanor_data (Databricks Asset Bundle)

Mirrors `vernacular-ingest/databricks/slang_bundle` and `pawl/data/databricks`: dev target (profile zer0state,
catalog `workspace`, schema `athanor_dev`), serverless job with **no schedule**, raw → validated/quarantine → curated
for `sft_row`, `audit_verdict`, `eval_gate`, `run_telemetry`; versioned contracts (athanor.v1), idempotent MERGE,
grouped leakage-safe splits by family, manifest in `release/`.

See `docs/INGEST_CONTRACT.md`, `docs/HANDOFF_SPARK.md`, `INVENTORY-phase1.md`.
`python3 -m pytest tests && databricks bundle validate -t dev && databricks bundle deploy -t dev`
