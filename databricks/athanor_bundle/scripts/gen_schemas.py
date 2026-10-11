import json, os, sys
R = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, R + "/src")
from athanor_data.contracts import CONTRACTS, CONTRACT_VERSION
J = {"string": "string", "bigint": "integer", "double": "number", "boolean": "boolean"}
for e, c in CONTRACTS.items():
    props = {f: {"type": [J[t]] + ([] if req else ["null"])} for f, (t, req) in c["fields"].items()}
    for f, v in c["enums"].items():
        props[f]["enum"] = v
    s = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{CONTRACT_VERSION}.{e}",
         "type": "object", "additionalProperties": False, "properties": props,
         "required": [f for f, (_, r) in c["fields"].items() if r]}
    open(f"{R}/contracts/{e}.v1.schema.json", "w").write(json.dumps(s, indent=2) + "\n")
