# PDF updates and rebuild instructions

22 September 2026. PDF teaching edition v0.2.0; prompts and SAS fixtures remain v0.1.0.

## This update

| Module | PDF status | Evidence status |
| --- | --- | --- |
| 01 MEAN | Previously delivered PDF imported unchanged | Historical original-prompt responses; B2/B3 reused saved code |
| 02 SUBSTR | Previously delivered PDF imported unchanged | Six reported trials; complete raw transcripts absent from the repository |
| 03 LENGTH | Populated with test setup and A/B result tables | Six reported trials; local reference and counterexamples checked separately |
| 04 CAT/CATX | Populated with test setup and A/B result tables | Six reported trials; A3 readable-name agreement distinguished from missing stored widths |
| 05-10 | Existing PDFs retained | Reported result files are present; PDF evidence updates still pending |

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
python validation/length-reference-20260922.py
python validation/cat-reference-20260922.py
```

The default output replaces the PDF in its module folder. To generate a separate review copy:

```bash
python tools/build_module_03.py --output /tmp/module-03-length.pdf
```

The rebuilds reproduce content and layout. PDF timestamps and document identifiers can change, so use the manifest for the exact delivered files and rendered pages for visual comparison.

## Verification and provenance

- `module-03-length/evidence-review-20260922.md` records the evidence boundary and interpretation.
- `module-04-cat/evidence-review-20260922.md` records the CAT/CATX evidence boundary and interpretation corrections. Reported full matches are A 0/3 and B 3/3; complete raw responses and execution logs are absent.
- `validation/length-reference-20260922.txt` records local reference checks, not original model-response execution.
- `validation/cat-reference-20260922.txt` records exact stored-value checks and locally reconstructed counterexamples, not original trial execution.
- `module-content/pdf-updates-20260922.json` identifies the baseline and SHA-256 hashes of the delivered PDFs.
- `file-hashes.json` is retained as the original package manifest, not a current whole-repository manifest.

Preserve complete raw responses and separate execution output in future trials. Record prompt, fixture, model and environment versions so subsequent findings can be traced to their actual inputs.
