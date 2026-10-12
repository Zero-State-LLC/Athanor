# PREREG-011 ADDENDUM 1 (2026-10-11; filed after the build step, BEFORE any arm generation or judging)
Parent sha256 fcb4b1c53fe1679b8802e0ff737ada7de07ed86512963a87a5ed4c5f0af85fc5.
Observed: first 450 candidates -> 247 YES / 203 PARTIAL; 245 kept after the overlap guard (<300, so the prereg HALT rule fired for the 450-candidate pool).
Changes (no model results exist yet; none can influence them):
1. Candidate pool extended from 450 to 900 passages (next 450 in the same seeded family-stratified order). Verification criteria (haiku YES, overlap<0.60) are UNCHANGED, not relaxed.
2. Added question-style filter (intent of the original 'do NOT mention the passage/text'): drop questions matching /the author(s)|the text|this text|the passage|this passage|the book|this book|the writer|the document/ — such questions are unanswerable without the source and are not domain knowledge questions. Applied to all 900.
3. P1g = first 300 surviving, in generation order. If still <300, HALT and report.
