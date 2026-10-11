def render_merge_sql(target_table: str, source_view: str, key: str, columns: list[str]) -> str:
    set_clause = ", ".join(f"t.{c}=s.{c}" for c in columns if c != key)
    return (f"MERGE INTO {target_table} AS t\nUSING {source_view} AS s\nON t.{key}=s.{key}\n"
            f"WHEN MATCHED THEN UPDATE SET {set_clause}\n"
            f"WHEN NOT MATCHED THEN INSERT ({', '.join(columns)}) VALUES ({', '.join('s.'+c for c in columns)})")
