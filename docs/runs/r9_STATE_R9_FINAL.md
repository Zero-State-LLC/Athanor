# run009 (option b, RAG anchoring, no SFT) — P1 FAIL (2026-10-10)
PREREG-009 sha256 43c4649e724247107a86402be95bb082002a2e7e82f1baa35a08eeb5f4923f8c. Corpus 2348 dedup PD passages; BM25+bge-small RRF, top-3.
Retrieval: gold source in top-3 for 121/300 (40.3%). goldexcl arm: 0/300 by construction.
P1 (with-ref gpt-4o-mini vs BASE, n=300, err 0): FULL 50.7% [45.0,56.3] FAIL (need >=55 & lower>50); GOLDEXCL 43.8% [38.3,49.5] (reported, not gated).
Diagnostic (post-hoc, not gated): FULL win when gold retrieved 60.3% (n=121); when NOT retrieved 44.1% (n=179).
P2/P4: unchanged weights. P3-lite on RAG outputs: loop 1/300, tag 0, boilerplate 0 (both arms). Copy rate: max 12%, 44/300 >0, none >60%. Model says 'passages don't answer' in 30 (full) / 40 (goldexcl) answers.
Verdict: gate FAILED; no ship. Bottleneck = retrieval recall, not copying.
