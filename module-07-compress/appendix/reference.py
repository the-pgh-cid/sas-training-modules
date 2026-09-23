"""Appendix reference only; not a historical model response or general SAS emulator."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT_COLUMNS = ['case_id', 'row_id', 'text']
RESULT_COLUMNS = ['no_spaces', 'no_digits', 'only_letters']

def load_fixtures(path=HERE / "fixtures.csv"):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["row_id"] = pd.to_numeric(df["row_id"])
    return df

def translate(df):
    out = df.copy(deep=True)
    text = out["text"].str
    out["no_spaces"] = text.replace(
        " ", "", regex=False)
    out["no_digits"] = text.replace(
        "[0-9]", "", regex=True)
    out["only_letters"] = text.replace(
        "[^A-Za-z]", "", regex=True)
    return out


if __name__ == "__main__":
    fixture = load_fixtures()
    fixture = fixture.loc[fixture["case_id"].eq("fixture"), INPUT_COLUMNS]
    print(translate(fixture).to_string(index=False))
