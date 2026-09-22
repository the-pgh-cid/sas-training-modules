# PDF updates and rebuild instructions

22 September 2026. PDF teaching edition v0.2.0; prompts and SAS fixtures remain v0.1.0.

## This update

| Module | PDF status | Evidence status |
| --- | --- | --- |
| 01 MEAN | Previously delivered PDF imported unchanged | Historical original-prompt responses; B2/B3 reused saved code |
| 02 SUBSTR | Previously delivered PDF imported unchanged | Six reported trials; complete raw transcripts absent from the repository |
| 03 LENGTH | Populated with test setup and A/B result tables | Six reported trials; local reference and counterexamples checked separately |
| 04 CAT/CATX | Populated with test setup and A/B result tables | Six reported trials; A3 readable-name agreement distinguished from missing stored widths |
| [05 ROUND](module-05-round/module-05-round.pdf) | Populated with test setup and A/B result tables | A 3/3 and B 3/3 reported numeric matches; A1's explanation is incorrect |
| [06 INTCK](module-06-intck/module-06-intck.pdf) | Populated with test setup and A/B result tables | A 3/3 and B 3/3 reported matches; different A methods preserve boundary counting |
| [07 COMPRESS](module-07-compress/module-07-compress.pdf) | Populated with test setup and A/B result tables | A 2/3 and B 3/3 reported matches; A1 retains digits for `ka` |
| [08 INPUT](module-08-input/module-08-input.pdf) | Populated with test setup and A/B result tables | A 3/3 and B 3/3 reported matches; value and type checks remain distinct |
| [09 FIRST./LAST.](module-09-firstvar/module-09-firstvar.pdf) | Populated with test setup, A/B results and compliance distinction | A 3/3 and B 3/3 reported output matches; B2/B3 omit explicit endpoint handling |
| [10 LAG](module-10-lag/module-10-lag.pdf) | Populated with test setup and A/B result tables | A 3/3 and B 3/3 reported matches; shift equivalence is scoped to this per-row program |

The original `module-content/modules-v0.1.0.json` remains the baseline teaching source. The scripts in `tools/` implement the PDF updates without silently changing the trial prompts. Original source notes, CSV files and trial logs are retained as evidence, even where the PDF's interpretation is more limited.

The earlier project-wide statements about all trials being pending describe the 18 September edition. `STATUS.md` and `TESTING-GUIDE.md` also contain legacy paths and unsupported predictions about expected model behavior. They require a separate teaching-guide revision; use this update table for current PDF status and each module's `prompts.md` for the exact prompt.

MEAN's setup panel intentionally preserves the previously delivered wording, which says the environment was not stated in that PDF. The repository now also includes original MEAN transcripts and a README with historical metadata. Reconciling that panel against the newly accessible transcripts is a later edit, not part of this unchanged import.

## Rebuild

Use a normal clone with history that includes baseline commit `a17fc462c76c4148ea9563914f6f5cd95a1191b2`. Each script obtains the original PDF with `git show`, then applies the edit once. This prevents overlays from accumulating when a script is rerun. GitHub's source ZIP does not contain that history; supply `--source` with an original v0.1.0 PDF when using a ZIP or a shallow clone without the baseline.

Tested with Python 3.12.14, PyMuPDF 1.26.6, ReportLab 4.4.9 and pandas 2.2.3. The scripts use DejaVu Sans and DejaVu Sans Mono from `/usr/share/fonts/truetype/dejavu/` on Linux (the `fonts-dejavu-core` package on Debian/Ubuntu).

```bash
python -m pip install -r tools/requirements-pdf.txt
python tools/build_module_01.py
python tools/build_module_02.py
python tools/build_module_03.py
python tools/build_module_04.py
python tools/build_module_05.py
python tools/build_module_06.py
python tools/build_module_07.py
python tools/build_module_08.py
python tools/build_module_09.py
python tools/build_module_10.py
python validation/length-reference-20260922.py
python validation/cat-reference-20260922.py
python validation/round-reference-20260922.py
python validation/intck-reference-20260922.py
python validation/compress-reference-20260922.py
python validation/input-reference-20260922.py
python validation/firstvar-reference-20260922.py
python validation/lag-reference-20260922.py
```

The default output replaces the PDF in its module folder. To generate a separate review copy:

```bash
python tools/build_module_03.py --output /tmp/module-03-length.pdf
```

The rebuilds reproduce content and layout. PDF timestamps and document identifiers can change, so use the manifest for the exact delivered files and rendered pages for visual comparison.

## Verification and provenance

- `module-03-length/evidence-review-20260922.md` records the evidence boundary and interpretation.
- `module-04-cat/evidence-review-20260922.md` records the CAT/CATX evidence boundary and interpretation corrections. Reported full matches are A 0/3 and B 3/3; complete raw responses and execution logs are absent.
- Each module 05-10 has an `evidence-review-20260922.md` explaining which reported results support the PDF and where the original analysis needs narrower wording. Original CSVs, trial logs, prompts and SAS fixtures remain unchanged.
- The module 05-10 trial summaries report Claude Sonnet 4.5, Claude Code 2.1.278, AWS Bedrock GovCloud, `effortLevel=high`, prompt v0.1.0, and six fresh parallel agents on 21 September. Complete raw responses and separate execution logs are not present in the repository. Reported assertion passes are not independently authenticated executions.
- A matching output, a correct explanation and compliance with a requested method are separate checks. ROUND A1 and FIRST./LAST. B2/B3 make these distinctions visible. A shared method does not establish identical responses, and three runs per prompt do not guarantee future outcomes.
- `validation/length-reference-20260922.txt` records local reference checks, not original model-response execution.
- `validation/cat-reference-20260922.txt` records exact stored-value checks and locally reconstructed counterexamples, not original trial execution.
- The corresponding `validation/{round,intck,compress,input,firstvar,lag}-reference-20260922.py` scripts and `.txt` outputs check local reference values and selected counterexamples. They do not replace the original model responses or establish SAS execution.
- [Modules 05-10 release review](validation/pdf-updates-05-10-review-20260922.md) records the 18-page visual review, source/prompt preservation, local validation and pixel-identical rebuild checks.
- `module-content/pdf-updates-20260922.json` identifies the baseline and SHA-256 hashes of the delivered PDFs.
- `file-hashes.json` is retained as the original package manifest, not a current whole-repository manifest.

Preserve complete raw responses and separate execution output in future trials. Record prompt, fixture, model and environment versions so subsequent findings can be traced to their actual inputs.
