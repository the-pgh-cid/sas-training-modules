# Module 08 INPUT: evidence review

22 September 2026. PDF teaching edition v0.2.0; both prompts and the SAS fixture remain v0.1.0.

## Evidence available

- `results-20260921.csv`: six run records with reported conversion methods, correctness and assertion presence.
- `trial-log-20260921.md`: reported setup, selected conversion expressions, expected values and reported value/type assertion results.
- `analysis-20260921.md`: the coordinator's interpretation and wider claims.
- `prompts.md`, `example-08-input-sas-snippet.sas` and `module-content/modules-v0.1.0.json`: unchanged teaching inputs and expected results.

The log describes Claude Sonnet 4.5 on AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0 and six fresh parallel agents. Complete `.output` transcripts and separate execution logs are absent from the inspected repository. The PDF therefore identifies the conditions, trial scores and passing assertions as reported. This update checks a local reference implementation; it does not certify or replay the historical responses. SAS execution remains pending.

## Findings carried into the PDF

| Runs | Reported method | Reported result | Reported assertions |
| --- | --- | --- | --- |
| A1-A3 | `pd.to_numeric` and `pd.to_datetime` with `%d%b%Y` | Expected values match in all three runs | None |
| B1-B3 | Same conversion methods | Expected values match in all three runs | Value and numeric/datetime type assertions reportedly pass |

The PDF displays A 3/3 and B 3/3 expected-value matches. The distinction between the prompts is the explicit contract and the requested checks, rather than an observed increase in this small sample's value-match count.

The original three-page teaching structure is retained. Page 1 preserves the full SAS fixture and expected table, including `char_date $9` and the distinction between calendar dates, SAS numeric storage and display. Page 2 adds A-run evidence without pretending that agreement guarantees future results. Page 3 preserves Prompt B and explains the source/result, date-format, value and type requirements.

## Interpretation corrections

The historical log, CSV and analysis are preserved. The current PDF uses narrower conclusions:

1. **Shared methods do not establish identical complete scripts.** Two summarized conversion expressions and method labels cannot prove that all imports, constructors, explanation text, assertions or other behavior were identical. The A/B groups explicitly differ in reported assertions. The PDF avoids the blanket phrase "zero variance."
2. **Training priors are not observed.** Six successful summaries do not establish why the model selected those APIs. The analysis's explanations involving universally known or uniquely obvious methods are hypotheses, not demonstrated findings.
3. **The supplied valid inputs define the scope.** These three clean values do not establish general SAS INPUT equivalence, behavior on malformed or missing values, compatibility with every informat, timezone handling or locale independence. The analysis's recommendation that Prompt A is generally sufficient is not warranted by this sample.
4. **A representation check adds information.** A string such as `2023-01-15` can look right while failing the requested datetime type. The local counterexample demonstrates this directly. A formatting operation used only for comparison leaves the stored datetime column intact.
5. **Date parsing has an environment assumption.** `%b` denotes the locale's abbreviated month name in [Python's datetime format documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). Prompt B says the supplied abbreviations are English. The reference explicitly uses the C time locale for these English inputs; this is not a claim that all locales or date formats behave identically.
6. **Error policy remains a separate choice outside the fixture.** pandas defaults raise on invalid numeric/date parsing, while `errors='coerce'` produces missing values. See [pandas.to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html) and [pandas.to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html). The extra local examples illustrate why successful valid-input checks do not settle malformed-input behavior; they do not change the exercise or trial scores.
7. **Reported assertion passes do not establish execution provenance.** Both prompts prohibit running or creating files during response generation. Missing transcripts and execution logs prevent a determination of whether checking was performed separately or only reported. This review neither certifies execution nor alleges a prompt violation.

## Local validation

Run `python validation/input-reference-20260922.py`; captured output is in `validation/input-reference-20260922.txt`.

- Parsed the original three DATALINES rows and retained both source string columns and row order.
- Computed the requested numeric and datetime result columns and checked all values against the baseline expected table.
- Checked the numeric and datetime dtypes and cross-checked calendar results against independently constructed year/month/day values.
- Demonstrated that numeric-looking and date-looking strings can match displays while failing the requested types.
- Confirmed formatting for comparison does not replace stored datetime values.
- Tested malformed `12x` and impossible `31FEB2023` outside the original fixture: default parsing rejects each, while explicit coercion gives missing values.

The output records Python 3.12.14, pandas 2.2.3 and `LC_TIME=C`. No SAS or Bedrock calls were made, and no absent historical model script was represented as executed.

## PDF verification

- Rebuilt with `tools/build_module_08.py` from the immutable original PDF using `pdf_build_support.py` and the explicit baseline source path.
- Retained three 960 x 600 pages, the existing colors and typography, complete source and prompt text, expected table and reference links.
- Rendered and visually inspected all three final pages; corrected the evidence-note position so both original reference links remain unobstructed.
- Full SAS source and both prompts remain extractable; prompt reflow changes whitespace only.

The old pending-trials sentence in `prompts.md` remains historical packet text. This review and the current PDF supersede that status. The blank `trial-log.md` remains available for future runs.
