# Module 10: LAG

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

- Recreate id and value, preserving all five rows and their order.
- Each SAS LAG call executes on every row in this program.
- prev_value: use value.shift(1), with no frequency argument.
- prev2_value: use value.shift(2), with no frequency argument.
- change: subtract prev_value from value.
- Leave unavailable prior values and resulting changes missing.
  Do not fill them with zero, drop rows, sort, or wrap values.
- Include assertions for the original id sequence and these lists:
  prev_value: [missing, 10, 15, 12, 18]
  prev2_value: [missing, missing, 10, 15, 12]
  change: [missing, 5, -3, 6, 2]
  Use pd.isna to test missing positions.
- Return one complete script. Compute results from value;
  do not hard-code the result columns.
Briefly explain why the first change is missing.
```

## Expected result

id | value | prev_value | prev2_value | change
--- | --- | --- | --- | ---
1 | 10 | . | . | .
2 | 15 | 10 | . | 5
3 | 12 | 15 | 10 | -3
4 | 18 | 12 | 15 | 6
5 | 20 | 18 | 12 | 2

A period denotes SAS numeric missing; pandas may display NaN or <NA>. Compare missing positions as well as numbers. Conditional LAG calls require a separate analysis.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
