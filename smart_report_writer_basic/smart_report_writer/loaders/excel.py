from __future__ import annotations
import pandas as pd

def load_excel_sheets(path: str) -> list[pd.DataFrame]:
    tabs: list[pd.DataFrame] = []
    try:
        xl = pd.ExcelFile(path)
        for s in xl.sheet_names:
            try:
                df = xl.parse(s)
                df.attrs["__sheet__"] = s
                tabs.append(df)
            except Exception:
                pass
    except Exception:
        # Return empty on failure
        pass
    return tabs
