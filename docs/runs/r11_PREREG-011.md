# PREREG-011 — P1g: grounded rebuild of the P1 in-domain benchmark, then re-baseline (no new training)
Author z0D for Aaron ("yes do it", 2026-10-11). Committed before any new question is generated.
## Why
run010 diagnosis: only 194/300 (65%) of old P1 questions are answerable from their gold passage (PARTIAL 90, NO 16). Old P1 verdicts (r6 ~33%, r8 48-51%, r9 50.7%) mix model quality with a broken test. This run fixes the TEST, then re-asks the questions.
## Build P1g (fixed now)
- Source: test-split passages only (never used for training), deduped by text, seed 20261011 order; family-stratified round-robin. Generate for the first 450.
- Question + reference: openai/gpt-4o-mini, passage in view: one general question a student would ask (no mention of 'the passage', <=25 words) and a grounded reference answer (<=90 words) using ONLY the passage.
- Verification (keep only if BOTH): (a) anthropic/claude-haiku-4.5 given question+passage answers YES (not PARTIAL/NO) to 'does the passage contain the information to answer this?'; (b) the question is not answerable from the question text alone (cheap guard: reference shares <60% of its content words with the question).
- P1g = first 300 verified (in generation order). If <300 verify, halt and report; do not relax.
## Arms (same 300 questions; all: Nemotron-Nano-8B, system 'detailed thinking off', temp 0.7, top_p 0.9, rep_pen 1.1, max_new 600 for ALL arms so truncation is not a confound; stopped-fraction reported)
- B0 BASE zero-shot (comparator).
- B1 BASE+RAG: C1 retrieval (bge-large + BM25 RRF, top-3, 2348-passage corpus incl. gold), run009 prompt.
- B2 BASE+RAG gold-excluded (reported only).
- B3 BASE+ORACLE: gold passage injected directly (instrument-validity arm).
- F  r8ck32 (SFT'd, zero-shot) — highest-P1 r8 checkpoint on the old test, chosen before looking at P1g results.
## Judge
Pairwise vs B0, A/B flip seeds fixed, with-reference (the grounded reference). Primary: openai/gpt-4o-mini. Secondary (reported, guards self-preference): anthropic/claude-haiku-4.5 same protocol.
## Gates (fixed)
- R0 instrument validity: B3 (oracle) must win >=60% vs B0 on primary judge, else P1g cannot detect context help -> report invalid, no arm verdicts.
- Per arm (B1, F): PASS = win >=55% with Wilson lower >50 on primary judge; secondary must not reverse direction (win<45%) else flagged. B2 reported. Also report retrieval hit@3 for B1 and copy-rate.
- Verdict semantics: B1 pass => ship retrieval pipeline. F pass => r8ck32 is release candidate pending P2-P4 (reuse r8 scores, P3 chat_g cell to be fixed first). Both fail on a VALID instrument => stop SFT/RAG-on-8B line; report.
## Cost/time
~450 questions + 450 verifications (~$0.3), 5 arms x 300 gens (~1.5h spark2), judge ~3000 calls (~$1).
