"""Local INTCK reference/counterexample review; not SAS or Bedrock execution."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
import json
import platform

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def count_boundaries(start, end):
    """Enumerate actual calendar transitions, independently of year/month formulas."""
    counts = [0, 0, 0]
    day = start
    while day < end:
        day += timedelta(days=1)
        counts[0] += 1
        counts[1] += day.day == 1
        counts[2] += day.day == 1 and day.month == 1
    return counts


def main():
    module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
                  if m['id'] == 6)
    source = (ROOT / 'module-06-intck/example-06-intck-sas-snippet.sas').read_text()
    pairs = [line.split() for line in source.split('datalines;', 1)[1].split(';', 1)[0].strip().splitlines()]
    frame = pd.DataFrame(pairs, columns=['start_date', 'end_date'])
    original = frame.copy(deep=True)
    for column in ['start_date', 'end_date']:
        frame[column] = pd.to_datetime(frame[column], format='%d%b%Y')
    start, end = frame['start_date'], frame['end_date']
    frame['days'] = (end - start).dt.days
    frame['months'] = 12 * (end.dt.year - start.dt.year) + end.dt.month - start.dt.month
    frame['years'] = end.dt.year - start.dt.year
    expected = [[int(v) for v in row[2:]] for row in module['expected_rows']]
    actual = frame[['days', 'months', 'years']].values.tolist()
    assert actual == expected
    assert frame.index.equals(original.index)
    for column in ['start_date', 'end_date']:
        assert frame[column].dt.strftime('%d%b%Y').str.upper().tolist() == original[column].tolist()
    enumerated = [count_boundaries(datetime.strptime(a, '%d%b%Y').date(),
                                  datetime.strptime(b, '%d%b%Y').date()) for a,b in pairs]
    assert enumerated == expected
    # Reconstruct the method reported for A1. This is not its complete transcript.
    applied = frame.apply(lambda r: pd.Series([
        (r.end_date - r.start_date).days,
        12 * (r.end_date.year - r.start_date.year) + r.end_date.month - r.start_date.month,
        r.end_date.year - r.start_date.year,
    ]), axis=1)
    assert applied.values.tolist() == expected
    wrong_months = (frame['days'] // 30).tolist()
    expected_months = frame['months'].tolist()
    rejected_rows = [i+1 for i,(a,b) in enumerate(zip(wrong_months, expected_months)) if a != b]
    assert rejected_rows == [3, 5, 6]
    assert frame.loc[4, ['days','months','years']].tolist() == [1,1,0]
    assert frame.loc[5, ['days','months','years']].tolist() == [1,1,1]

    print('INTCK LOCAL REFERENCE REVIEW / 22 SEP 2026')
    print(f'Python {platform.python_version()}; pandas {pd.__version__}')
    print('Local reference checks only; no SAS execution and no new Bedrock trials.')
    print('Scope: ordinary discrete day/month/year intervals on the six date-only rows.')
    for column in ['days', 'months', 'years']:
        print(column + ': ' + repr(frame[column].tolist()))
    print('PASS: all 18 results; original date values and row order retained.')
    print('PASS: independently enumerated calendar transitions agree with all formulas.')
    print('PASS: reconstructed functions/.apply() and inline methods agree on this fixture.')
    print('COUNTEREXAMPLE: elapsed days // 30 gives ' + repr(wrong_months))
    print('Rejected rows: ' + repr(rejected_rows))
    print('PASS: Jan 31 -> Feb 1 is [1 day, 1 month, 0 years].')
    print('PASS: Dec 31 -> Jan 1 is [1 day, 1 month, 1 year].')
    print('No performance benchmark or general interval equivalence is claimed.')


if __name__ == '__main__':
    output = StringIO()
    with redirect_stdout(output):
        main()
    report = output.getvalue()
    Path(__file__).with_suffix('.txt').write_text(report)
    print(report, end='')
