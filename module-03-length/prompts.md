# Module 03: LENGTH: say which spaces count

Attach the paired SAS file, or paste its contents after the prompt. Keep the same source and setup for A and B. Start a fresh conversation for each attempt.

## Prompt A: high degrees of freedom

```text
Convert this SAS code to Python.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Prompt B: low degrees of freedom

```text
Convert this SAS code to Python using pandas.
- Create text from ABC, ABC, ABCDEFGHIJ, X, and an empty string.
  The final SAS input period represents character missing here.
- Right-pad every text value with spaces to width 10.
- Preserve the stored text. For len, remove trailing ordinary
  spaces only with .str.rstrip(' '), then count characters.
- Match SAS LENGTH for a blank string: set its result to 1.
  Use .str.len().clip(lower=1) after the trailing-space removal.
- Print a visible representation of text and the len column.
- Include assertions: stored widths are all 10; len values are
  [3, 3, 10, 1, 1] in the original row order.
- Briefly explain why stored width and LENGTH can differ.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Expected result

Row | Stored width | len
--- | --- | ---
1 | 10 | 3
2 | 10 | 3
3 | 10 | 10
4 | 10 | 1
5 | 10 | 1

Both ABC rows are padded with seven blanks. The final row is ten blanks. SAS LENGTH returns 1 for this all-blank character value.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
