# run008 FINAL (2026-10-10/11): NO checkpoint release-eligible. No HF push.
Data: 707 teacher-distilled (Nemotron-3-Super) domain rows + 314 replay; data gate K=0.997 (uninformative). Train: r7 recipe, val loss 1.553->1.418.
P1 (with-ref gpt-4o-mini vs BASE, n=300 held-out): ck16 48.0% [42.4,53.6]; ck32 51.2% [45.5,56.8]; ck48 48.0% [42.4,53.6]. Need >=55% and lower>50 -> all FAIL (r6 was ~33%).
P2: all PASS. P4: ck16 PASS (safe 9<=9); ck32/48 FAIL (safe 11). P3: all FAIL as scored, BUT chat_g cell is MISSING in out-r8 (suite_run_r8 did not produce it) so P3 cannot pass by construction; completion_s had 1 loop (ck16) / 1 tag leak (ck32).
Even ignoring P3, P1 fails on every checkpoint. Verdict stands: NONE PASS.
Files: out-r8/, judge_r8.json, r8_summary.txt, PREREG-008*.md.
