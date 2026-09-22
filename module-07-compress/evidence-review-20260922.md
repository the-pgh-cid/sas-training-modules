# Module 07 COMPRESS: evidence review

22 September 2026. PDF teaching edition v0.2.0; both prompts and the SAS fixture remain v0.1.0.

## Evidence available

- `results-20260921.csv`: six reported runs, correctness flags, character-class interpretations and regex patterns.
- `trial-log-20260921.md`: reported setup, agent IDs, selected expressions, output comparisons and assertion results.
- `analysis-20260921.md`: the coordinator's interpretation and illustrative examples.
- `prompts.md`, `example-07-compress-sas-snippet.sas` and `module-content/modules-v0.1.0.json`: unchanged teaching inputs and expected values.

The dated log describes Claude Sonnet 4.5 on AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0 and six fresh parallel agents. Complete `.output` transcripts and separate execution logs are absent from the inspected repository. These conditions, the response contents and successful assertion execution are therefore reported, rather than independently verified here. The PDF labels them accordingly. SAS execution remains pending.

## Findings carried into the PDF

| Runs | Reported `only_letters` pattern | Reported expected values | Teaching point |
| --- | --- | --- | --- |
| A1 | `[^A-Za-z0-9]` | No | Including digits in the allowed set changes the result in all three rows |
| A2-A3 | `[^a-zA-Z]` | Yes | The supplied ASCII letter class has the intended meaning |
| B1-B3 | `[^A-Za-z]` | Yes; assertions reported passed | Explicit character rules and complete expected columns make the requirements checkable |

The PDF displays A 2/3 and B 3/3 expected-value matches, as recorded in the CSV. For the illustrative input `Phone: 555-1234`, applying A1's reported expression produces `Phone5551234`; the expected result is `Phone`. The local reconstruction validates that expression's behavior, not the absent original response.

The original three-page structure remains: source/setup/expected values; full Prompt A with observed results and anti-pattern; full Prompt B with rationale, reported results and a concrete independent check. The expected table, ASCII scope, trailing-storage-padding exception, internal-space requirement and full prompts are retained.

## Interpretation corrections

The historical reports are preserved. The PDF does not carry forward their stronger or incorrect claims:

1. **No inference about training priors or internal reasoning.** The pattern keeps digits. Its output is observable; the model's internal cause is not established by three summarized A runs.
2. **No guarantee from B's three reported successes.** Agreement in these selected methods and values does not prove identical full responses, zero possible variance or general correctness on future inputs.
3. **SAS character lists are not regex ranges.** The historical example `compress(text, '0-9')` is not the fixture's all-digits removal. Its literal character list contains `0`, `-` and `9`. The actual fixture correctly uses `0123456789`.
4. **Keep operates on the selected list.** The historical comment describing `compress(text, '', 'k')` as keeping first-argument characters is misleading. Selection comes from the second argument plus modifier classes. Likewise, `n` includes English letters and underscore as well as digits, so `kn` does not mean keep numerals only. The PDF confines itself to the verified `ka` rule. See the [SAS COMPRESS function reference](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/n0fcshr0ir3h73n1b845c4aq58hz.htm).
5. **Python string replacement and pandas regex replacement differ.** Some historical illustrative examples call `text.replace('[0-9]', '')` as though ordinary Python string replacement understands regex. The current reference uses pandas `.str.replace(..., regex=True)` for character classes and `regex=False` for literal spaces, consistent with the [pandas string replacement reference](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html).
6. **Reported passes do not establish execution provenance.** Both prompts prohibit file creation/execution during generation. Absent transcripts and execution logs, this review cannot determine whether checking occurred separately or whether the assertion result was only reported. It does not allege a prompt violation or certify a run.

## Local validation

Run `python validation/compress-reference-20260922.py`; the captured output is `validation/compress-reference-20260922.txt`.

- Parsed the existing three DATALINES strings without splitting internal spaces.
- Computed all nine expected results with the requested pandas replacements and cross-checked them against a separate character-set filter.
- Checked source/row preservation, the exact two internal spaces in `ABC  XYZ`, punctuation retention and the fixture's content comparison after width-20 storage padding is omitted.
- Reconstructed A1's summarized expression and confirmed that all three letters-only results fail; confirmed the A2/A3 and B letter-class spellings agree on this fixture.
- Added local illustrative cases for empty strings, digit-only strings, mixed case, punctuation and a tab. Literal-space removal retains the tab; a broader whitespace-removal rule would change the result.

These local checks neither replay the six historical responses nor execute SAS or Bedrock. They cover the supplied ASCII content contract, not general SAS modifier, encoding or storage equivalence. Extra cases are not added to the historical trial scores.

## PDF verification

- Rebuilt with `tools/build_module_07.py` from the immutable original PDF using `pdf_build_support.py` and the explicit baseline source path.
- Retained three 960 x 600 pages and the original teaching design and reference links.
- Rendered and visually inspected all three final pages, including the corrected placement of the evidence note beside the reference links.
- Full SAS source and both prompts remain extractable; prompt reflow changes whitespace only.

The old pending-trials sentence in `prompts.md` is retained as historical packet text. This review and the current PDF supersede that status. The blank `trial-log.md` remains available for future runs.
