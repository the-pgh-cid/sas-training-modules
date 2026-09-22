"""Independent fixture checks and endpoint counterexample; not a Bedrock replay."""
import json
import platform
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text()) if m['id'] == 9)
expected_first = [1, 0, 1, 0, 0, 1]
expected_last = [0, 1, 0, 0, 1, 1]


def flags(group):
    """Explicit positional endpoints; sample has no missing group values."""
    first = group.ne(group.shift(1))
    last = group.ne(group.shift(-1))
    first.iloc[0] = True
    last.iloc[-1] = True
    return first.astype(int), last.astype(int)


print('LOCAL PYTHON REFERENCE: MODULE 09 FIRST./LAST. / 2026-09-22')
print(f'Python {platform.python_version()}; pandas {pd.__version__}')
print('Reference and counterexamples only; not SAS execution or original Bedrock scripts.')
for dtype in ['object', 'string']:
    df = pd.DataFrame({'id': range(1, 7), 'group': pd.Series(['A', 'A', 'B', 'B', 'B', 'C'], dtype=dtype),
                       'value': [10, 20, 30, 40, 50, 60]})
    assert df['group'].notna().all() and df['group'].is_monotonic_increasing
    df['first_flag'], df['last_flag'] = flags(df['group'])
    assert df['first_flag'].tolist() == expected_first
    assert df['last_flag'].tolist() == expected_last
    assert df.astype(str).values.tolist() == module['expected_rows']
    assert pd.api.types.is_integer_dtype(df['first_flag'])
    assert pd.api.types.is_integer_dtype(df['last_flag'])
    first_count = df.groupby('group', sort=False).cumcount().eq(0).astype(int)
    last_count = df.groupby('group', sort=False).cumcount(ascending=False).eq(0).astype(int)
    assert first_count.equals(df['first_flag']) and last_count.equals(df['last_flag'])
    print(f'PASS dtype={dtype}: full six-row table, id order, integer flags, singleton, independent group counts.')
    if dtype == 'object':
        # Reconstruct the expressions shown in the trial log, not missing full scripts.
        assert df['group'].ne(df['group'].shift(1)).astype(int).tolist() == expected_first
        assert df['group'].ne(df['group'].shift(-1)).astype(int).tolist() == expected_last
        print('PASS object reconstruction: unguarded B2/B3 expressions match this fixture.')
    else:
        raw_first = df['group'].ne(df['group'].shift(1))
        raw_last = df['group'].ne(df['group'].shift(-1))
        assert pd.isna(raw_first.iloc[0]) and pd.isna(raw_last.iloc[-1])
        print(f'Nullable string unguarded first comparisons: {raw_first.tolist()}')
        print(f'Nullable string unguarded last comparisons: {raw_last.tolist()}')
        for raw in [raw_first, raw_last]:
            try:
                raw.astype(int)
            except ValueError as exc:
                print(f'EXPECTED COUNTEREXAMPLE: {type(exc).__name__}: {exc}')
            else:
                raise AssertionError('Expected nullable endpoint conversion failure')
        # Changed labels show why endpoints should be positional outside this fixture.
        df.index = [10, 20, 30, 40, 50, 60]
        a, b = flags(df['group'])
        assert a.tolist() == expected_first and b.tolist() == expected_last
        assert (df.index == 0).sum() == 0 and (df.index == len(df)-1).sum() == 0
        print('PASS positional endpoint handling also survives non-default index labels.')

# Show why checking only boundary records is not equivalent to flagging all rows.
keep = df.loc[df['first_flag'].eq(1) | df['last_flag'].eq(1), 'id'].tolist()
assert keep == [1, 2, 3, 5, 6]
print(f'EXPECTED ANTI-PATTERN: keeping only boundary rows drops id 4; remaining ids={keep}.')
print('first_flag:', expected_first)
print('last_flag: ', expected_last)
print('Scope: single nonmissing key, sorted fixture; no multi-key/NOTSORTED equivalence claimed.')
print('All local checks passed. Reported B2/B3 output matches do not satisfy explicit-endpoint wording.')
