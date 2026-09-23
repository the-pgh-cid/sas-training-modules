# Module 07 COMPRESS appendix companions

These files accompany the two-page SAS/Python/R appendix. They are newly authored reference translations and tests, not recovered model responses or new Bedrock trials. The original teaching fixtures, prompts and trial scores remain unchanged.

## Run Python

Python 3 and pandas are required; tests use the standard-library `unittest` runner. Paths can be absolute, so these commands work from any directory after replacing `/absolute/path/to/repo`:

```bash
python /absolute/path/to/repo/module-07-compress/appendix/reference.py
python /absolute/path/to/repo/module-07-compress/appendix/test_reference.py
```

`translate(df)` returns a new DataFrame and derives every result from the input columns. `load_fixtures()` locates `fixtures.csv` beside the script. The CLI prints the original fixture rows only.

## Run R

Only base R is needed; no packages are installed by these scripts:

```bash
Rscript /absolute/path/to/repo/module-07-compress/appendix/reference.R
Rscript /absolute/path/to/repo/module-07-compress/appendix/test_reference.R
```

`translate(df)` returns the derived data frame. The scripts resolve their directory using the `--file` argument supplied by Rscript; working-directory changes are unnecessary. The tests source the same `reference.R` used by the demonstration. Each `PASS T1/T2/T3` line is printed only after that test's assertions complete.

## Run SAS: authored, unexecuted

SAS is unavailable in this authoring environment. Both SAS files are executable source for validation in a licensed SAS session, but no SAS pass is claimed. Set `APPENDIX_DIR` to the appendix directory on that machine, then submit:

```sas
%let APPENDIX_DIR=/absolute/path/to/repo/module-07-compress/appendix;
%include "&APPENDIX_DIR/reference.sas";
```

To run the three acceptance checks in that session:

```sas
%include "&APPENDIX_DIR/test_reference.sas";
```

The reference defines `%load_fixtures(out=)` and `%transform(in=, out=)`. The test harness includes that same reference, loads the same CSV, and calls the transformation for each check. Failures issue an error and abort the submitted program. The harness uses `APPENDIX_TESTING` to suppress the demonstration when included by tests. Unset that macro variable if you later want the reference demonstration to print again.

## Shared fixture contract

Columns: `case_id,row_id,text,expected_no_spaces,expected_no_digits,expected_only_letters`.

- `case_id="fixture"` marks the original teaching rows in their original order.
- `case_id="edge"` marks added validation rows. These are not added to historical A/B scores.
- `row_id` is a row identifier within each group; together with `case_id` it identifies a row.
- `expected_*` columns are the shared language-neutral oracle. The translations receive input columns and compute outputs; tests compare against these independent expected columns.
- CSV fields are quoted so string spaces survive parsing. Reserved numeric-missing sentinel: `__MISSING__`. These three modules' selected numeric fixtures contain no missing values; that token does not broaden their scope.

All string fields are quoted. Do not strip their leading or internal spaces. Empty strings and three literal spaces are separate CSV inputs. Python and R preserve those literal strings. SAS uses width-20 character fields and blank-padded character comparison, consistent with omitting trailing storage padding. This is ASCII content validation, not a Unicode or universal COMPRESS implementation.

## Exactly three named tests

| ID | Python/R/SAS test name | Purpose |
| --- | --- | --- |
| T1 | `test_T1_original_fixture_known_answers` | Every expected output for the original fixture |
| T2 | `test_T2_added_in_scope_boundaries` | Added discriminating boundary rows |
| T3 | `test_T3_preservation_types_and_order` | Reversed row order, unchanged inputs, appropriate types and complete expected outputs |

Each test invokes the reference transformation. T3 also uses custom Python/R row identifiers; the SAS harness retains an explicit ordering column. A correct-looking printout alone does not satisfy the contract checks.

## Execution record

Python: all three tests passed during authoring (Python 3.12.14, pandas 2.2.3). R: all three tests passed under R 4.6.0 via WebR 0.6.0 (Node/WASM); the portable commands above remain the native Rscript interface. This verifies the R code in that runtime, not a separate native R installation. SAS: unexecuted. These tests validate only the stated examples and contract, not general SAS equivalence or production readiness.

Primary technical references are listed in `appendix.json` and linked on the comparison page. Its snippets are exact contiguous core excerpts from the companion reference files; loading, helpers and CLI boilerplate are omitted from the page and described in the language notes.
