# PREREG-009 — run009, option (b): retrieval/anchoring, NO SFT, no weights changed
Status: APPROVED by Aaron ("go", 2026-10-11) as drafted. Committed before any retrieval or generation.

## Question
Does giving the unmodified Nemotron-Nano-8B BASE retrieved source passages in context (RAG anchoring) beat BASE zero-shot on the P1 in-domain task? SFT (r6, r8) topped out at parity (48-51%, gate 55%).

## Design
- Corpus: all PD passages already in the Athanor pipeline (run006 train 1012 + val 163 + test 1300 + the 300 p1 passages), chunked as-is, deduped by text. Index: BM25 (rank_bm25) + dense (bge-small or similar on spark2), fused RRF; top-k=3 passages, ~<=1200 tokens injected.
- Leak control (fixed now): the question's own source passage is NOT removed (that is the realistic KB case), BUT we also report a "gold-excluded" arm where the P1 passage is removed from the index, to separate "retrieval finds it" from "model uses nearby context". Primary verdict arm = full corpus; gold-excluded arm is reported, not gated.
- Arms (all on the same 300 held-out P1 questions, same n): BASE zero-shot (reuse r6/r8 BASE answers, 300 tok), BASE+RAG (same decoding: temp 0.7, top_p 0.9, rep_pen 1.1, 'detailed thinking off', max_new 300, same seed family). Prompt: "Use the passages below if relevant; if they do not answer, say so. Passages: ..." 
- Judge: IDENTICAL to r6/r8 P1 (with-reference gpt-4o-mini, A/B flip seeds, n=300). Plus the 3-judge no-ref panel as a secondary readout.
## Gates (fixed)
- P1: BASE+RAG win rate vs BASE >= 55% with Wilson lower > 50.
- P2/P3/P4: weights unchanged => P2/P4 hold by construction; P3 rechecked on RAG outputs (loop/tag-leak/boilerplate no worse than BASE). Add: answer must not copy >60% of the passage text verbatim (copy-rate reported).
- Pass => RAG pipeline is the Athanor serving path (ship the pipeline, not a checkpoint; nothing to push to HF). Fail => report; options become retrieval quality work or a different base.
## Cost/time
~1 GPU-hour on spark2 (index + 300x answers), ~$1 judging. Fix chat_g cell omission from r8 suite before any P3 claim.
