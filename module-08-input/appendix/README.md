# Module 08: input reference appendix

These authored references support the two-page appendix. They do not replace the original prompts, fixtures or historical trial scores. `fixture` rows reproduce the original known-answer example. `edge` rows are added local validation cases.

## Files and shared fixture schema

- `reference.py`, `reference.R`, `reference.sas`: compute output from source columns; no hard-coded expected result columns.
- `test_reference.py`, `test_reference.R`, `test_reference.sas`: exactly three named acceptance checks invoking the reference transform.
- `fixtures.csv`: one shared input/expected-value source for all three languages.
- `appendix.json`: comparison snippets, teaching notes and the three test descriptions for PDF rendering.

`case_id,row_id,char_num,char_date,expected_num_value,expected_date_value`. Source columns are loaded as strings, including `0012`. Expected dates use ISO YYYY-MM-DD. `row_id` only identifies validation rows and is not part of the original fixture.

CSV quotes preserve source spaces in the file; Python/R loaders do not trim character values. These cases do not add a padded character-storage test. The reserved numeric missing sentinel is `__MISSING__`; pandas reads it as NaN, R as NA and the SAS LAG loader maps it explicitly to numeric missing. No numeric missing inputs are added to modules 08 or 09. Expected fields are comparison data, never inputs to the Python/R translations. The SAS loader keeps expected fields beside inputs solely for its assertions; transform does not read those fields.

## Run from any working directory

Use an absolute path to this directory. Python requires pandas; R uses only the standard R distribution and needs no external packages.

```bash
python /path/to/sas-training-modules/module-08-input/appendix/reference.py
python /path/to/sas-training-modules/module-08-input/appendix/test_reference.py
Rscript /path/to/sas-training-modules/module-08-input/appendix/reference.R
Rscript /path/to/sas-training-modules/module-08-input/appendix/test_reference.R
```

The reference CLIs print the original fixture results. Test files resolve adjacent source/CSV paths from their own location. Each Python test is a standard-library unittest method. Each R test uses base assertions and prints its PASS line only after all assertions succeed.

For the repository's optional WebR adapter (real R compiled to WebAssembly), see `tools/run_r_webr.cjs`; it uses `SAS_TRAINING_WEBR` to locate an installed WebR package. This is an execution alternative, not an R simulation.

## SAS execution instructions and status

**SAS is authored but unexecuted. No SAS runtime was available for this work.** Use a SAS session and set the path before including either script:

```sas
%let APPENDIX_DIR=/path/to/sas-training-modules/module-08-input/appendix;
%include "&APPENDIX_DIR/reference.sas"; /* computes and prints fixture */
%include "&APPENDIX_DIR/test_reference.sas"; /* three acceptance checks */
```

The harness loads the same CSV, calls `%transform(in=,out=)`, checks values/missing positions, compares source columns and order with PROC COMPARE, and checks representation/type requirements. It defines exactly three test macros: `test_T1_known_answer`, `test_T2_boundary`, `test_T3_contract`. Failures issue ERROR and abort; the dataset row count is checked before PASS. Running tests defines `APPENDIX_TEST_ONLY=1` to suppress the reference demo. If re-running the reference demo later in the same SAS session, first use `%symdel APPENDIX_TEST_ONLY / nowarn;`.

## Three tests

| ID | Name | Case |
| --- | --- | --- |
| T1 | Original known-answer fixture | Original fixture |
| T2 | Added valid leap-day / number case | Added edge validation |
| T3 | Preserve strings, order and types | Preservation/type/order contract |

`translate` retains source text and produces numeric plus pandas datetime / R Date values. English month parsing uses `LC_TIME=C` in Python and R, restoring the old time locale afterward. Locale setting is process-wide, so this reference is intended for standalone execution, not simultaneous threads changing locale. The SAS standalone reference sets `LOCALE=en_US`. Invalid-input policies and arbitrary SAS informats are outside this exercise.

## Execution evidence

Locally verified on 2026-09-23: Python 3.12.14 / pandas 2.2.3 and R 4.6.0 / WebR 0.6.0 each pass all three tests. This verifies these authored references, not the unavailable original model scripts. SAS checks remain unexecuted. The parent repository test runner records the consolidated run output.
