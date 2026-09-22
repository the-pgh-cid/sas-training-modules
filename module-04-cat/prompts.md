# Module 04: CAT: preserve the intended spaces

Attach the paired SAS file, or paste its contents after the prompt. Keep the same source and setup for A and B. Start a fresh conversation for each attempt.

## Prompt A: high degrees of freedom

```text
Convert this SAS code to Python.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Prompt B: low degrees of freedom

```text
Convert this SAS CAT/CATX code to Python using pandas.
- Use first, middle, last in the original row order.
  Map the input periods to blank middle fields, not literal dots.
- Right-pad every input field to 8 characters with spaces.
- name1: concatenate the padded fields without trimming (CAT).
- name2: strip ordinary leading/trailing spaces from each field,
  skip blank fields, and join with one space (CATX).
- Store both result columns padded to width 24.
- Include assertions for both widths and all results below.
  For name1 checks, _ denotes one space:
  John____Q_______Public__
  Jane____________Doe_____
  Bob_____________Smith___
  name2, with trailing padding hidden:
  John Q Public; Jane Doe; Bob Smith.
- Print name1 with spaces visible and name2 in readable form.
  Keep stored values unchanged; explain the difference briefly.

Show code in this response. Do not create or run files, or read existing
Python files.
```

## Expected result

Row | CAT: name1 | CATX: name2
--- | --- | ---
1 | John____Q_______Public__ | John Q Public
2 | Jane____________Doe_____ | Jane Doe
3 | Bob_____________Smith___ | Bob Smith

Each underscore represents one stored blank in name1. name2 hides trailing storage padding. Input periods become blank middle fields. Both stored result columns have width 24.

Expected values checked in local Python reference implementations. SAS execution and revised Bedrock prompt trials are pending.
