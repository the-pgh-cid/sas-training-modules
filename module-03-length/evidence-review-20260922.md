# LENGTH PDF evidence review

Teaching PDF v0.2.0, 22 September 2026. SAS fixture and prompt wording remain v0.1.0.

## Evidence used

- `results-20260921.csv`: six reported runs; numeric match YES for every run; semantic-correctness flags NO for A1-A3 and YES for B1-B3.
- `trial-log-20260921.md`: reported model, client version, effort setting, deployment, prompt version, fresh parallel subagents and implementation observations.
- `analysis-20260921.md`: explanatory summaries and partial code excerpts.
- `prompts.md`, the paired SAS file and `module-content/modules-v0.1.0.json`: unchanged teaching inputs.

The referenced `.output` transcripts are not in the repository at baseline commit `a17fc462c76c4148ea9563914f6f5cd95a1191b2`. The appendix called "Raw Agent Outputs" contains fragments, not complete runnable responses. In particular, the B3 fragment creates `text_padded` without showing how it is assigned to `df['text']`. The PDF therefore calls the trial results and passing assertions **reported**. It does not claim independent execution or verification of the original responses, their isolation, or their exact prompts.

## Teaching interpretation

All six reported numeric vectors match `[3, 3, 10, 1, 1]`. A1-A3 are reported to retain a literal period and omit width-10 storage and the trailing-blank/all-blank rules. The PDF names those behavioral differences instead of treating a specific method name as the sole test of correctness. Equivalent implementations can use different methods.

The current fixture explicitly requires stored text preservation. That scope matters: a translation that deliberately normalizes string storage could be suitable for a different contract. Here, a value-only comparison does not establish that this fixture's stored text and missing input were reproduced.

The source notes' claims of guaranteed correctness, production readiness, universally eliminated variance, and causal explanations about model priors are not adopted. Three reported trials per prompt describe this small set only. The reports also show different padding idioms among B runs, so numerical agreement is not byte-for-byte code identity.

## Local checks

`validation/length-reference-20260922.py` independently checks the fixture and the PDF counterexamples. It demonstrates that direct lengths on `['ABC', 'ABC', 'ABCDEFGHIJ', 'X', '.']` can match the numeric vector while failing the stored-width and missing-value checks. It is explicitly a reconstruction of the described method, not a recovered A transcript.

The reference excludes trailing ordinary spaces, retains leading spaces and tabs, returns 1 for all blanks, preserves the stored source, and checks five widths of 10. These checks cover the supplied ASCII fixture and stated counterexamples only. SAS LENGTH is byte-based; the teaching sample does not establish Unicode equivalence with Python character counts.

SAS execution remains pending. The rule was checked against the [SAS LENGTH function documentation](https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000245907.htm).

## PDF verification

Three pages, original SAS example and both prompts retained, expected values preserved, and original reference link retained. The generated pages were rendered and visually inspected. No new LLM trials were run.
