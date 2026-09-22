"""Local ROUND checks; not SAS execution or a rerun of Bedrock responses.

The five-row exercise remains unchanged. Halfway probes below are independent
review counterexamples, outside the teaching fixture and Prompt B's scope.
"""
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_HALF_UP
from io import StringIO
from pathlib import Path
import csv
import json
import platform

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
                  if m['id'] == 5)
    source = (ROOT / 'module-05-round/example-05-round-sas-snippet.sas').read_text()
    tokens = source.split('datalines;', 1)[1].split(';', 1)[0].split()
    values = [float(t) for t in tokens]
    assert values == [2.3, 2.7, -1.4, -1.6, 3.0]
    frame = pd.DataFrame({'value': values})
    original = frame.copy(deep=True)
    frame['rounded'] = frame['value'].round(0)
    expected = [int(row[2]) for row in module['expected_rows']]
    assert frame['rounded'].tolist() == expected == [2, 3, -1, -2, 3]
    assert frame['value'].equals(original['value'])
    assert frame.index.equals(original.index)
    # Independent decimal arithmetic checks the documented simple unit-1 result.
    reference = [int(Decimal(t).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) for t in tokens]
    assert reference == expected
    assert frame['value'].round().equals(frame['rounded'])
    with (ROOT / 'module-05-round/results-20260921.csv').open(newline='') as stream:
        reported = list(csv.DictReader(stream))
    assert sum(r['Understanding_Correct'] == 'YES' for r in reported[:3]) == 2

    print('ROUND LOCAL REFERENCE REVIEW / 22 SEP 2026')
    print(f'Python {platform.python_version()}; pandas {pd.__version__}; NumPy {np.__version__}')
    print('Local reference checks only; no SAS execution and no new Bedrock trials.')
    print('Fixture: ' + repr(values))
    print('pandas .round() and .round(0): ' + repr(frame['rounded'].tolist()))
    print('Independent decimal unit-1 check: ' + repr(reference))
    print('PASS: all five values, numeric equality, row order and unchanged inputs.')
    print('Source reconciliation: A2 and A3 explain ties correctly; 2/3, not 1/3.')
    print()
    print('OUTSIDE-EXERCISE COUNTEREXAMPLES: unchanged teaching fixture')
    probes = pd.Series([2.5, -2.5, 3.5, -3.5])
    pandas_ties = probes.round(0).astype(int).tolist()
    away_ties = [int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) for v in probes]
    assert pandas_ties == [2, -2, 4, -4]
    assert away_ties == [3, -3, 4, -4]
    assert pandas_ties != away_ties
    print('Exact ties: ' + repr(probes.tolist()))
    print('pandas to-even results: ' + repr(pandas_ties))
    print('Documented SAS tie direction, modeled in Decimal: ' + repr(away_ties))
    print('PASS: 2.5 and -2.5 distinguish the rules; 3.5 and -3.5 do not.')
    alternative = np.where(probes >= 0, np.floor(probes + 0.5), np.ceil(probes - 0.5))
    assert alternative.astype(int).tolist() == away_ties
    print('A2 floor/ceil recipe passes these exact ties only; no general SAS-equivalence claim.')
    print('SAS ROUND also documents near-halfway handling and fuzzing; no SAS run was made.')
    print('PASS: bounded checks completed.')


if __name__ == '__main__':
    output = StringIO()
    with redirect_stdout(output):
        main()
    report = output.getvalue()
    Path(__file__).with_suffix('.txt').write_text(report)
    print(report, end='')
