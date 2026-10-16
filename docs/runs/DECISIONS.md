# Athanor decisions — 2026-10-12 (Aaron)
1. HF: Option B, PRIVATE first. Publish pipeline repo (code, config, build script, model card with numbers+caveats; NO corpus text, NO index, NO weights). Staged at ~/athanor-run-archive/hf-athanor-rag-pipeline (Mac) and spark2 ~/hf-staging/athanor-rag-pipeline; SHA256SUMS verified. Needs: Danny/Aaron pick account/org and add HF_TOKEN themselves; Hub-block (Athanor docs/status.md) lifted. Nothing uploaded.
2. Public only after PUBLIC_CHECKLIST.md: larger-held-out routing recall; human-written occult prompts; judge/human spot-check instead of phrase list; one real safety review; full suite re-run with pre-check; licence check.
3. Fine-tuning line FROZEN: no checkpoint passed all four gates; old P1 only 65% answerable from own passage -> fix benchmark (P1g) before more GPU on training.
4. Do NOT push run004-r1 adapter (no gate results, stale checksums, placeholder repo id).
5. Run records moved off scratch: Mac ~/athanor-run-archive/athanor-runs-r6-r15_20261011.tgz (sha256 669dc5402f23df57…) + summaries/ (20 files); spark2 ~/Athanor-evidence/docs/runs/ (20 files, UNCOMMITTED in git). Databricks pipeline: not done (no access/target given).
