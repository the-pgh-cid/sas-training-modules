# Module 07: COMPRESS

Attach the paired SAS file, or paste its contents after the prompt. Keep the same source and setup for A and B. Start a fresh conversation for each attempt.

## Prompt A: high degrees of freedom

```text
Convert this SAS code to Python.
Show code in this response. Do not create or run files, or read
existing Python files.
```

## Prompt B: low degrees of freedom

```text
Convert this SAS code to Python using pandas.
Show code in this response. Do not create or run files, or read
existing Python files.

- Recreate the three text values in their original order.
- These inputs contain ASCII characters only. Ignore SAS trailing
  storage padding when comparing values; preserve internal spaces.
- no_spaces: remove literal spaces with
  .str.replace(' ', '', regex=False).
- no_digits: remove 0-9 with .str.replace('[0-9]', '', regex=True).
- only_letters: ka keeps letters; use
  .str.replace('[^A-Za-z]', '', regex=True).
- Include assertions for these three complete result columns:
  no_spaces: ['ABC123XYZ', 'Phone:555-1234', 'ID-2023-Q4']
  no_digits: ['ABC  XYZ', 'Phone: -', 'ID--Q']
  only_letters: ['ABCXYZ', 'Phone', 'IDQ']
- Return one complete script. Compute results from text;
  do not hard-code the result columns.
Briefly explain the difference between removing and keeping.
```

## Expected result

Row | no_spaces | no_digits | only_letters
--- | --- | --- | ---
1 | "ABC123XYZ" | "ABC  XYZ" | "ABCXYZ"
2 | "Phone:555-1234" | "Phone: -" | "Phone"
3 | "ID-2023-Q4" | "ID--Q" | "IDQ"

Quotes mark string boundaries and are not data. Stored trailing padding is omitted. Preserve both internal spaces in the first no_digits result.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
