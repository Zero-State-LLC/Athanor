# Inventory (2026-10-10 PT, from the box)

Spark access: `~/.ssh/config` defines `spark` (ssh.zer0state.com) and `spark2` (ssh-spark2.zer0state.com) via cloudflared,
but the box has no `ssh` binary and cannot install one (no sudo). **Sparks unreachable; nothing read; no GPU use.**
spark-af42 has no ssh entry. Not found on the box: `~/Athanor/data/run007`, `~/athanor-eval/out-r6`, `out-r7`, `scores.json`, `judge_r6.json`, prereg P1–P4 results.

Org repo: `Zero-State-LLC/Athanor` (public, default `main` @ 4e6b889). Box copy `/workspace/Athanor` (remote scrimshawlife-ctrl/Athanor, branch docs/readme-comprehensive).

| path | sha256[:16] | rows | kind | rights | landed? |
|---|---|---|---|---|---|
| repo `eval_results.json` (Nemotron-Nano-8B base vs merged ppl, 100/606 samples) | 209aeebbd3efa1d8 | 1 object | observed | repo license | no – no run_id/checkpoint/gate; not the r6/r7 eval |
| repo `artifacts/efficiency/ATHANOR-STRUCTURAL-EFFICIENCY-001/*_training_data*.jsonl` (6 files) | 5c6e…/8cad…/5db0…/a0bc… | 504 each | synthetic (templated by build_efficiency_data.py) | repo license | no – separate experiment, no family/provenance; not the domain SFT |
| repo `artifacts/efficiency/.../efficiency_eval.jsonl` | 23534adec605ede5 | 267 | synthetic | repo | no |
| repo `artifacts/composition/.../composition_eval.jsonl` | b0de0376360bf728 | 84 | synthetic | repo | no |
| repo `artifacts/mechanisms/.../causality_eval.jsonl` | 5638af0445b88818 | 157 | synthetic | repo | no |
| repo `fixtures/correspondence/pairs.p3a.jsonl` | c3529ff0fd7d2307 | 7257 | corpus fixtures (encoder), not SFT | PD-first | no |
| box `~/.athanor/corpus/atoms.jsonl` | e42f2dea78a0bef5 | 2997 | observed corpus atoms (encoder) | PD-first per LICENSE_POLICY | no – not an SFT/audit/eval/telemetry entity |
