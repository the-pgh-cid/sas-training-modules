# Module 06 INTCK: evidence review, 22 September 2026

The teaching PDF now includes the reported 21 September A/B results while preserving the six original rows, both prompts and the three-page teaching structure. The scope remains default discrete day, month and year boundaries on date-only inputs.

## Evidence used

- `results-20260921.csv`: six run records, methods, correctness, assertion inclusion and explanation fields.
- `trial-log-20260921.md`: reported setup, per-run code excerpts and result notes.
- `analysis-20260921.md`: reviewed against the individual records; unsupported conclusions are not adopted.
- `prompts.md`, `example-06-intck-sas-snippet.sas`, `trial-log.md` and `module-content/modules-v0.1.0.json`: original exercise, reference expectations and run-recording instructions.

The setup is reported as Claude Sonnet 4.5 on AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0, six fresh parallel agents. Full named `.output` transcripts and separate execution logs are absent from this repository. The PDF labels results and assertion outcomes as reported. This update did not run SAS or issue new Bedrock trials.

## Adopted findings

| Runs | Reported method | Supplied values | Assertions | Boundary explanation |
| --- | --- | --- | --- | --- |
| A1 | Functions with row-wise `.apply()` | All three columns match | Not included | Included |
| A2-A3 | Vectorized inline | All three columns match | Not included | Included |
| B1-B3 | Vectorized inline | All three columns match | Included; pass reported | Included |

Reported expectations are:

- `days = [14, 31, 364, 5, 1, 1]`
- `months = [0, 1, 11, 0, 1, 1]`
- `years = [0, 0, 0, 0, 0, 1]`

The final two rows distinguish calendar boundaries from elapsed periods. January 31 to February 1 crosses a month; December 31 to January 1 crosses a month and a year. The observed method differences did not change fixture results. This is not a promise of future model consistency.

## Corrections and excluded claims

- No inference is made about model training data, prior knowledge, or why the model selected each method.
- The analysis's 50x runtime comparison lacks benchmark code, machine details and measured execution output. Its small-data times also confuse agent duration fields with Python runtime. None of those performance numbers appears in the revised PDF.
- Agreement on six rows does not prove that the methods have no edge cases or that every SAS interval is equivalent to these formulas.
- Similar reported method and assertion structure does not establish byte-identical complete responses. The revised PDF does not claim zero variance or guaranteed convergence.
- Continuous, shifted, multiplied, custom, week and datetime intervals remain outside scope. No proposed extension is silently added to the original exercise.
- Business examples do not establish that every billing or contract rule requires discrete boundary counts. The revised teaching text stays with the explicitly requested SAS behavior.

## Primary technical reference checked

The documented default INTCK method is discrete and counts interval boundaries. The SAS reference explicitly distinguishes one-day month-boundary cases from completed intervals. [SAS INTCK function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p1md4mx2crzfaqn14va8kt7qvfhr.htm). The original SAS and pandas parsing reference links remain in the PDF.

## Local validation and visual review

`python validation/intck-reference-20260922.py` writes `validation/intck-reference-20260922.txt`.

- Parsed the six pairs directly from the unchanged SAS fixture and checked every calculated value, with original date values and row order retained.
- Independently enumerated each calendar transition between dates and compared all 18 counts with the vectorized formulas.
- Reconstructed the functions/`.apply()` approach described in A1 and confirmed agreement on the fixture. This reconstruction is not a replay of a complete model transcript.
- The counterexample `elapsed days // 30` yields `[0, 1, 12, 0, 0, 0]`, failing the required month count on rows 3, 5 and 6. This makes the anti-pattern concrete without changing the fixture.
- Rendered and visually inspected all three revised pages. Confirmed all original SAS and prompt words remain extractable after whitespace normalization.
- Rebuild uses `tools/build_module_06.py` and the immutable baseline supplied by `tools/pdf_build_support.py`; no overlays are stacked on a previous edition.

SAS execution remains pending. Reported assertion passes remain separate from the local reference validation. No performance measurement was made.
