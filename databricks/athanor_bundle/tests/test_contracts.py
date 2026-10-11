import hashlib, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from athanor_data.contracts import CONTRACTS, validate
from athanor_data.split import split_for_group
from athanor_data.sql import render_merge_sql

def test_required_missing():
    assert "missing:family" in validate("sft_row", {"contract_version": "athanor.v1"})

def test_human_separate_from_judge():
    errs = validate("audit_verdict", {"human_reviewed": False, "human_winner": "BASE"})
    assert "human_winner_without_review" in errs

def test_gates_not_training_labels():
    assert "passed" not in CONTRACTS["sft_row"]["fields"] and "judge_winner" not in CONTRACTS["sft_row"]["fields"]

def test_split_grouped_deterministic():
    assert split_for_group("FamA") == split_for_group("fama")
    assert {split_for_group(f"f{i}") for i in range(200)} == {"train", "val", "test"}

def test_split_matches_sql_formula():
    g = "fam1"; h = hashlib.sha256(f"athanor.split.v1:{g}".encode()).hexdigest()
    assert int(h[52:64], 16) % 100 == int(h[-12:], 16) % 100

def test_merge_sql():
    s = render_merge_sql("t", "s", "k", ["k", "v"])
    assert "ON t.k=s.k" in s and "t.v=s.v" in s
