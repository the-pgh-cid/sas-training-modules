# Module 05 ROUND: evidence review, 22 September 2026

The teaching PDF now includes the reported 21 September A/B results while preserving all five original input values, both prompts and the three-page teaching structure. The exercise remains limited to the supplied non-halfway values and nearest-integer rounding.

## Evidence used

- `results-20260921.csv`: six run records and the separate `Correctness` and `Understanding_Correct` fields.
- `trial-log-20260921.md`: reported setup, per-run excerpts and explanation notes.
- `analysis-20260921.md`: reviewed against the individual records; its unsupported conclusions are not adopted.
- `prompts.md`, `example-05-round-sas-snippet.sas`, `trial-log.md` and `module-content/modules-v0.1.0.json`: original exercise, reference expectations and run-recording instructions.

The setup is reported as Claude Sonnet 4.5 on AWS Bedrock GovCloud, Claude Code 2.1.278, `effortLevel=high`, prompt v0.1.0, six fresh parallel agents. Full named `.output` transcripts and separate execution logs are absent from this repository. The PDF therefore labels results and assertion outcomes as reported. This update did not run SAS or issue new Bedrock trials.

## Adopted findings

| Runs | Reported method | Supplied numeric values | Explanation or scope |
| --- | --- | --- | --- |
| A1 | `.round()` | Match | Incorrectly says SAS and pandas both use half-to-even |
| A2 | `.round()` | Match | Correct tie-direction distinction; offers floor/ceil alternative |
| A3 | `.round()` | Match | Correct tie-direction distinction; notes no halfway inputs |
| B1-B3 | `.round(0)` | Match; assertions reported passed | Explicitly exclude halfway values and other rounding units |

All six reported outputs agree with `[2, 3, -1, -2, 3]` for the five fixture values. Three consistent outputs do not establish future model repeatability or general translation equivalence.

## Corrections and excluded claims

- The analysis summary says only 1/3 A explanations are correct. The CSV marks A2 and A3 `YES`, and their quoted explanations support **2/3**. A3's lack of an alternative implementation does not make its explanation wrong.
- A2's simple sign-aware floor/ceil recipe is not certified as generally SAS-exact or production-ready. SAS ROUND includes near-halfway handling and floating-point adjustments beyond the tested exact-tie examples.
- Correct output does not establish that the accompanying explanation is correct. A1 is the concrete example; its incorrect general claim is not adopted.
- Speculation about training priors, model knowledge, guaranteed convergence, or production readiness is excluded. Claims that B has zero risk or always prevents misinformation are also excluded.
- The source analysis's illustrative sum for half-away-from-zero is arithmetically wrong: rounding `[0.5, 1.5, 2.5, 3.5, 4.5]` away from zero gives a sum of 15, not 14. That appendix and its unsupported historical explanation are not used.
- The original five inputs and prompt scope were retained. Halfway counterexamples exist only in the separate local review script, clearly labeled outside the exercise.

## Primary technical references checked

At exact ties, SAS ROUND chooses the greater magnitude; its documentation also describes approximate ties and fuzzing. This supports rejecting A1's explanation and withholding a general equivalence claim for A2. [SAS ROUND function](https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p0tj6cmga7p8qln1ejh6ebevm0c9.htm).

pandas Series rounding uses the nearest even value for halfway cases. [pandas Series.round](https://pandas.pydata.org/docs/reference/api/pandas.Series.round.html). Both references are linked from the teaching PDF.

## Local validation and visual review

`python validation/round-reference-20260922.py` writes `validation/round-reference-20260922.txt`.

- Parsed the five inputs directly from the unchanged SAS fixture; checked `.round()` and `.round(0)` against all expected values, with original input values and row order retained.
- Independently checked simple unit-1 rounding with decimal arithmetic.
- Verified the source explanation count is 2/3.
- Separate exact-tie probes show pandas results `[2, -2, 4, -4]` versus a decimal model of SAS's documented tie direction `[3, -3, 4, -4]` for `[2.5, -2.5, 3.5, -3.5]`. This is a local counterexample, not SAS execution.
- A2's alternative passes those exact ties. This narrow check does not establish general SAS equivalence.
- Rendered and visually inspected all three revised pages. Confirmed all original SAS and prompt words remain extractable after whitespace normalization, with improved response-policy line wrapping.
- Rebuild uses `tools/build_module_05.py` and the immutable baseline supplied by `tools/pdf_build_support.py`; no overlays are stacked on a previous edition.

SAS execution remains pending. Reported assertion passes remain separate from the local reference validation.
