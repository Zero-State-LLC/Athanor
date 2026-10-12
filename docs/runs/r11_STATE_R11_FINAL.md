# run011 P1g (grounded benchmark) — RESULT 2026-10-11. PREREG-011 sha fcb4b1c5…; ADDENDUM-1 sha 33e57ee0….
P1g: 300 q from held-out test-split passages, haiku-verified answerable (pool 900 -> 488 kept -> first 300). B1 retrieval source-in-top3 247/300 (82.3%) vs 40% on old P1.
R0 (oracle B3 >=60% primary): 86.7% -> instrument VALID.
Win vs BASE zero-shot (with-ref, n=300) primary gpt-4o-mini / secondary claude-haiku-4.5:
 B1 BASE+RAG        84.3% [79.8,88.0] / 95.0% [91.9,96.9]  -> PASS
 B2 RAG gold-excl   64.2% [58.6,69.4] / 83.5% [78.9,87.3]  (reported)
 B3 ORACLE passage  86.7% [82.4,90.1] / 97.0% [94.4,98.4]  (validity)
 F  r8ck32 SFT      57.7% [52.0,63.1] / 46.0% [40.4,51.7], 17 secondary errors -> primary PASS, secondary ambiguous (not <45 rule); ck32 still FAILED P4 (safe refusals 11 > 9) and P3 incomplete in r8 -> NOT release-eligible.
Caveats: references are gpt-4o-mini written FROM the passage, so P1g rewards passage-consistent answers (= KB knowledge, the product goal), and favors arms that see the passage. Primary-judge/ref-writer share a vendor (secondary is a different vendor and agrees on direction). One build iteration (ADDENDUM-1) before any arm ran.
Verdict: retrieval pipeline (bge-large + BM25 RRF, top-3) is the ship candidate. No HF push (nothing trained to push).
