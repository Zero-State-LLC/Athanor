import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files = []
for rel in ["databricks.yml", "README.md", "contracts", "docs", "src", "scripts", "tests"]:
    it = ROOT / rel
    for p in ([it] if it.is_file() else sorted(x for x in it.rglob("*") if x.is_file() and "__pycache__" not in x.parts)):
        files.append({"path": str(p.relative_to(ROOT)), "sha256": sha(p),
                      "row_count": sum(1 for l in p.open() if l.strip()) if p.suffix == ".jsonl" else None})
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "release/MANIFEST_v0.1.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"schema_version": "athanor.manifest.v1",
    "generated_at": datetime.now(timezone.utc).isoformat(), "files": files}, indent=2, sort_keys=True) + "\n")
