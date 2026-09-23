"""One sorted nonmissing group key; flag every row with explicit endpoints."""
from pathlib import Path
import pandas as pd

SOURCE_COLUMNS = ['id', 'group', 'value']

def translate(df):
    out = df.copy(deep=True)
    group = out['group']
    if group.isna().any() or not group.is_monotonic_increasing:
        raise ValueError('Expected sorted, nonmissing groups')
    first = group.ne(group.shift(1))
    last = group.ne(group.shift(-1))
    if len(out):
        first.iloc[0] = True
        last.iloc[-1] = True
    out['first_flag'] = first.astype(int)
    out['last_flag'] = last.astype(int)
    return out

def load_cases():
    return pd.read_csv(Path(__file__).with_name('fixtures.csv'),
                       dtype={'group': 'string'},
                       keep_default_na=False, na_values=['__MISSING__'])

if __name__ == '__main__':
    cases = load_cases()
    print(translate(cases.loc[cases.case_id.eq('fixture'), SOURCE_COLUMNS]).to_string(index=False))
