# Handoff: landing spark artifacts (z0D / Mac)

The box has no ssh client, so spark2 / spark-af42 artifacts were NOT read. Tables are deployed empty.
Do not run anything on the GPUs; these are read-only file conversions.

1. On a machine that can reach the sparks, `git fetch && git checkout data/databricks-athanor-phase1`,
   `cd databricks/athanor_bundle`, profile `zer0state` configured (catalog `workspace`).
2. Record for each artifact: `sha256sum`, `wc -l`, and whether it is observed / synthetic / model_generated.
3. Convert (write a small converter per artifact; map fields only, never fill gaps with guesses — use null for optional fields):

| artifact | entity | key | notes |
|---|---|---|---|
| `~/Athanor/data/run007/*.jsonl` | sft_row | record_id = `run007:<file>:<line>` | family required (28 families); run_id=`run007`; rights required |
| `~/athanor-eval/out-r7/` audit (715 rows, SFT target vs BASE) | audit_verdict | verdict_id = `r7:<record_id>` | audit_round=`r7`; judge_winner TARGET/BASE/TIE (expect 486 BASE); judge_model+version from the judge config; human_* only from a real human review file |
| `~/athanor-eval/out-r6/judge_r6.json` | audit_verdict | `r6:<record_id>` | audit_round=`r6` |
| `scores.json`, prereg P1–P4 results per checkpoint | eval_gate | `<run>:<ckpt>:<suite>:<metric>` | gate_id P1..P4; threshold from the prereg doc; passed as computed there |
| trainer_state.json / train logs per run | run_telemetry | `<run>:<step>` | config_sha256 = sha256 of the exact training YAML; host spark2 / spark-af42 |

4. `python3 scripts/land_record.py <entity> file.jsonl --landed-by z0D --dry-run`, fix until 0 invalid, then rerun without `--dry-run`.
5. `databricks bundle run -t dev zs_athanor_data_pipeline`, then check counts:
   r7 audit should show 715 curated_audit_verdict rows with audit_round='r7' and 486 judge_winner='BASE';
   quarantine tables should be 0. Stop the SQL warehouse afterwards.
6. r8 (audit-as-you-go): land each candidate's verdict as it is judged; the gate "every row beats BASE" is
   `curated_audit_verdict WHERE audit_round='r8' AND judge_winner <> 'TARGET'` = 0.
