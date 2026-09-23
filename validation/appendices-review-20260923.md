# Appendix integration review

23 September 2026. Package v0.3.0, appendix v0.1.0.

All ten module PDFs now contain their original three teaching pages followed by a two-page appendix. Page A1 compares SAS, Python/pandas and base R. Page A2 describes three acceptance tests. Each module supplies runnable references, tests, shared CSV inputs and expected results, editable appendix content and execution instructions.

## Executed checks

| Check | Result |
| --- | --- |
| Python 3.12.14 / pandas 2.2.3 | 30 tests passed, three per module |
| Actual R 4.6.0 through WebR 0.6.0 | 30 tests passed, three per module |
| Negative controls on copied references | 20 of 20 suites rejected intentionally empty output through assertion failures |
| Original core pages | All 30 pages have identical extracted text and rendered pixels to the baseline |
| Clean appendix rebuild | All 50 pages have identical rendered pixels to the delivered PDFs |
| Visual review | All 20 appendix pages inspected for legibility, clipping, spacing and overlap |
| PDF structure | Ten five-page PDFs; every appendix character is within its page bounds |
| Displayed code and links | All 30 excerpts match the corresponding source; all 30 reference links are present |
| Historical source preservation | 109 existing files outside the ten PDFs and five documentation notices remain byte-identical |

The consolidated positive run is recorded in [appendix-tests-20260923.txt](appendix-tests-20260923.txt). It uses `tools/run_appendix_tests.py --webr`, with `SAS_TRAINING_WEBR` pointing to WebR 0.6.0. Each suite must both exit successfully and report three completed tests.

[appendix-negative-controls-20260923.json](appendix-negative-controls-20260923.json) records the separate negative run. In a temporary copy of each appendix, a wrapper called the original `translate` and returned zero rows while retaining columns and types. Every Python and R suite failed with a real assertion; none failed because of an import, path or runtime error. SHA-256 checks confirmed that all 50 delivered Python/R reference, test and fixture files remained unchanged. These controls establish that the suites exercise the transformation; they do not establish exhaustive mutation coverage.

## PDF and source preservation

The baseline is the three-page PDF for each module at commit `1800819e7ecf1485dce3820046146824d5f735a5`. Comparison used PyMuPDF rendering at 1.25 scale with RGB output and no alpha, plus exact extracted-text comparison for the original pages. A separate rebuild from the same baseline and appendix JSON reproduced all 50 rendered pages. Visual review used rendered appendix pages at 1.25 or 1.5 scale.

The original prompts, SAS examples, reported results, trial logs, analyses, module metadata and historical manifests were not edited. Original page numbering remains part of the original lesson; new pages use A1/2 and A2/2. The current PDF and appendix-file hashes are recorded in [appendices-20260923.json](../module-content/appendices-20260923.json).

## Execution limits

Thirty SAS acceptance checks are authored and source-reviewed but **not executed**. No licensed SAS runtime was available. Native `Rscript` execution and native R demonstration printing were also not executed; the R result above is specifically from actual R through WebR. The portable R scripts and native commands are supplied for that additional environment check.

The references preserve the stated teaching scope. They do not imply general equivalence for SAS ROUND halfway behavior, Unicode character-storage rules, arbitrary INPUT informats, multiple BY keys, NOTSORTED groups or conditional LAG queues. No new reference output is represented as a historical model trial, and no historical score was changed.
