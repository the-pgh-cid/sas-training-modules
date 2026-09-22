"""Local Python reference checks. Not SAS execution or Bedrock prompt trials.

These assertions check the module's stated expectations against deliberately
written reference translations for the supplied inputs. They do not measure
model repeatability, authenticate SAS results, or establish general equivalence.
"""
from collections import deque
from datetime import date
from io import StringIO
from pathlib import Path
import contextlib
import json
import platform

import pandas as pd


HERE = Path(__file__).parent
MODULES = {m['id']: m for m in json.loads((HERE / 'modules_06_10.json').read_text())}


def compare_table(module_id, actual):
    expected = MODULES[module_id]['expected_rows']
    assert actual == expected, (module_id, actual, expected)


def intck_reference():
    pairs = [
        ('01JAN2023', '15JAN2023'), ('01JAN2023', '01FEB2023'),
        ('01JAN2023', '31DEC2023'), ('15MAR2023', '20MAR2023'),
        ('31JAN2023', '01FEB2023'), ('31DEC2023', '01JAN2024'),
    ]
    df = pd.DataFrame(pairs, columns=['start_date', 'end_date'])
    start = pd.to_datetime(df['start_date'], format='%d%b%Y')
    end = pd.to_datetime(df['end_date'], format='%d%b%Y')
    df['days'] = (end - start).dt.days
    df['months'] = (end.dt.year - start.dt.year) * 12 + end.dt.month - start.dt.month
    df['years'] = end.dt.year - start.dt.year
    compare_table(6, df.astype(str).values.tolist())
    # Independently identify an intervening first-of-month for contrast rows.
    assert date(2023, 1, 31) < date(2023, 2, 1) <= date(2023, 2, 1)
    assert df.loc[4, 'days'] == 1 and df.loc[4, 'months'] == 1
    assert df.loc[5, 'days'] == 1 and df.loc[5, 'years'] == 1
    print('06 INTCK: PASS, all 6 rows and 3 calculated columns match expectations.')


def compress_reference():
    df = pd.DataFrame({'text': ['ABC 123 XYZ', 'Phone: 555-1234', 'ID-2023-Q4']})
    df['no_spaces'] = df['text'].str.replace(' ', '', regex=False)
    df['no_digits'] = df['text'].str.replace('[0-9]', '', regex=True)
    df['only_letters'] = df['text'].str.replace('[^A-Za-z]', '', regex=True)
    actual = [[json.dumps(v) for v in row] for row in df.values.tolist()]
    compare_table(7, actual)
    # Check equivalent ASCII transformations against character filtering.
    for row in df.itertuples(index=False):
        assert row.no_spaces == ''.join(c for c in row.text if c != ' ')
        assert row.no_digits == ''.join(c for c in row.text if c not in '0123456789')
        assert row.only_letters == ''.join(c for c in row.text if c.isalpha())
    assert df.loc[0, 'no_digits'].count(' ') == 2
    print('07 COMPRESS: PASS, all 3 rows match, including 2 preserved internal spaces.')


def input_reference():
    df = pd.DataFrame({
        'char_num': ['123', '456', '789'],
        'char_date': ['15JAN2023', '01FEB2023', '31DEC2023'],
    })
    df['num_value'] = pd.to_numeric(df['char_num'])
    df['date_value'] = pd.to_datetime(df['char_date'], format='%d%b%Y')
    assert pd.api.types.is_numeric_dtype(df['num_value'])
    assert pd.api.types.is_datetime64_any_dtype(df['date_value'])
    assert df['date_value'].dt.date.tolist() == [date(2023, 1, 15), date(2023, 2, 1), date(2023, 12, 31)]
    actual = [
        [json.dumps(row.char_num), json.dumps(row.char_date), str(row.num_value), row.date_value.strftime('%Y-%m-%d')]
        for row in df.itertuples(index=False)
    ]
    compare_table(8, actual)
    print('08 INPUT: PASS, all 3 rows, calendar dates, numeric and datetime types match.')


def first_last_reference():
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'group': ['A', 'A', 'B', 'B', 'B', 'C'],
        'value': [10, 20, 30, 40, 50, 60],
    })
    assert df['group'].is_monotonic_increasing
    assert df['group'].notna().all()
    first = df['group'].ne(df['group'].shift(1))
    last = df['group'].ne(df['group'].shift(-1))
    first.iloc[0] = True
    last.iloc[-1] = True
    df['first_flag'] = first.astype(int)
    df['last_flag'] = last.astype(int)
    # Independent grouping counts provide a second route for this sorted sample.
    assert df['first_flag'].equals(df.groupby('group', sort=False).cumcount().eq(0).astype(int))
    assert df['last_flag'].equals(df.groupby('group', sort=False).cumcount(ascending=False).eq(0).astype(int))
    compare_table(9, df.astype(str).values.tolist())
    print('09 FIRST./LAST.: PASS, all 6 rows, order, and singleton-group flags match.')


def lag_reference():
    df = pd.DataFrame({'id': [1, 2, 3, 4, 5], 'value': [10, 15, 12, 18, 20]})
    df['prev_value'] = df['value'].shift(1)
    df['prev2_value'] = df['value'].shift(2)
    df['change'] = df['value'] - df['prev_value']
    actual = [['.' if pd.isna(v) else str(int(v)) for v in row] for row in df.values.tolist()]
    compare_table(10, actual)
    # Simulate two separate queues executed once per input row.
    queues = [deque([None]), deque([None, None])]
    for row in df.itertuples(index=False):
        expected = []
        for queue in queues:
            expected.append(queue.popleft())
            queue.append(row.value)
        for reference, translated in zip(expected, (row.prev_value, row.prev2_value)):
            assert pd.isna(translated) if reference is None else translated == reference
    print('10 LAG: PASS, all 5 rows and missing positions match per-row queue checks.')


def main():
    print('LOCAL PYTHON REFERENCE CHECKS: EXAMPLES 06-10')
    print(f'Python {platform.python_version()}; pandas {pd.__version__}')
    print('These are not SAS executions and not AWS Bedrock A/B trials.')
    print('Expected SAS results remain subject to execution in the target SAS environment.')
    print()
    intck_reference()
    compress_reference()
    input_reference()
    first_last_reference()
    lag_reference()
    print()
    print('All local Python reference checks passed.')


if __name__ == '__main__':
    buffer = StringIO()
    with contextlib.redirect_stdout(buffer):
        main()
    report = buffer.getvalue()
    (HERE / 'local_validation_06_10.txt').write_text(report)
    print(report, end='')
