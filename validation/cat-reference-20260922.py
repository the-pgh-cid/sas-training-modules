"""Local CAT/CATX reference and counterexamples, not original trial execution.

Scope: the supplied ASCII character fixture (fields <= 8, outputs <= 24).
Not a general SAS parser or implementation of numeric/overflow/encoding rules.
"""
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODULE = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 4)


def catx_space(fields):
    """The exercise's character-only CATX rule, before output storage padding."""
    return ' '.join(v.strip(' ') for v in fields if v.strip(' '))


def main():
    print('LOCAL PYTHON REFERENCE: MODULE 04 CAT/CATX')
    print(f'Python {sys.version.split()[0]}; pandas {pd.__version__}')
    print('Hand-authored fixture checks and reconstructed summary snippets only.')
    print('No SAS execution, Bedrock calls, or original model-response execution.')
    sas = (ROOT / 'module-04-cat/example-04-cat-sas-snippet.sas').read_text()
    datalines = sas.split('    datalines;\n', 1)[1].split('\n;', 1)[0]
    raw_rows = [line.split() for line in datalines.splitlines()]
    assert raw_rows == [['John', 'Q', 'Public'], ['Jane', '.', 'Doe'], ['Bob', '.', 'Smith']]
    assert all(len(v) <= 8 for row in raw_rows for v in row)
    cols = ['first', 'middle', 'last']
    df = pd.DataFrame(raw_rows, columns=cols).replace('.', '')
    for col in cols:
        df[col] = df[col].str.ljust(8)
    original_inputs = df.copy(deep=True)
    df['name1'] = df['first'] + df['middle'] + df['last']
    df['name2'] = df[cols].apply(catx_space, axis=1).str.ljust(24)
    expected_cat = ['John____Q_______Public__', 'Jane____________Doe_____',
                    'Bob_____________Smith___']
    expected_names = ['John Q Public', 'Jane Doe', 'Bob Smith']
    assert [r[1] for r in MODULE['expected_rows']] == expected_cat
    assert [r[2] for r in MODULE['expected_rows']] == expected_names
    assert df['name1'].tolist() == [v.replace('_', ' ') for v in expected_cat]
    assert df['name2'].tolist() == [v.ljust(24) for v in expected_names]
    assert df[cols].apply(lambda s: s.str.len().eq(8)).all().all()
    assert df[['name1', 'name2']].apply(lambda s: s.str.len().eq(24)).all().all()
    assert df.loc[1:, 'middle'].tolist() == [' ' * 8] * 2
    # Readable and visible-space displays must not mutate storage.
    stored = df.copy(deep=True)
    visible = df['name1'].str.replace(' ', '_', regex=False)
    readable = df['name2'].str.rstrip(' ')
    pd.testing.assert_frame_equal(df, stored)
    pd.testing.assert_frame_equal(df[cols], original_inputs)
    for i, (cat, catx) in enumerate(zip(visible, readable), 1):
        print(f'PASS row {i}: CAT={cat}; CATX={catx!r}; stored widths=24/24')
    print('PASS input widths=8; missing middle fields=8 spaces; row order and storage preserved.')

    # Apply the recipes described in A summaries, without claiming a raw-run replay.
    raw_cat = [''.join(row) for row in raw_rows]
    raw_join = [' '.join(row) for row in raw_rows]
    filter_join = [' '.join(v for v in row if v != '.') for row in raw_rows]
    assert raw_cat == ['JohnQPublic', 'Jane.Doe', 'Bob.Smith']
    assert raw_join == ['John Q Public', 'Jane . Doe', 'Bob . Smith']
    assert filter_join == expected_names
    assert list(map(len, filter_join)) == [13, 8, 9]
    print('CHECK summary recipes: raw + loses CAT padding; unfiltered join retains missing dots.')
    print('CHECK filter/join: readable names match; stored widths are 13, 8, 9 instead of 24.')

    # Additional teaching counterexamples; not added to the tested SAS fixture.
    assert catx_space([' Jane   ', '        ', 'Doe     ']) == 'Jane Doe'
    assert catx_space(['        '] * 3) == ''
    assert catx_space(['        '] * 3).ljust(24) == ' ' * 24
    assert catx_space([' Mary Ann ', '', ' Lee ']) == 'Mary Ann Lee'
    assert catx_space(['\tA ', '', ' B\t']) == '\tA B\t'
    assert catx_space(['Jane', '.', 'Doe']) == 'Jane . Doe'
    print('PASS CATX checks: ordinary outer spaces, all-blank fields, internal spaces, tabs, literal dot.')
    # Several idioms are equivalent once the same stored values are supplied.
    for row, expected in zip(df[cols].itertuples(index=False, name=None), expected_cat):
        a, b, c = row
        assert a+b+c == ''.join(row) == f'{a}{b}{c}' == expected.replace('_', ' ')
    print('PASS +, join and f-strings agree on the same padded CAT inputs.')
    print('RESULT: local reference and counterexample checks passed; reported A/B trials remain separate.')


if __name__ == '__main__':
    main()
