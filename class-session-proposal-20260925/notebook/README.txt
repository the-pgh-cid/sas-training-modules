MEAN pilot executable companions

Start with ../04_MEAN_workbook.ipynb in an approved Jupyter environment or VS Code notebook editor.
Use Python 3.10 or later with pandas already available in the approved environment.
The exact locally tested versions are recorded in environment-tested.txt.
The notebook is self-contained. It does not install packages or connect to Bedrock.
The corresponding HTML is a static preview, not an executable notebook.

Run the companion Python reference from any working directory:
    python /path/to/notebook/test_reference.py
On Windows, supply the equivalent path and approved Python command.

Contents:
  fixtures.csv              Shared repository inputs and separate expected results.
  mean_reference.py         Supplied reference callable, not a captured model response.
  pilot_checks.py           Three-test callable-based acceptance harness.
  test_reference.py         Runner; exits nonzero on any failed check.
  mean_source.sas           Original three-row SAS source for licensed execution.
  environment-tested.txt    Actual authoring versions, not mandatory enterprise versions.
  source-provenance.json    Upstream commit, blob hashes and adaptation notes.
  validation-results.txt    Locally recorded reference and diagnostic check output.

Never relabel local Python reference results as SAS execution or live model results.
No source repository changes were made by creating this package.
