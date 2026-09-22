"""Local ASCII fixture checks, not a replay of the reported LLM transcripts."""
import pandas as pd


def length_reference(text):
    return text.str.rstrip(' ').str.len().clip(lower=1)


source = pd.Series(['ABC', 'ABC', 'ABCDEFGHIJ', 'X', ''])
stored = source.str.pad(10, side='right', fillchar=' ')
before = stored.copy()
expected = [3, 3, 10, 1, 1]
assert stored.str.len().tolist() == [10] * 5
assert stored.iloc[-1] == ' ' * 10
assert length_reference(stored).tolist() == expected
assert stored.equals(before)
print('PASS: five reference values, width 10, blank storage and unchanged source text.')

reported_a_example = pd.Series(['ABC', 'ABC', 'ABCDEFGHIJ', 'X', '.'])
assert reported_a_example.str.len().tolist() == expected
assert reported_a_example.str.len().tolist() != [10] * 5
assert reported_a_example.iloc[-1] != ' ' * 10
print('PASS: reconstructed A-style example matches values but fails storage and missing checks.')

counterexamples = pd.Series(['ABC   ', '', ' ABC '])
assert counterexamples.str.len().tolist() == [6, 0, 5]
assert length_reference(counterexamples).tolist() == [3, 1, 4]
for value, direct, reference in zip(counterexamples, counterexamples.str.len(), length_reference(counterexamples)):
    print(f'{value!r}: direct len={direct}; expected LENGTH={reference}')

# Ordinary spaces only: a tab is not removed by this fixture's rule.
assert length_reference(pd.Series(['ABC\t', '   ', ' ABC'])).tolist() == [4, 1, 4]
print('PASS: trailing ordinary spaces, all blanks, leading spaces and tab distinction.')
print('Scope: supplied ASCII fixture and stated counterexamples; SAS execution pending.')
