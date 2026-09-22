# Module 06: INTCK

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

- Recreate the six rows in order; keep the same column names.
- Parse dates with pd.to_datetime(..., format='%d%b%Y').
  The inputs are valid dates with English month names.
- Preserve default discrete INTCK behavior: count boundaries.
- days: subtract start_date from end_date and use .dt.days.
- months: 12 * (end year - start year) + end month - start month.
- years: end year - start year.
- Return one complete script and include assertions for:
  days = [14, 31, 364, 5, 1, 1]
  months = [0, 1, 11, 0, 1, 1]
  years = [0, 0, 0, 0, 0, 1]
- Calculate from the input dates; do not hard-code result columns.
Briefly explain why a one-day interval can cross a month or year.
```

## Expected result

start_date | end_date | days | months | years
--- | --- | --- | --- | ---
01JAN2023 | 15JAN2023 | 14 | 0 | 0
01JAN2023 | 01FEB2023 | 31 | 1 | 0
01JAN2023 | 31DEC2023 | 364 | 11 | 0
15MAR2023 | 20MAR2023 | 5 | 0 | 0
31JAN2023 | 01FEB2023 | 1 | 1 | 0
31DEC2023 | 01JAN2024 | 1 | 1 | 1

The last two rows distinguish calendar boundaries from elapsed months or years. Compare every result column.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
