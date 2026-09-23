"""Executable teaching reference; not a replay of an LLM response."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUTS = ['text']
OUTPUTS = ['first_three', 'middle', 'from_seventh']
NUMERIC = []
WIDTHS = {'text': 20, 'first_three': 3, 'middle': 4, 'from_seventh': 14}


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
    out["text"] = out["text"].str.ljust(20)
    s = out["text"].str
    out["first_three"] = s.slice(0, 3)
    out["middle"] = s.slice(4, 8)
    out["from_seventh"] = s.slice(6, None)
    return out


if __name__ == "__main__":
    cases = load_cases()
    result = translate(input_data(cases[cases.case_id == "fixture"]))
    print(result.to_string(index=False))
