# Module 01: MEAN: make missing values explicit

Attach the paired SAS file, or paste its contents after the prompt. Keep the same source and setup for A and B. Start a fresh conversation for each attempt.

## Prompt A: high degrees of freedom

```text
Convert this SAS code to Python.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Prompt B: low degrees of freedom

```text
Convert this SAS code to Python using pandas and NumPy.
- Create a DataFrame with columns x, y, z in the given row order.
- Represent SAS numeric missing values (.) with np.nan.
- Calculate average across x, y, z within each row using
  DataFrame.mean(axis=1, skipna=True).
- Keep an all-missing row missing; do not replace missing with zero.
- Print x, y, z, average, and briefly explain the missing-value rule.
- Include assertions: averages are 2.0, 5.0, and NaN, respectively.
  Check NaN with pandas.isna(), not equality.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Expected result

Row | average | Reason
--- | --- | ---
1 | 2.0 | Three observed values
2 | 5.0 | Missing value excluded
3 | . / NaN | All values missing

SAS prints numeric missing as a period. The Python exercise uses NaN. A missing value is not zero.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
