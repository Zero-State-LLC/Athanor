#!/usr/bin/env python3
"""Validate JSONL against an Athanor contract and land it in the UC landing volume.

usage: land_record.py ENTITY FILE.jsonl --landed-by NAME [--dry-run] [--profile zer0state]
         [--catalog workspace] [--schema athanor_dev]
Fills contract_version, landed_by, landed_at, source_sha256 (of FILE) if absent; never invents content.
Any invalid row aborts the whole landing (nothing is uploaded)."""
import argparse, datetime, hashlib, json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from athanor_data.contracts import CONTRACTS, CONTRACT_VERSION, validate

ap = argparse.ArgumentParser()
ap.add_argument("entity", choices=list(CONTRACTS)); ap.add_argument("file")
ap.add_argument("--landed-by", required=True); ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--profile", default="zer0state"); ap.add_argument("--catalog", default="workspace")
ap.add_argument("--schema", default="athanor_dev")
a = ap.parse_args()
raw = open(a.file, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
out, bad = [], 0
for i, line in enumerate(raw.decode().splitlines(), 1):
    if not line.strip():
        continue
    r = json.loads(line)
    r.setdefault("contract_version", CONTRACT_VERSION); r.setdefault("landed_by", a.landed_by)
    r.setdefault("landed_at", now); r.setdefault("source_sha256", sha)
    errs = validate(a.entity, r)
    if errs:
        bad += 1; print(f"line {i}: {errs}", file=sys.stderr)
    out.append(json.dumps(r, sort_keys=True))
print(f"{a.entity}: {len(out)} rows, {bad} invalid, source_sha256={sha}")
if bad or a.dry_run:
    sys.exit(1 if bad else 0)
name = f"{a.entity}-{now[:19].replace(':', '')}-{sha[:12]}.jsonl"
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
    f.write("\n".join(out) + "\n")
dst = f"dbfs:/Volumes/{a.catalog}/{a.schema}/landing/{a.entity}/{name}"
subprocess.run(["databricks", "fs", "cp", f.name, dst, "-p", a.profile], check=True)
print(f"landed {dst}")
