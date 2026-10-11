"""raw -> validated/quarantine -> curated for every Athanor contract. Idempotent (MERGE on key)."""
import os, sys
_a = sys.argv[1:]
if "--src" in _a:
    sys.path.insert(0, _a[_a.index("--src") + 1])
from pyspark.sql import SparkSession
from athanor_data.contracts import CONTRACTS, CONTRACT_VERSION
from athanor_data.split import split_sql, SPLIT_METHOD_VERSION
from athanor_data.sql import render_merge_sql

a = sys.argv[1:]
arg = lambda n: a[a.index(n) + 1] if n in a else None
catalog, schema, stage = arg("--catalog"), arg("--schema"), arg("--stage")
assert catalog and schema and stage in ("raw", "validate", "curate")
spark = SparkSession.builder.getOrCreate()
fq = lambda t: f"{catalog}.{schema}.{t}"
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.landing")

for ent, c in CONTRACTS.items():
    cols = list(c["fields"])
    ddl = ", ".join(f"{f} {t.upper()}" for f, (t, _) in c["fields"].items())
    key = c["key"]
    if stage == "raw":
        spark.sql(f"CREATE TABLE IF NOT EXISTS {fq('raw_'+ent)} (raw_id STRING, payload_json STRING, _source_file STRING, _ingested_at TIMESTAMP)")
        path = f"/Volumes/{catalog}/{schema}/landing/{ent}/"
        try:
            df = spark.read.text(path).selectExpr(
                "sha2(value, 256) AS raw_id", "value AS payload_json",
                "_metadata.file_path AS _source_file", "current_timestamp() AS _ingested_at")
            df.limit(1).collect()  # force path resolution
        except Exception as e:  # empty / missing landing dir
            print(f"[{ent}] no landing files: {type(e).__name__}")
            continue
        df.createOrReplaceTempView("src")
        spark.sql(f"MERGE INTO {fq('raw_'+ent)} t USING src s ON t.raw_id=s.raw_id WHEN NOT MATCHED THEN INSERT *")
    elif stage == "validate":
        spark.sql(f"CREATE TABLE IF NOT EXISTS {fq('validated_'+ent)} (raw_id STRING, {ddl})")
        spark.sql(f"CREATE TABLE IF NOT EXISTS {fq('quarantine_'+ent)} (raw_id STRING, payload_json STRING, reasons ARRAY<STRING>, _quarantined_at TIMESTAMP)")
        checks = [f"IF(p IS NULL, 'malformed_json', NULL)",
                  f"IF(p.contract_version <=> '{CONTRACT_VERSION}', NULL, 'contract_version')"]
        checks += [f"IF(p.{f} IS NULL, 'missing:{f}', NULL)" for f, (_, r) in c["fields"].items() if r]
        for f, allowed in c["enums"].items():
            vals = ", ".join(f"'{v}'" for v in allowed if v is not None)
            checks.append(f"IF(p.{f} IS NOT NULL AND p.{f} NOT IN ({vals}), 'enum:{f}', NULL)")
        if ent == "audit_verdict":
            checks.append("IF(p.human_reviewed = false AND p.human_winner IS NOT NULL, 'human_winner_without_review', NULL)")
        if ent == "sft_row":  # rows seeded from outside text land with rights='unknown' and are held in quarantine
            checks.append("IF(lower(p.rights) = 'unknown', 'rights_unknown', NULL)")
        spark.sql(f"""CREATE OR REPLACE TEMP VIEW chk AS SELECT raw_id, payload_json, p,
            filter(array({', '.join(checks)}), x -> x IS NOT NULL) AS reasons
            FROM (SELECT raw_id, payload_json, from_json(payload_json, '{ddl}') AS p FROM {fq('raw_'+ent)})""")
        spark.sql(f"CREATE OR REPLACE TEMP VIEW ok AS SELECT raw_id, {', '.join('p.'+f+' AS '+f for f in cols)} FROM chk WHERE size(reasons)=0")
        spark.sql(f"CREATE OR REPLACE TEMP VIEW bad AS SELECT raw_id, payload_json, reasons, current_timestamp() AS _quarantined_at FROM chk WHERE size(reasons)>0")
        spark.sql(render_merge_sql(fq('validated_'+ent), "ok", "raw_id", ["raw_id"] + cols))
        spark.sql(f"MERGE INTO {fq('quarantine_'+ent)} t USING bad s ON t.raw_id=s.raw_id WHEN NOT MATCHED THEN INSERT *")
    else:
        extra = ""
        xcols = []
        if c["group"]:
            extra = f", {split_sql(c['group'])} AS split, '{SPLIT_METHOD_VERSION}' AS split_method"
            xcols = ["split", "split_method"]
        spark.sql(f"CREATE TABLE IF NOT EXISTS {fq('curated_'+ent)} ({ddl}{', split STRING, split_method STRING' if xcols else ''})")
        # latest landing wins per business key (dedupe before MERGE keeps it deterministic)
        spark.sql(f"""CREATE OR REPLACE TEMP VIEW cur AS SELECT {', '.join(cols)}{extra} FROM (
            SELECT *, row_number() OVER (PARTITION BY {key} ORDER BY landed_at DESC, raw_id) rn
            FROM {fq('validated_'+ent)}) WHERE rn=1""")
        spark.sql(render_merge_sql(fq('curated_'+ent), "cur", key, cols + xcols))
    print(f"[{stage}] {ent} done")
