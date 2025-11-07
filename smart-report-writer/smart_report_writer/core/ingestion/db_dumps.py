import sqlite3, io, os
from typing import Dict, Any

def inspect_sqlite(data: bytes) -> Dict[str, Any]:
    # sandbox: in-memory sqlite
    mem = sqlite3.connect(":memory:")
    with mem:
        tmp = "srw_temp.db"
        open(tmp, "wb").write(data)
        disk = sqlite3.connect(tmp)
        for row in disk.iterdump():
            try:
                mem.execute(row)
            except Exception:
                pass
        os.remove(tmp)
    cur = mem.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    return {"tables": [{"name": n, "sql": s} for (n,s) in cur.fetchall()]}
