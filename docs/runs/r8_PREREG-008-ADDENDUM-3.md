# PREREG-008 ADDENDUM 3 (2026-10-10; filed before training). Aaron's go: "do #1".
Pass-2 judging: K = 713/715 = 0.997 (gate 0.30 passed by the letter; judged uninformative — 120B teacher vs 8B student). Proceeding to ONE LoRA run, release gate unchanged.
Mix (build_mix_r8.py, seed 20261016): 707 domain rows (best finished teacher candidate with >=2/3 judge wins; 6 prompts dropped because their only winners were truncated at the token cap, 2 had no clear winner) + 314 replay (30.8%, incl. 24 harmful-refusal demos) = 1021; train 961 / val 60. sha_train 4d4b86b857025043.
Recipe: train_r7.py hparams UNCHANGED (r16 a32 drop0.1, lr 3e-5 cosine, warm 5, accum 16, 48 steps, seed 42, ckpt/8). Only paths changed. Arm B (unfiltered attribution arm) is not run: no audit filter exists to attribute.
Eval: P1-P4 per PREREG-006 gates, same runner/items as r6/r7 (suite_run_r7.py, paths only changed). No HF push unless a checkpoint passes ALL gates. Failure is a valid, reportable outcome.
