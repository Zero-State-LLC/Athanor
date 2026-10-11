import hashlib

SPLIT_METHOD_VERSION = "athanor.split.v1"


def split_for_group(group_key: str, version: str = SPLIT_METHOD_VERSION) -> str:
    """Grouped split: every row of a family lands in one split (no family leakage)."""
    b = int(hashlib.sha256(f"{version}:{group_key.lower()}".encode()).hexdigest()[-12:], 16) % 100
    return "train" if b < 80 else ("val" if b < 90 else "test")


def split_sql(col: str, version: str = SPLIT_METHOD_VERSION) -> str:
    """Spark SQL equivalent of split_for_group."""
    h = f"pmod(conv(substr(sha2(concat('{version}:', lower({col})), 256), 53, 12), 16, 10), 100)"
    return f"CASE WHEN {h} < 80 THEN 'train' WHEN {h} < 90 THEN 'val' ELSE 'test' END"
