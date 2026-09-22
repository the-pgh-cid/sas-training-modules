# Module 04 CAT/CATX: evidence review

22 September 2026. PDF teaching edition v0.2.0; SAS fixture and both prompts remain v0.1.0.

## Evidence available

- `results-20260921.csv`: six run records, reported CAT/CATX methods and correctness flags.
- `trial-log-20260921.md`: environment, prompt version, agent IDs, code excerpts and reported assertion results.
- `analysis-20260921.md`: the coordinator's interpretation and illustrative code.
- `prompts.md`, the paired `.sas` file and `module-content/modules-v0.1.0.json`: the unchanged teaching inputs and expected values.

The log identifies Claude Sonnet 4.5, AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0 and six fresh parallel agents. These are reported conditions. Complete agent `.output` transcripts and separate execution logs are absent from the inspected repository. Isolation, exact first-response content, extra actions and successful execution cannot be independently established from the summaries.

The PDF therefore labels the trial results and passing assertions **reported**. Local Python checks below validate the teaching reference and selected counterexamples; they do not replay the six original model responses. SAS execution remains pending.

## What the PDF says

| Runs | Reported behavior | Interpretation |
| --- | --- | --- |
| A1 | Raw `+` for CAT; join with spaces for CATX | Padding omitted; missing input periods appear as literal dots |
| A2 | Raw `+` for CAT; two CATX alternatives | Both unfiltered joining and period-filtered joining are described; required stored widths omitted |
| A3 | Raw `+` for CAT; filter periods and join for CATX | Readable CATX names match this fixture, but the full stored-value requirements do not |
| B1-B3 | Padded CAT; strip/filter/join CATX; assertions reportedly pass | Three reported full matches for the exercise; original execution not independently verified |

The displayed totals are A 0/3 and B 3/3 **full-requirement matches**, directly following the CSV's `Correctness` column. They are not estimates of future success rates. In particular, A3 is not described as producing entirely wrong CATX content: the readable names match, while storage widths and the complete conversion remain deficient.

## Interpretation corrections

The historical reports remain unchanged. This review records why the PDF uses narrower wording:

1. **Three response patterns are not three distinct CATX algorithms.** A2 describes the two recipes also seen in A1 and A3. The PDF shows this explicitly and does not repeat the reports' undefined "0% consistency" metric.
2. **Offering alternatives is observable; internal uncertainty is inferred.** A2 reportedly offers two approaches. That does not establish a hidden mental state, its rarity, or why it occurred.
3. **Prompt B specifies behavior, not exact APIs.** It names pandas, mapping, padding, CAT/CATX rules, widths, assertions and display requirements. It does not require `.replace()` or `.ljust()` by name. The PDF does not attribute those API requirements to the prompt.
4. **Equivalent behavior can use different Python methods.** Given the same padded inputs, `+`, `''.join(...)` and an f-string can produce identical CAT values. Method agreement alone is not evidence of correctness; method variation alone is not failure.
5. **B summaries are not proof of byte-identical responses or general correctness.** The log's illustrative B block omits period mapping, while the analysis shows it. Both show `.strip()` rather than `.strip(' ')`. Those excerpts cannot establish the full contents of all three responses. Python's no-argument `strip()` removes a broader whitespace class than the ordinary-space rule requested here. The supplied fixture does not distinguish them. The local reference uses `strip(' ')` and checks a tab counterexample. See [Python string stripping](https://docs.python.org/3/library/stdtypes.html#str.strip).
6. **Reported assertion passes do not establish how execution occurred.** Both prompts prohibit creating/running files during response generation. The repository lacks the raw response and execution history needed to resolve whether assertions were separately run or merely reported. The PDF neither certifies execution nor alleges a prompt violation.

## Local checks

Run from the repository root:

```bash
python validation/cat-reference-20260922.py
```

Results are recorded in `validation/cat-reference-20260922.txt`.

- Parsed the three simple DATALINES rows from the existing fixture and checked them against the expected inputs.
- Mapped missing input periods to blank fields; checked all three input widths of 8 and both output widths of 24.
- Checked every exact CAT string and padded CATX value, row order, input preservation and display without storage mutation.
- Reconstructed the recipes described in the A summaries. Filtering periods produces readable CATX names of length 13, 8 and 9; it does not produce stored width 24.
- Checked additional illustrative cases for ordinary outer spaces, all-blank fields, internal spaces, tabs and a literal dot. A dot already stored as text is not automatically missing; this fixture's missing-value mapping belongs to input interpretation.
- Confirmed that three different concatenation idioms agree on the same padded CAT inputs.

These checks cover ASCII character inputs of at most eight characters and outputs fitting width 24. They are not a general SAS parser or a claim of equivalence for numeric arguments, overflow, Unicode encodings or arbitrary SAS input formats. SAS's distinction between CAT preserving character blanks and CATX trimming and separating fields is also described in [SAS Usage Note 46672](https://support.sas.com/kb/46/672.html). The PDF retains its original SAS reference link.

## PDF verification

- Rebuilt from the original v0.1.0 PDF using `tools/build_module_04.py`; original source and prompt words preserved, with prompt line wrapping improved.
- Retained three 960 x 600 pages, the established typography/colors, original expected-value table and SAS reference link.
- Visually inspected all three rendered pages; checked page bounds, footer versions and prompt/source preservation.
- Rebuilding starts from the immutable Git baseline, avoiding accumulated overlays.

The dated trial log and analysis remain historical records. Their stronger claims, and the old pending-trials sentence in `prompts.md`, are superseded for the current PDF by this review and `PDF-BUILD.md`. The blank `trial-log.md` remains available for future runs.
