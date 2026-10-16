# run012 P2/P3/P4 recheck of RAG pipeline + packaging (2026-10-11)
Always-on RAG vs BASE: P2 FAIL (pooled -5.5, max single -10.0: gsm8k 28.3->18.3), P4 FAIL (harmful 25->23), P3 FAIL small (loop 15 vs 11 greedy; 2 vs 0 sampled).
Gate by top-1 cosine tau 0.635: AUC 0.996 (provisional, tuned on eval sets). Package: ~/athanor-rag-serve (spark2), copy Mac scratch r12/athanor-rag-serve; smoke test SMOKE_OK incl. off-domain gate (sim 0.609 -> plain BASE, 391 correct).
Not validated: end-to-end gated P2/P4 / held-out gate threshold.
