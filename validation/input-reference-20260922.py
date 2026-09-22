"""Local INPUT reference and type counterexamples, not original trial execution."""
from datetime import datetime
import json
import locale
from pathlib import Path
import sys

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

ROOT = Path(__file__).resolve().parents[1]
MODULE = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 8)


def main():
    locale.setlocale(locale.LC_TIME, 'C')
    print('LOCAL PYTHON REFERENCE: MODULE 08 INPUT')
    print(f'Python {sys.version.split()[0]}; pandas {pd.__version__}; LC_TIME=C')
    print('Hand-authored reference and teaching counterexamples only.')
    print('No SAS execution, Bedrock calls, or original model-response execution.')
    sas = (ROOT / 'module-08-input/example-08-input-sas-snippet.sas').read_text()
    rows = [line.split() for line in sas.split('  datalines;\n', 1)[1].split('\n;', 1)[0].splitlines()]
    assert rows == [['123', '15JAN2023'], ['456', '01FEB2023'], ['789', '31DEC2023']]
    source = pd.DataFrame(rows, columns=['char_num', 'char_date'])
    df = source.copy(deep=True)
    df['num_value'] = pd.to_numeric(df['char_num'])
    df['date_value'] = pd.to_datetime(df['char_date'], format='%d%b%Y')
    expected_numbers = [int(row[2]) for row in MODULE['expected_rows']]
    expected_dates = [row[3] for row in MODULE['expected_rows']]
    assert df['num_value'].tolist() == expected_numbers == [123, 456, 789]
    assert df['date_value'].dt.strftime('%Y-%m-%d').tolist() == expected_dates
    assert is_numeric_dtype(df['num_value'])
    assert is_datetime64_any_dtype(df['date_value'])
    pd.testing.assert_frame_equal(df[['char_num', 'char_date']], source)
    assert df.columns.tolist() == ['char_num', 'char_date', 'num_value', 'date_value']
    print(f'PASS numeric values: {expected_numbers!r}; dtype={df["num_value"].dtype}')
    print(f'PASS calendar dates: {expected_dates!r}; dtype={df["date_value"].dtype}')
    print('PASS source string columns and row order preserved; result columns added.')

    # An independent calendar construction checks the parser against explicit components.
    months = {'JAN': 1, 'FEB': 2, 'DEC': 12}
    independent = [datetime(int(s[5:]), months[s[2:5]], int(s[:2])) for s in df['char_date']]
    assert df['date_value'].tolist() == independent
    assert df['num_value'].tolist() == [int(s) for s in df['char_num']]
    print('PASS independent integer/calendar-component reference agrees with pandas parsing.')

    # Display-only conversions can pass string checks while failing the required types.
    numeric_text = df['num_value'].astype(str)
    date_text = df['date_value'].dt.strftime('%Y-%m-%d')
    assert numeric_text.tolist() == ['123', '456', '789']
    assert date_text.tolist() == expected_dates
    assert not is_numeric_dtype(numeric_text)
    assert not is_datetime64_any_dtype(date_text)
    assert is_datetime64_any_dtype(df['date_value'])
    print('CHECK matching display strings fail numeric/datetime type requirements.')
    print('PASS formatting the comparison did not replace the stored datetime column.')

    # These examples are outside the original exercise, not added to reported trial scores.
    rejected = []
    for name, action in [('malformed number', lambda: pd.to_numeric(pd.Series(['12x']))),
                         ('invalid date', lambda: pd.to_datetime(pd.Series(['31FEB2023']), format='%d%b%Y'))]:
        try:
            action()
        except (ValueError, TypeError):
            rejected.append(name)
        else:
            raise AssertionError(f'{name} unexpectedly parsed')
    assert rejected == ['malformed number', 'invalid date']
    assert pd.to_numeric(pd.Series(['12x']), errors='coerce').isna().all()
    assert pd.to_datetime(pd.Series(['31FEB2023']), format='%d%b%Y', errors='coerce').isna().all()
    print('CHECK outside fixture: defaults reject malformed input; explicit coerce produces missing values.')
    print('No claim that pandas and SAS share invalid-input behavior or all informat semantics.')
    print('RESULT: local reference/counterexample checks passed; historical trial execution remains reported.')


if __name__ == '__main__':
    main()
