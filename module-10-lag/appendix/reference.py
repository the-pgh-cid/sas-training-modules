"""LAG-to-shift reference only for calls executed on every input row."""
from pathlib import Path
import pandas as pd

SOURCE_COLUMNS = ['id', 'value']

def translate(df):
    out = df.copy(deep=True)
    out['prev_value'] = out['value'].shift(1)
    out['prev2_value'] = out['value'].shift(2)
    out['change'] = (
        out['value'] - out['prev_value'])
    return out

def load_cases():
    return pd.read_csv(Path(__file__).with_name('fixtures.csv'),
                       keep_default_na=False, na_values=['__MISSING__'])

if __name__ == '__main__':
    cases = load_cases()
    print(translate(cases.loc[cases.case_id.eq('fixture'), SOURCE_COLUMNS]).to_string(index=False))
