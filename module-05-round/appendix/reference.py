"""Appendix reference only; not a historical model response or general SAS emulator."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT_COLUMNS = ['case_id', 'row_id', 'value']
RESULT_COLUMNS = ['rounded']

def load_fixtures(path=HERE / "fixtures.csv"):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["row_id"] = pd.to_numeric(df["row_id"])
    df['value'] = pd.to_numeric(df['value'].replace("__MISSING__", None))
    df['expected_rounded'] = pd.to_numeric(df['expected_rounded'].replace("__MISSING__", None))
    return df

def translate(df):
    out = df.copy(deep=True)
    out["rounded"] = out["value"].round(0)
    return out


if __name__ == "__main__":
    fixture = load_fixtures()
    fixture = fixture.loc[fixture["case_id"].eq("fixture"), INPUT_COLUMNS]
    print(translate(fixture).to_string(index=False))
