import pandas as pd
from io import BytesIO
from typing import Dict, Any

def load_table(data: bytes, filename: str) -> pd.DataFrame:
    name = filename.lower()
    if name.endswith(".csv") or name.endswith(".tsv"):
        sep = "\t" if name.endswith(".tsv") else ","
        return pd.read_csv(BytesIO(data), sep=sep)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(BytesIO(data))
    if name.endswith(".json"):
        return pd.read_json(BytesIO(data))
    if name.endswith(".jsonl"):
        return pd.read_json(BytesIO(data), lines=True)
    if name.endswith(".xml"):
        return pd.read_xml(BytesIO(data))
    if name.endswith(".parquet"):
        return pd.read_parquet(BytesIO(data))
    raise ValueError("Unsupported table format")

def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    profile = {
        "rows": len(df),
        "cols": len(df.columns),
        "columns": []
    }
    for c in df.columns:
        s = df[c]
        stats = {}
        try:
            stats = {
                "min": s.min(),
                "max": s.max(),
                "mean": s.mean(),
                "std": s.std(),
            }
        except Exception:
            stats = {}

        profile["columns"].append({
            "name": str(c),
            "type": str(s.dtype),
            "nulls": int(s.isna().sum()),
            "unique": int(s.nunique()),
            "stats": stats,
            "sample_values": s.head(5).tolist(),
        })
    return profile
