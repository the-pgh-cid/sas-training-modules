"""Run the supplied teaching reference from any working directory."""
from pathlib import Path
from mean_reference import candidate
from pilot_checks import load_cases, run_acceptance

if __name__ == "__main__":
    fixture = Path(__file__).with_name("fixtures.csv").read_text(encoding="utf-8")
    result = run_acceptance(candidate, load_cases(fixture))
    raise SystemExit(0 if result.wasSuccessful() and result.testsRun == 3 else 1)
