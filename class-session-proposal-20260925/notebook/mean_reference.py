"""Teaching reference adapted from module 01; not an observed model response."""
import pandas as pd


def candidate(df: pd.DataFrame) -> pd.DataFrame:
    """Append the row-wise mean without changing the supplied input table."""
    out = df.copy(deep=True)
    out["average"] = out[["x", "y", "z"]].mean(axis=1, skipna=True)
    return out
