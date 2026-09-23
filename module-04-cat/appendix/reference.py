"""Executable teaching reference; not a replay of an LLM response."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUTS = ['first', 'middle', 'last']
OUTPUTS = ['name1', 'name2']
NUMERIC = []
WIDTHS = {'first': 8, 'middle': 8, 'last': 8, 'name1': 24, 'name2': 24}


def load_cases():
    data = pd.read_csv(HERE / "fixtures.csv", dtype=str,
                       keep_default_na=False, na_filter=False)
    for column in NUMERIC:
        data[column] = pd.to_numeric(data[column].replace("__MISSING__", float("nan")))
    return data


def input_data(cases):
    return cases[["case_id", "row_id"] + INPUTS].copy(deep=True)


def catx_space(row):
    parts = [v.strip(" ") for v in row]
    return " ".join(v for v in parts if v)


def translate(df):
    out = df.copy(deep=True)
    cols = ["first", "middle", "last"]
    for col in cols:
        out[col] = out[col].str.ljust(8)
    out["name1"] = (
        out["first"] + out["middle"]
        + out["last"])
    out["name2"] = out[cols].apply(
        catx_space, axis=1).str.ljust(24)
    return out


if __name__ == "__main__":
    cases = load_cases()
    result = translate(input_data(cases[cases.case_id == "fixture"]))
    print(result.to_string(index=False))
