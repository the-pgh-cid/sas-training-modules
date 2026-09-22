# Module 09: FIRST. / LAST.

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

- Recreate id, group, and value. Keep all six rows in their order.
- These rows are already sorted by group, with no missing groups.
- Add first_flag and last_flag as integer 0/1 columns.
- first_flag is 1 on the first row or when group differs from
  the previous row. Compare with group.shift(1).
- last_flag is 1 on the last row or when group differs from
  the next row. Compare with group.shift(-1).
- Handle the first and last rows explicitly. Do not filter rows
  or reorder records within groups.
- Include assertions for id = [1, 2, 3, 4, 5, 6],
  first_flag = [1, 0, 1, 0, 0, 1], and
  last_flag = [0, 1, 0, 0, 1, 1].
- Return one complete script. Compute the flags from group;
  do not hard-code them. Explain why row 6 has both flags.
```

## Expected result

id | group | value | first_flag | last_flag
--- | --- | --- | --- | ---
1 | A | 10 | 1 | 0
2 | A | 20 | 0 | 1
3 | B | 30 | 1 | 0
4 | B | 40 | 0 | 0
5 | B | 50 | 0 | 1
6 | C | 60 | 1 | 1

Scope: one nonmissing grouping variable and the supplied sorted rows. Both flags are 1 for a one-row group. All six rows remain in the output.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
