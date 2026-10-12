# PREREG-008 ADDENDUM 1 (2026-10-10, before any candidate was judged)
Parent: PREREG-008.committed.md sha256 f86028acb9038af521c9a5ea13b8518846998bc449cfa45eec4382f366289213.
Change: §1 generator Spark1 Qwen3.8-27B -> Nemotron-3-Super-120B-A12B-NVFP4 served by vLLM on spark2 (port 8899, per Aaron: "on spark2").
Reason: Spark1 endpoint throughput ~2 candidates/min (33 of 2860 in ~20 min; latency queue-bound), projected ~20 h. Observed before any judging; no results influenced the choice.
Unchanged: N=4, temp 0.7, top_p 0.9, system prompt, token cap, 715 prompts, judge panel, clear-win rule, keep rule, K<0.30 gate, all §4/§5. Thinking mode off for the generator (answers must be comparable to BASE zero-shot).
Discarded: 40 Spark1 candidates (cands_spark1_abandoned.jsonl) are NOT used.
Note: Nemotron-3-Super is in the same model family as the BASE/target (Nemotron) lineage -> possible self-preference is neutralized by the non-Nemotron judge panel but is reported as a limitation.
Operational: the vLLM server holds ~85% GPU memory and MUST be stopped before any LoRA training.
