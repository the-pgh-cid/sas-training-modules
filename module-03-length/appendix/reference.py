"""Executable teaching reference; not a replay of an LLM response."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUTS = ['text']
OUTPUTS = ['len']
NUMERIC = ['expected_len']
WIDTHS = {'text': 10}


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
    out["text"] = out["text"].str.ljust(10)
    trimmed = out["text"].str.rstrip(" ")
    out["len"] = trimmed.str.len().clip(
        lower=1)
    return out


if __name__ == "__main__":
    cases = load_cases()
    result = translate(input_data(cases[cases.case_id == "fixture"]))
    print(result.to_string(index=False))
