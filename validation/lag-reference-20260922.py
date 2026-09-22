"""Independent row-shift, queue and negative checks; not original trial execution."""
from collections import deque
import json
import platform
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text()) if m['id'] == 10)


def normalize(values):
    return [None if pd.isna(v) else int(v) for v in values]


def queue_reference(values, lag, execute=None):
    queue = deque([None] * lag)
    output = []
    for i, value in enumerate(values):
        if execute is None or execute[i]:
            output.append(queue.popleft())
            queue.append(value)
        else:
            output.append(None)
    return output


print('LOCAL PYTHON REFERENCE: MODULE 10 LAG / 2026-09-22')
print(f'Python {platform.python_version()}; pandas {pd.__version__}')
print('Reference and counterexamples only; not SAS execution or original Bedrock scripts.')
for dtype in ['int64', 'Int64']:
    df = pd.DataFrame({'id': range(1, 6), 'value': pd.Series([10, 15, 12, 18, 20], dtype=dtype)})
    df['prev_value'] = df['value'].shift(1)
    df['prev2_value'] = df['value'].shift(2)
    df['change'] = df['value'] - df['prev_value']
    actual = [['.' if pd.isna(v) else str(int(v)) for v in row] for row in df.values.tolist()]
    assert actual == module['expected_rows']
    assert df['id'].tolist() == [1, 2, 3, 4, 5]
    assert normalize(df['prev_value']) == queue_reference(df['value'], 1)
    assert normalize(df['prev2_value']) == queue_reference(df['value'], 2)
    assert normalize(df['change']) == [None, 5, -3, 6, 2]
    print(f'PASS dtype={dtype}: full five-row table, original ids, all missing positions, independent LAG/LAG2 queues.')

# These counterexamples deliberately violate the contract and must be caught.
filled_change = df['value'] - df['prev_value'].fillna(0)
assert filled_change.iloc[0] == 10 and pd.isna(df['change'].iloc[0])
print('EXPECTED ANTI-PATTERN: fillna(0) creates first change=10 instead of missing.')
wrapped_previous = [20, 10, 15, 12, 18]
assert wrapped_previous[0] != normalize(df['prev_value'])[0]
print('EXPECTED ANTI-PATTERN: wrapping the final value produces first prior=20 instead of missing.')
sorted_values = df.sort_values('value')['value']
assert sorted_values.index.tolist() != df.index.tolist()
assert (sorted_values-sorted_values.shift(1)).loc[2] == 2
assert df.loc[2, 'change'] == -3
print('EXPECTED ANTI-PATTERN: sorting by value changes id 3 change from -3 to 2.')

# Separate scenario: only rows 2 and 4 execute a particular LAG occurrence.
# This models a conditional assignment to a non-retained result variable.
mask = [False, True, False, True, False]
conditional = queue_reference(df['value'], 1, mask)
unconditional_then_mask = normalize(df['value'].shift(1).where(mask))
assert conditional == [None, None, None, 15, None]
assert unconditional_then_mask == [None, 10, None, 12, None]
assert conditional != unconditional_then_mask
print('Conditional queue (execute rows 2,4):', normalize(conditional))
print('Unconditional row shift then mask:   ', unconditional_then_mask)
print('PASS scope counterexample: conditional call history differs from original-row shift.')
print('prev_value: ', normalize(df['prev_value']))
print('prev2_value:', normalize(df['prev2_value']))
print('change:     ', normalize(df['change']))
print('All local checks passed. Shift equivalence is limited to the supplied per-row calls.')
