"""Valid English numeric/date input reference; no general SAS INPUT equivalence."""
from pathlib import Path
import locale
import pandas as pd

SOURCE_COLUMNS = ['char_num', 'char_date']

def english_dates(text):
    old_locale = locale.setlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, 'C')
        return pd.to_datetime(text, format='%d%b%Y')
    finally:
        locale.setlocale(locale.LC_TIME, old_locale)

def translate(df):
    out = df.copy(deep=True)
    out['num_value'] = pd.to_numeric(
        out['char_num'])
    out['date_value'] = english_dates(
        out['char_date'])
    return out

def load_cases():
    return pd.read_csv(Path(__file__).with_name('fixtures.csv'),
                       dtype={'char_num': str, 'char_date': str},
                       keep_default_na=False, na_values=['__MISSING__'])

if __name__ == '__main__':
    cases = load_cases()
    print(translate(cases.loc[cases.case_id.eq('fixture'), SOURCE_COLUMNS]).to_string(index=False))
