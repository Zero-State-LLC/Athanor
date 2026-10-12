# PREREG-008 — Athanor run008, arm (a): audit-as-you-go data rebuild
Committed before ANY candidate is generated. Author: z0D for Aaron (go: "a, then continue", 2026-10-10). Supersedes nothing in PREREG-006/007 gates.

## Why
r7 audit: BASE zero-shot beat r6 SFT targets on 486/715 domain rows (drop 0.680 > 0.60). Training data was worse than the untouched model. r8 therefore fixes the DATA first; no training until data passes the gate below.

## §1 Candidate generation
- Prompts: the 715 non-replay domain `user` prompts of r6 sft_train (same set audited in r7; r7 BASE answers reused as comparator, unchanged).
- Generator: Spark1 Qwen3.8-27B (qwen.zer0state.com, model "/model"). N=4 candidates/prompt, temp 0.7, top_p 0.9, system: "Answer accurately and concisely (under 200 words). If unsure, say so rather than inventing details." Candidates capped ~300 tokens like BASE. No reference text given.
- The r6 SFT target is NOT a candidate.

## §2 Judge panel (3 judges, all non-Qwen to avoid generator self-preference)
openai/gpt-4o-mini (validated in r7), anthropic/claude-haiku-4.5, google/gemini-2.5-flash-lite. Protocol = r7 pairwise (temp 0, seeded A/B flip, WINNER parse, no reference), candidate vs BASE answer.
- Panel validation (blocking): the r7 control measured no-reference audit verdicts against the WITH-reference P1 judge verdicts (control_verdicts.json) on n=100 frozen questions — NOT against human labels (correction: r7 reports described this as 'judge-vs-human'; it was no-ref vs with-ref, both gpt-4o-mini). Rerun the same no-ref protocol with the 3-judge panel majority on the same 100 items; sign agreement vs the with-ref verdicts must be >= 70% (same TIE rule), else HALT. Known limit: reference verdicts come from gpt-4o-mini; no human labels exist.
- A candidate CLEARLY WINS iff >= 2 of 3 judges pick it over BASE (TIE and BASE votes do not count).

## §3 Row acceptance
- A prompt is KEPT iff >= 1 of its 4 candidates clearly wins. Selected answer = candidate with most judge wins, ties -> lowest candidate index.
- Judge ERROR/PARSE_ERROR counts as not-a-win; if >5% of calls error, rerun errors once, then report.
- keep_rate K = kept / 715 (also reported per family).

## §4 Gate (fixed now)
- K < 0.30  -> HALT arm (a); route to option (b) retrieval/anchoring; NO training, NO ckpt, NO HF push. Aaron decides.
- K >= 0.30 -> build mix = kept rows (selected candidates) + replay incl. deliberate harmful-refusal examples (P4 stays hard gate: harmful refusals >= 24/25, safe_refused <= 9) -> LoRA train with the r7 recipe/hparams unchanged (train_r7.py) -> full P1-P4 eval per PREREG-006 gates. Release gate stays closed until a checkpoint passes all four. No HF push otherwise.
- No recipe changes, no threshold changes, no judge/prompt substitution after seeing any result.

## §5 Reporting
Post to Buzz #general: kickoff, this plan, telemetry (panel agreement, K, per-family, error rate, cost) when done, and the gate verdict.
