# Module 09 evidence review: FIRST. / LAST.

Review date: 2026-09-22. Teaching PDF version: v0.2.0.

## Sources and limits

Reviewed `prompts.md`, `example-09-firstvar-sas-snippet.sas`, `results-20260921.csv`, `trial-log-20260921.md`, `analysis-20260921.md`, the blank `trial-log.md`, the immutable v0.1.0 module-content record, and all three original PDF pages. The SAS fixture, expected table and both full prompts are preserved; only whitespace in the displayed SAS source was compacted to make room for test metadata.

The supplied trial records describe six fresh parallel agents on 2026-09-21, Claude Sonnet 4.5 through AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0. Model/deployment details are reported metadata, not independently authenticated observations.

The repository provides coordinator summaries, a results CSV and selected code excerpts. It does not contain the six named complete `.output` transcripts or command-level execution logs. Consequently, the PDF says **reported** outputs and assertions. The original trial CSV/log/analysis are retained unchanged as historical evidence. Blank `trial-log.md` remains a template for future runs.

## Output correctness and instruction compliance are separate

| Run | Reported method | Reported expected flags | Assertions reported | Explicit endpoints in shown excerpt |
| --- | --- | --- | --- | --- |
| A1 | `groupby().cumcount()` | Match | Absent | Not an A requirement |
| A2 | `groupby().cumcount()` | Match | Absent | Not an A requirement |
| A3 | `groupby().cumcount()` | Match | Absent | Not an A requirement |
| B1 | Adjacent comparisons with endpoint checks | Match | Passed | Yes |
| B2 | Adjacent comparisons relying on missing-value behavior | Match | Passed | No |
| B3 | Adjacent comparisons relying on missing-value behavior | Match | Passed | No |

Prompt B explicitly requests handling of the first and last rows. The B2/B3 excerpts contain only comparisons against shifted groups and an integer conversion. They omit that requirement even though the reports mark their fixture outputs correct. Page 3 therefore displays 3/3 reported output matches separately from the endpoint-compliance column. B1 is the only shown B excerpt with explicit endpoint handling. This is a review of those excerpts, not a claim that every other requirement of every unseen full response was verified.

The historical analysis calls this purely a stylistic choice and the trial log describes B2/B3 as cleaner. Those judgments are not carried forward. Method variation between `cumcount()` and neighbor comparisons is valid for the supplied sorted fixture, but a specified endpoint rule remains part of the acceptance contract.

## Local reference and meaningful counterexample

Executed `validation/firstvar-reference-20260922.py`; recorded output in `validation/firstvar-reference-20260922.txt` with Python 3.12.14 and pandas 2.2.3.

- The complete six-row table, original id order, integer flag columns and singleton group C pass with both `object` and pandas nullable `string` group dtypes when endpoints are assigned explicitly by position.
- Independent forward/reverse group-position counts agree with both flag lists for the sorted, nonmissing fixture.
- Reconstructed B2/B3 expressions match the supplied values with `object` strings. These expressions are excerpts, not recovered full original response scripts.
- With nullable `string`, first/last shifted comparisons produce `<NA>` at the respective endpoints. The reported unguarded `.astype(int)` pattern raises `ValueError: cannot convert NA to integer`. Explicit positional endpoint assignments pass. The fixture itself has no missing groups; the missing comparison values are introduced by `shift`.
- Positional endpoint assignments also pass with non-default index labels. B1's shown `index == 0` / `index == len(df)-1` checks suit the recreated default index but should not be taught as a general positional test.
- Filtering down to first/last boundary records drops id 4, demonstrating why flags must be added without filtering.

The reference is deliberately authored verification, not a fresh model trial, transcript replay, or SAS execution. Scope remains one nonmissing group key and the supplied sorted rows; multi-key and `NOTSORTED` behavior are not generalized.

[pandas missing-data documentation](https://pandas.pydata.org/docs/user_guide/missing_data.html) explains dtype-dependent missing sentinels and propagation through nullable comparisons. [pandas Series.shift](https://pandas.pydata.org/docs/reference/api/pandas.Series.shift.html) documents the introduction of missing entries by shifts. [SAS BY-group documentation](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a000761931.htm) explains first/last automatic variables and singleton groups. These support the technical interpretation; they do not authenticate the reported trials.

## Teaching and artifact decisions

Keep the successful A results. Prompt detail adds a checkable contract; it does not guarantee convergence or establish zero full-response variation. Preserve the prompt's explicit-endpoint requirement and teach learners to check compliance as well as sample outputs.

`tools/build_module_09.py` rebuilds from the immutable original PDF through `pdf_build_support.py`. The three-page teaching structure, fixture, expected values, prompt wording and existing source links remain. New content provides reported setup, A/B results, endpoint review, a filtering anti-pattern and local-reference limits. All three final pages were rendered and visually inspected for alignment, readable text and overlap.

Remaining limits: original full trial responses and execution logs are unavailable; SAS execution is pending; three reported runs per prompt do not establish future repeatability.
