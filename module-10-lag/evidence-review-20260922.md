# Module 10 evidence review: LAG

Review date: 2026-09-22. Teaching PDF version: v0.2.0.

## Sources and limits

Reviewed `prompts.md`, `example-10-lag-sas-snippet.sas`, `results-20260921.csv`, `trial-log-20260921.md`, the blank `trial-log.md`, the immutable v0.1.0 module-content record and all three original PDF pages. This module has no separate `analysis-20260921.md`; analysis appears inside the dated trial log. The full SAS fixture, expected table and both prompts are preserved.

The source reports six fresh parallel agents on 2026-09-21 using Claude Sonnet 4.5 through AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0. These are reported metadata. The CSV and trial log name original `.output` files, but complete transcripts and command-level execution logs are absent from the repository. The new PDF therefore labels results and assertion passes as **reported**. Original historical CSV and log remain unchanged; `trial-log.md` remains a blank future-run template.

## What the records support

| Run | Reported method | Reported expected output | Assertions reported |
| --- | --- | --- | --- |
| A1 | `shift(1)` and `shift(2)` | Match | Absent |
| A2 | `shift(1)` and `shift(2)` | Match | Absent |
| A3 | `shift(1)` and `shift(2)` | Match | Absent |
| B1 | `shift(1)` and `shift(2)` | Match | Passed |
| B2 | `shift(1)` and `shift(2)` | Match | Passed |
| B3 | `shift(1)` and `shift(2)` | Match | Passed |

All six rows share the recorded method. The trial log shows a common three-line implementation for lagged values and subtraction. This supports agreement at the recorded-method level; it does not establish identical complete responses, zero variance, hidden training priors or guaranteed future agreement. B reports add assertions and an explanation of why the first change is missing. Without full response/execution artifacts, complete instruction compliance and actual assertion execution are not independently verified.

The teaching comparison preserves successful A outcomes. A more explicit B prompt makes the acceptance conditions visible even when both prompt variants already have reported output matches.

## Local reference and scope checks

Executed `validation/lag-reference-20260922.py`; stored output in `validation/lag-reference-20260922.txt` with Python 3.12.14 and pandas 2.2.3.

- The full five-row expected table, original ids, both lag lists, every missing position and changes match for ordinary integer and nullable integer dtypes.
- Separate independently maintained queues of lengths one and two match `shift(1)` and `shift(2)` because each SAS function occurrence executes once on every input row in this program.
- Filling the first missing prior value with zero creates a first change of 10, instead of missing.
- Wrapping the final value to the beginning creates a first prior value of 20, instead of missing.
- Sorting by value changes the calculation for id 3 from -3 to 2.
- A separate conditional-call counterexample executes a LAG occurrence only on rows 2 and 4. Its queue returns `[missing, missing, missing, 15, missing]`. Unconditionally shifting all rows and then masking produces `[missing, 10, missing, 12, missing]`. Thus conditional call history needs separate translation analysis. The counterexample models an ordinary non-retained assignment target and is not a SAS execution.

These checks are authored references, not fresh Bedrock trials or execution of the unavailable original full responses. SAS execution remains pending.

[SAS LAG documentation](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0l66p5oqex1f2n1quuopdvtcjqb.htm) specifies a separate initialized queue per function occurrence and advancement only when that occurrence executes. [pandas Series.shift](https://pandas.pydata.org/docs/reference/api/pandas.Series.shift.html) describes shifts, missing starting positions and frequency behavior. These support the restricted interpretation used here.

## Artifact decisions and QA

`tools/build_module_10.py` rebuilds from the immutable original PDF using `pdf_build_support.py`. It retains the three-page structure, source, expected values, full prompts and reference links. Added content shows reported setup, all A and B outcomes, missing-value/order anti-patterns, assertion-report status and the per-row limitation of LAG-to-shift equivalence. All three final pages were rendered and visually inspected for alignment, readable text and overlap.

Remaining limits: complete trial responses and execution logs are unavailable; SAS execution is pending; three reported runs per prompt do not establish future repeatability.
