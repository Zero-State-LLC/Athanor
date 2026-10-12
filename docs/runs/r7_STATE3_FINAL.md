# Athanor r7 — FINAL STATE (2026-10-10, supersedes STATE2.md)

## Verdict: PREREG §1 GATE FIRED — no arm-A training. Run007 ends here.
- Audit judge (v2, collision-safe keying) complete: **drop_rate = 0.6797** (TARGET 229 / BASE 486, n=715).
- Gate: drop_rate > 0.60 ⇒ "set too thin, NO arm-A training" (prereg §1). `build_mix_r7_v2.py` line 25 raises SystemExit on exactly this.
- Control arm PASSED earlier: n=100, agreement 78.0% ≥ 70 bar, judge_wr 24.5%. The audit instrument is trustworthy — BASE genuinely beats the r6 SFT targets on 68% of domain rows.
- Consequence: r6's P1 failure is explained — the SFT data itself was mostly worse than BASE zero-shot. Training on it (any recipe) cannot beat BASE. No checkpoints, no HF push (unchanged from r6 conclusion).

## Verified on spark2 (2026-10-10, this session)
- `r7_gpu_chain.log` ends `R7_GPU_CHAIN_DONE` (audit_base 715 rows + control_base 100). GPU idle: 0 compute procs.
- `~/Athanor/data/run007/`: 45 audit_base_bNNN.json batches, audit_base.json (715), audit_meta.json, control_result.json (pass_bar_70 true).
- NO `lora-out-nemotron-run007-*` dir, no train_r7.py / suite_run_r7.py / build_mix process running. Nothing left to babysit.
- Mac authoritative artifacts: `~/.hermes/cache/scratch/r7/audit_summary.json` (drop_rate 0.6797, per-family), `audit_verdicts_v2.json`, `audit_judge_v2.log` (ends AUDIT_JUDGE_DONE), `control_result.json` (identical to spark2).

## Per-family survivor rates (TARGET wins / total)
23 of 28 families BASE-wins-majority. Worst: egypt_magical 11.1%, chaos_spare_hist 14.3%, alchemy_lab / hebrew_bible_magical 15.2%. Best: goetia_catalog 66.7%, angel 62.5%, runes_eddic 60.6%. Overall 229/715 = 32.0% survive.

## What "continue" would mean next (needs Aaron's call — prereg stop, do not override silently)
1. Post gate verdict to Buzz #general (`~/bin/buzz-post-general.sh`) — drafted-ready, not posted.
2. r8 direction options: (a) rebuild SFT targets from BASE self-distillate + stronger teacher with per-row judge acceptance (audit-as-you-go, not audit-after); (b) drop the SFT-target approach for P1 entirely and pursue retrieval/anchoring (prereg's eval_retrieve.py exists); (c) arm-B-only attribution run — pointless without arm A.
3. Close run007 in the ledger with gate-fail status.

## Compression config (verified this session)
- `compression.threshold: 0.5` in ~/.hermes/config.yaml, model bosgame-qwen llama-server `-c 131072` → 0.5×131072 = 65,536 token trigger, i.e. already effectively ~66-70k. OMH compaction trigger fired this turn, confirming it works. The gap was ME not calling /compact proactively, not the config. No config change needed.
- Standing 70k-compress directive IS saved in memory (succeeded first call). The r7-status memory entry update failed (consolidation loop guard) — retry next turn.
