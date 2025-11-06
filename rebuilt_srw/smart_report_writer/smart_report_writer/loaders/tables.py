from __future__ import annotations
import csv, json
import pandas as pd
from typing import Any, Dict

def sniff_delim(sample: str) -> str:
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except Exception:
        return ","

def load_table_like(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        delim = sniff_delim(sample)
        df = pd.read_csv(fh, sep=delim)
    return df

def profile_df(df: pd.DataFrame, name: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "name": name,
        "shape": list(df.shape),
        "columns": [],
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "sample": df.head(5).to_dict("records"),
    }
    for c in df.columns:
        s = df[c]
        d = {"name": str(c), "dtype": str(s.dtype), "n_null": int(s.isna().sum())}
        if pd.api.types.is_numeric_dtype(s):
            d.update({
                "min": float(s.min(skipna=True)),
                "max": float(s.max(skipna=True)),
                "mean": float(s.mean(skipna=True)),
                "p50": float(s.quantile(0.5)),
            })
        else:
            d.update({"unique": int(s.nunique(dropna=True))})
        info["columns"].append(d)
    return info
