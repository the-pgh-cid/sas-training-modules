"""Appendix reference only; not a historical model response or general SAS emulator."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT_COLUMNS = ['case_id', 'row_id', 'start_date', 'end_date']
RESULT_COLUMNS = ['days', 'months', 'years']

def load_fixtures(path=HERE / "fixtures.csv"):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["row_id"] = pd.to_numeric(df["row_id"])
    df['expected_days'] = pd.to_numeric(df['expected_days'].replace("__MISSING__", None))
    df['expected_months'] = pd.to_numeric(df['expected_months'].replace("__MISSING__", None))
    df['expected_years'] = pd.to_numeric(df['expected_years'].replace("__MISSING__", None))
    return df

# Explicit English month mapping avoids depending on the process locale.
MONTHS = dict(zip(
    "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(),
    [f"{m:02}" for m in range(1, 13)]))


def parse_date9(series):
    iso = (series.str[5:] + "-" + series.str[2:5].map(MONTHS)
           + "-" + series.str[:2])
    return pd.to_datetime(iso, format="%Y-%m-%d")


def translate(df):
    out = df.copy(deep=True)
    out["start_date"] = parse_date9(
        out["start_date"])
    out["end_date"] = parse_date9(
        out["end_date"])
    s = out["start_date"].dt
    e = out["end_date"].dt
    out["days"] = (
        out["end_date"] - out["start_date"]
    ).dt.days
    out["years"] = e.year - s.year
    out["months"] = (
        12*out["years"] + e.month-s.month)
    return out


if __name__ == "__main__":
    fixture = load_fixtures()
    fixture = fixture.loc[fixture["case_id"].eq("fixture"), INPUT_COLUMNS]
    print(translate(fixture).to_string(index=False))
