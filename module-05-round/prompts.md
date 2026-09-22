# Module 05: ROUND: keep the promise specific

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
- Build a DataFrame with value in the original row order:
  [2.3, 2.7, -1.4, -1.6, 3.0].
- Create rounded using the value Series .round(0) method.
- Print value and rounded. Numeric 2 and 2.0 are equivalent here.
- Include an assertion that rounded values are [2, 3, -1, -2, 3].
- Briefly explain what the check covers: these five inputs,
  nearest-integer rounding, including the negative inputs.
- State that halfway values and other rounding units have not
  been tested. Keep those cases outside this exercise.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Expected result

Row | value | rounded
--- | --- | ---
1 | 2.3 | 2
2 | 2.7 | 3
3 | -1.4 | -1
4 | -1.6 | -2
5 | 3.0 | 3

Compare numeric values. A display of 2.0 equals 2 here. Halfway cases and other rounding units are outside this 101 example.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
