"""Local ASCII COMPRESS reference and counterexamples, not original trial execution."""
import json
from pathlib import Path
import string
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODULE = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 7)


def reference(value):
    """Explicit character-set oracle for this exercise's content comparison."""
    return {
        'no_spaces': ''.join(c for c in value if c != ' '),
        'no_digits': ''.join(c for c in value if c not in string.digits),
        'only_letters': ''.join(c for c in value if c in string.ascii_letters),
    }


def converted(values):
    df = pd.DataFrame({'text': values})
    df['no_spaces'] = df['text'].str.replace(' ', '', regex=False)
    df['no_digits'] = df['text'].str.replace('[0-9]', '', regex=True)
    df['only_letters'] = df['text'].str.replace('[^A-Za-z]', '', regex=True)
    return df


def main():
    print('LOCAL PYTHON REFERENCE: MODULE 07 COMPRESS')
    print(f'Python {sys.version.split()[0]}; pandas {pd.__version__}')
    print('Hand-authored reference and reconstructed summary expression only.')
    print('No SAS execution, Bedrock calls, or original model-response execution.')
    sas = (ROOT / 'module-07-compress/example-07-compress-sas-snippet.sas').read_text()
    inputs = sas.split('  datalines;\n', 1)[1].split('\n;', 1)[0].splitlines()
    assert inputs == ['ABC 123 XYZ', 'Phone: 555-1234', 'ID-2023-Q4']
    assert all(s.isascii() and len(s) <= 20 for s in inputs)
    df = converted(inputs)
    columns = ['no_spaces', 'no_digits', 'only_letters']
    for index, col in enumerate(columns, 1):
        expected = [json.loads(row[index]) for row in MODULE['expected_rows']]
        assert df[col].tolist() == expected == [reference(s)[col] for s in inputs]
        print(f'PASS {col}: {expected!r}')
    assert df['text'].tolist() == inputs
    assert df.loc[0, 'no_digits'] == 'ABC  XYZ'
    print('PASS original inputs and row order preserved; both internal spaces retained.')

    # Reconstruct the expression reported for A1, not its absent full response.
    wrong = df['text'].str.replace('[^A-Za-z0-9]', '', regex=True)
    assert wrong.tolist() == ['ABC123XYZ', 'Phone5551234', 'ID2023Q4']
    assert wrong.ne(df['only_letters']).all()
    print(f'CHECK reported A1 expression: {wrong.tolist()!r}; all 3 rows fail letters-only.')
    alternate = df['text'].str.replace('[^a-zA-Z]', '', regex=True)
    assert alternate.tolist() == df['only_letters'].tolist()
    print('PASS A2/A3 reported letter-class spelling matches the B pattern for this fixture.')

    # Local teaching cases, separate from the three-row SAS fixture and historical trials.
    extra = ['', '1234', 'aB9_- !', 'A\t 1 B']
    ext = converted(extra)
    for col in columns:
        assert ext[col].tolist() == [reference(s)[col] for s in extra]
    assert ext.loc[3, 'no_spaces'] == 'A\t1B'
    assert ext.loc[2, 'no_digits'] == 'aB_- !'
    assert ext.loc[1, 'only_letters'] == ''
    print('PASS extra cases: empty input, digits only, mixed case, punctuation, and a tab.')
    print('CHECK literal-space removal retains a tab; broader whitespace removal would differ.')
    # Trailing blanks used for SAS storage are excluded by the prompt contract.
    for value in inputs:
        padded = value.ljust(20)
        for col in columns:
            assert reference(padded)[col].rstrip(' ') == reference(value)[col]
    print('PASS fixture content agrees after omitting width-20 trailing storage padding.')
    print('RESULT: local reference/counterexample checks passed; historical trial execution remains reported.')


if __name__ == '__main__':
    main()
