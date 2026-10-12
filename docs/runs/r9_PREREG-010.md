# PREREG-010 — run010: retrieval-quality ladder for RAG anchoring (no training, weights unchanged)
Author z0D for Aaron ("try 1", 2026-10-11). Committed before any dev question is generated or any new retrieval is run. Supersedes nothing in PREREG-009; reuses its P1 gate verbatim.
## Why
run009: source passage in top-3 for 121/300 (40%); P1 win 60.3% when retrieved vs 44.1% when not (post-hoc). Retrieval recall is the bottleneck.
## Anti-overfit design (fixed now)
- DEV set (tuning): 200 passages sampled (seed 20261011) from train+val passages (never from the 300 p1 passages), one general question each written by openai/gpt-4o-mini in the P1 style ("general question on the topic, do not reference the passage, <=25 words"). Config selection uses DEV only.
- TEST = the 300 frozen P1 questions. Retrieval on TEST is run ONCE, with the single frozen config. No config is chosen using TEST.
## Ladder (all configs defined now; corpus = same 2348 deduped PD passages; top-3 injected)
- C0 baseline: bge-small + BM25, RRF (run009).
- C1: bge-large-en-v1.5 dense + BM25, RRF.
- C2: C1 top-30 -> cross-encoder BAAI/bge-reranker-large -> top-3.
- C3: C2 with HyDE query expansion (gpt-4o-mini writes a <=60-word hypothetical answer, appended to the query for dense, BM25 and reranker). Serving dependency on an external LLM is DISCLOSED; if C3 is selected only because of HyDE it is reported as such.
- Selection: highest DEV hit@3 (gold passage text in top-3); ties -> simpler (lower index). Seeds/params fixed above; no further configs.
## Gates (fixed)
- R1 (retrieval, pre-generation): selected config DEV hit@3 >= 0.70. Else HALT: report, no generation.
- R2: frozen config TEST hit@3 reported; if < 0.60 HALT (no generation, report). Else proceed.
- P1: full-corpus arm, BASE+RAG (unmodified Nemotron-Nano-8B, same decoding/prompt as run009) vs BASE zero-shot, same with-reference gpt-4o-mini judge, n=300: win >= 55% with Wilson lower > 50. Gold-excluded arm reported, not gated. P3-lite + copy-rate (<=60%) rechecked. Weights unchanged => P2/P4 by construction.
- Pass => the retrieval pipeline is the serving path (nothing to HF). Fail => reported; no further tuning on TEST.
## Cost/time
Dev questions ~200 calls (~$0.05); ladder ~1h spark2 GPU; generation+judge ~1.5h if it proceeds.
