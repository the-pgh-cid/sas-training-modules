# Modules 05-10 PDF release review

22 September 2026. Teaching edition v0.2.0; original prompts and SAS fixtures v0.1.0.
Repository base: `c8296213ce5a834eb4c279330a7aac6093d565d9`.

## Completed checks

- Six PDFs, each exactly three 960 x 600 pages, were rendered and visually reviewed by their module author and an independent integration review. Corrected footer overlap and text-flow issues were re-rendered and checked.
- All 18 final pages reproduce pixel for pixel when rebuilt from their immutable original PDF using `--source`. PDF byte identifiers can change across builds; delivered SHA-256 hashes are in `module-content/pdf-updates-20260922.json`.
- Full original SAS and both prompts remain extractable from each PDF after whitespace normalization. Every extracted text span falls within its page bounds.
- All six local reference/counterexample scripts passed when rerun during integration. Their captured standard output matches the committed `.txt` reports exactly.
- Original prompts, SAS fixtures, results CSVs, trial logs and source analyses match the repository base byte for byte. Modules 01-04 PDFs also remain byte-identical.
- Root documentation points readers to the current PDF status while marking the older package notes as historical.

## Reported outcomes carried into the PDFs

| Module | Prompt A expected-value matches | Prompt B expected-value matches | Distinction retained |
| --- | --- | --- | --- |
| 05 ROUND | 3/3 | 3/3 | A1 explanation is wrong despite matching numbers; A2 and A3 explain the difference correctly |
| 06 INTCK | 3/3 | 3/3 | Custom functions and direct formulas both preserve the specified boundary counts |
| 07 COMPRESS | 2/3 | 3/3 | A1 keeps digits under the letters-only requirement |
| 08 INPUT | 3/3 | 3/3 | Values and numeric/datetime types need separate checks |
| 09 FIRST./LAST. | 3/3 | 3/3 | B2/B3 omit explicit endpoint handling despite reported correct outputs |
| 10 LAG | 3/3 | 3/3 | Row shifts fit these unconditional per-row calls; missing values and order matter |

These counts describe the supplied summaries, not independently replayed historical runs. Complete original responses and separate execution logs are absent. No new Bedrock trials or SAS execution were performed. Local counterexamples are labeled separately and do not change historical scores.

## Reproduction

Use the commands in `PDF-BUILD.md`. A normal clone must include baseline commit `a17fc462c76c4148ea9563914f6f5cd95a1191b2`; otherwise pass an original v0.1.0 PDF through `--source` and a different destination through `--output`.

Integration used Python 3.12.14, pandas 2.2.3, PyMuPDF 1.26.6 and ReportLab 4.4.9. The review rendered PDFs with PyMuPDF and compared unscaled page pixel buffers. Fonts and dependencies are documented in `PDF-BUILD.md`.
