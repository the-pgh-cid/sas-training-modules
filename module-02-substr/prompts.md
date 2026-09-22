# Module 02: SUBSTR: specify the positions

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
- Build a DataFrame with text in the supplied row order.
- Right-pad text with spaces to width 20 before slicing.
- Use .str.slice(). Subtract 1 from the SAS start position.
  Python stop = adjusted start + requested length.
- Create first_three with slice(0, 3), middle with slice(4, 8),
  and from_seventh with slice(6, None).
- Preserve result widths 3, 4, 14; trim trailing spaces only
  in the printed view, not in the stored columns.
- Include assertions for the widths and these visible triples:
  ABCDEFGHIJ: ABC, EFGH, GHIJ
  HelloWorld: Hel, oWor, orld
  SAS-to-Python: SAS, to-P, -Python
- Print all columns and briefly explain the position adjustment.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Expected result

Row | first_three | middle | from_seventh
--- | --- | --- | ---
1 | ABC | EFGH | GHIJ
2 | Hel | oWor | orld
3 | SAS | to-P | -Python

The table hides trailing storage blanks for readability. Stored widths are 20 for text and 3, 4, 14 for the extracted columns.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
