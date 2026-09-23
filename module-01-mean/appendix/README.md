# Module 01 MEAN: executable appendix

This companion contains hand-authored SAS, Python and R references plus exactly three acceptance tests per language. These files supplement the existing teaching module; they do not modify its fixture, prompts, reported scores or trial evidence. Added validation rows use `case_id="edge"` and are not model trials.

## Files and contract

- `reference.py` and `reference.R`: `translate(df)` returns a new table with derived outputs. The caller's table is unchanged. Python needs pandas; R uses base R only.
- `reference.sas`: equivalent `%translate(in=, out=)` macro, explicit CSV loader and fixture printout.
- `test_reference.py`, `test_reference.R`, `test_reference.sas`: T1 original fixture, T2 added boundary, T3 preservation/type/order. Every test calls the actual reference transformation.
- `fixtures.csv`: one shared, fully quoted UTF-8 CSV for all languages. Columns: `case_id`, `row_id`, `x`, `y`, `z`, `expected_average`.
- `appendix.json`: comparison snippets, teaching notes, test expectations and primary references for the PDF appendix.

`case_id` is either `fixture` or `edge`; `row_id` is stable within the shared table. All `expected_*` columns are test oracles, never inputs to the calculation. Quotes preserve leading/trailing spaces; do not open and resave the CSV with software that trims them. Tabs in the character edge cases are literal tab characters inside quoted fields. Numeric `__MISSING__` is decoded to NaN in Python, NA in R and ordinary `.` in SAS.

Character expected values include their exact storage padding. Python/R pad within `translate`; SAS acquires fixed-width storage during CSV loading. Consequently, the same logical inputs and expected stored outputs are compared. The SAS loader uses DSD and `$CHAR` informats. T3 checks stored preservation and declared widths in SAS, and also checks caller-object preservation and row/index order in Python/R.

Scope: Ordinary SAS numeric missing and finite numeric x/y/z values; no special missing codes, weights or grouping. Added edge rows are new validation examples, not new model trials.

## Run from any working directory

Replace `/absolute/path/to/repo` with your checkout path:

```bash
python /absolute/path/to/repo/module-01-mean/appendix/reference.py
python /absolute/path/to/repo/module-01-mean/appendix/test_reference.py
Rscript /absolute/path/to/repo/module-01-mean/appendix/reference.R
Rscript /absolute/path/to/repo/module-01-mean/appendix/test_reference.R
```

For SAS, submit the following two statements in an installed SAS session, with the absolute appendix path on that host:

```sas
%let APPENDIX_DIR=/absolute/path/to/repo/module-01-mean/appendix;
%include "&APPENDIX_DIR/test_reference.sas";
```

Use `reference.sas` instead to load and print only the original reference fixture. The tests include `reference.sas` and therefore print the fixture before running their three checks. The SAS harness aborts on a mismatch; a PASS line is written only after a check succeeds.

## Execution status

On 23 September 2026, all three Python tests passed with Python 3.12.14/pandas 2.2.3. All three R tests passed on real R 4.6.0 via WebR 0.6.0. WebR is a WebAssembly R runtime; this confirms R execution, not native Rscript installation. Native commands above remain the portable user workflow.

**SAS is authored but unexecuted in this environment.** Its three acceptance checks must be run in the target SAS installation; the presence of a harness is not evidence that SAS passed. The local Python/R checks are not Bedrock trial replays or evidence of model repeatability.

The PDF code panels are core excerpts from these companions. Module-specific loader/setup and any named helpers remain in the full reference files. Test expectations live in the shared CSV rather than in a second implementation of the calculation.
