"""Executable teaching reference; not a replay of an LLM response."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUTS = ['x', 'y', 'z']
OUTPUTS = ['average']
NUMERIC = ['x', 'y', 'z', 'expected_average']
WIDTHS = {}


def load_cases():
    data = pd.read_csv(HERE / "fixtures.csv", dtype=str,
                       keep_default_na=False, na_filter=False)
    for column in NUMERIC:
        data[column] = pd.to_numeric(data[column].replace("__MISSING__", float("nan")))
    return data


def input_data(cases):
    return cases[["case_id", "row_id"] + INPUTS].copy(deep=True)


def translate(df):
    out = df.copy(deep=True)
    cols = ["x", "y", "z"]
    out["average"] = out[cols].mean(
        axis=1, skipna=True)
    return out


if __name__ == "__main__":
    cases = load_cases()
    result = translate(input_data(cases[cases.case_id == "fixture"]))
    print(result.to_string(index=False))
