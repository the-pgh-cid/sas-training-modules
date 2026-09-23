# SAS / Python / R comparisons and acceptance tests

23 September 2026. Package v0.3.0 contains the original three-page v0.2.0 lesson plus a two-page appendix for each of the ten modules. Appendix pages are numbered A1/2 and A2/2; the original teaching pages and their trial evidence are preserved.

The first appendix page aligns the actual SAS, pandas and base-R core implementations. It explains the semantic details that the syntax alone can hide. The second page describes three named acceptance tests, each with its input, expected behavior and the mistake it is designed to catch.

## What the tests establish

| Test | Purpose | Evidence boundary |
| --- | --- | --- |
| T1 | Match all expected outputs for the original fixture | Tests a new reference implementation, not a historical model response |
| T2 | Exercise added, discriminating cases within the stated scope | Added validation rows never alter the historical A/B scores |
| T3 | Preserve the required inputs, order, widths, missing positions or types | Tests the behavioral contract alongside value equality |

Each test can contain several assertions. Three tests are a teaching structure, not a claim that three examples prove general equivalence. Explanations and explicit implementation requirements still need review: correct sample output alone does not establish full prompt compliance.

Expected values are held separately from the transformations. Each module's `appendix/fixtures.csv` is read by all three languages. `case_id` distinguishes original `fixture` rows from added `edge` rows; `expected_*` columns define the expected results. Quoted strings retain meaningful spaces. `__MISSING__` is reserved for numeric missing values and decoded by the loaders. Individual README files explain any module-specific representation choices.

The Python and R transformations receive the input columns, compute the results and return a new table. Test scripts call those same transformations. The SAS reference and harness share their transformation macro and CSV input. These small macros organize the executable harness; SAS macro conversion is not added to the 101 lesson.

## Companion files

Each `module-NN-name/appendix/` directory contains:

- `reference.sas`, `reference.py`, `reference.R`: complete runnable examples; PDF snippets omit loading and test boilerplate.
- `test_reference.sas`, `test_reference.py`, `test_reference.R`: three named acceptance checks in each language.
- `fixtures.csv`: common inputs and expected results.
- `appendix.json`: editable page content, excerpts, scope and primary reference links.
- `README.md`: exact commands, fixture details and limitations.

Python uses pandas and standard-library `unittest`. R uses base R only. The tests do not require pytest, testthat or any additional R package.

## Run Python and R

From the repository root, with Python, pandas and native R installed:

```bash
python tools/run_appendix_tests.py
python tools/run_appendix_tests.py --modules 1 5 10
```

Choose one language or save the complete output:

```bash
python tools/run_appendix_tests.py --language python
python tools/run_appendix_tests.py --language r
python tools/run_appendix_tests.py --report /tmp/appendix-tests.txt
```

The runner fails on an unsuccessful test or a missing three-test completion record. It does not silently count an unavailable R interpreter as a passing test. The individual reference and test scripts also run directly from any working directory; see their README commands.

### Optional WebR execution

This release's R checks were executed with actual R 4.6.0 through WebR 0.6.0 in Node, rather than native `Rscript`. The same base-R test files can be run with native R; that environment still needs its own execution record.

For a POSIX environment with Node and npm, install WebR separately from the repository:

```bash
npm install --prefix /tmp/sas-training-r-runtime webr@0.6.0
export SAS_TRAINING_WEBR=/tmp/sas-training-r-runtime/node_modules/webr
python tools/run_appendix_tests.py --webr
```

`tools/run_r_webr.cjs` mounts this repository into the R virtual filesystem and supplies the ordinary `commandArgs()` file argument when sourcing a script. It propagates R assertion failures as a nonzero process exit. This optional adapter does not change the portable R test code.

## SAS execution is pending

The SAS references and three-check harnesses are supplied for execution in a licensed SAS environment. They have been reviewed as source, but this release does not claim a SAS run or a three-language execution pass. Set `APPENDIX_DIR` to the module's appendix directory and submit the commands in that module's README. Record the SAS version, log and result before marking those checks executed.

## Scope remains specific

- ROUND covers the supplied nearest-integer, non-halfway inputs and additional non-halfway checks. R/pandas rounding does not establish general equivalence with SAS ROUND.
- Character examples use the stated ASCII and storage-width rules. Ordinary spaces, tabs, empty strings and missing sentinels are distinguished where applicable.
- INTCK uses ordinary discrete date intervals. INPUT checks the valid numeric/date patterns specified by its fixture.
- FIRST./LAST. retains the sorted, nonmissing single-key assumption and explicitly handles endpoints.
- LAG uses unconditional per-row calls. Conditional queue behavior remains a separate translation problem.

These are new reference implementations, not R versions of the historical Bedrock trials. No original prompt, SAS snippet, CSV result, trial log or source analysis is relabeled.

## Rebuild the PDFs

```bash
python -m pip install -r tools/requirements-pdf.txt
python tools/build_appendices.py
```

The builder retrieves the immutable three-page core PDFs from commit `1800819e7ecf1485dce3820046146824d5f735a5`, then appends exactly two pages. A source ZIP or shallow checkout without that commit can use a directory of original v0.2 PDFs:

```bash
python tools/build_appendices.py --source-dir /path/to/v0.2-pdfs --output-dir /tmp/expanded-pdfs
```

The source directory uses flat names such as `module-01-mean.pdf`. A five-page PDF is rejected as a baseline, preventing duplicate appendices. Earlier `build_module_NN.py` scripts reproduce the historical three-page cores; use `build_appendices.py` for the current five-page package.

The current delivery hashes are in `module-content/appendices-20260923.json`. The earlier `pdf-updates-20260922.json` remains the historical core manifest. Execution output and the integration review are in `validation/`.
